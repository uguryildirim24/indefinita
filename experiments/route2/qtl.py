"""Bounded public adult DLPFC QTL follow-up and single-signal coloc sensitivity."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import gzip
import json
import math
import sys
import httpx
import numpy as np
from scipy.special import logsumexp
from pyliftover import LiftOver
import pysam
from associate import HERE, rows, tsv, sha
from ld import orientation

DATA = HERE / 'data'
URL = 'https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/sumstats/QTS000015/QTD000176/QTD000176.all.tsv.gz'


def coloc(beta1, se1, beta2, se2, maf2, n2, p12, effect_prior_sd=0.15):
    # coloc sdY.est: no-intercept regression 2*N*MAF*(1-MAF) on 1/varbeta.
    inv = 1 / se2 ** 2
    nvx = 2 * n2 * maf2 * (1 - maf2)
    sdy2 = float(np.dot(inv, nvx) / np.dot(inv, inv))
    if not math.isfinite(sdy2) or sdy2 <= 0:
        raise ValueError('QTL trait variance not estimable')
    logbfs = []
    for beta, se, sdy in [(beta1, se1, 1.), (beta2, se2, np.sqrt(sdy2))]:
        v, w = se ** 2, (effect_prior_sd * sdy) ** 2
        r = w / (w + v)
        logbfs.append(.5 * (np.log1p(-r) + r * (beta / se) ** 2))
    a, b = logbfs
    ma, mb = a.max(), b.max()
    ea, eb = np.exp(a - ma).astype(np.longdouble), np.exp(b - mb).astype(np.longdouble)
    cross = ea.sum() * eb.sum() - np.dot(ea, eb)
    l3 = float(np.log(cross)) + ma + mb if cross > 0 else -np.inf
    l = np.array([0., np.log(1e-4) + logsumexp(a), np.log(1e-4) + logsumexp(b),
                  np.log(1e-4) * 2 + l3, np.log(p12) + logsumexp(a + b)])
    posterior = np.exp(l - logsumexp(l))
    return posterior, sdy2


def main():
    manifest = {r['file']: r for r in json.loads((HERE / 'fetch-manifest.json').read_text())}
    for name in ['hg19ToHg38.over.chain.gz', 'QTD000176.all.tsv.gz.tbi']:
        r = manifest[name]
        if r['http_status'] != 200 or r.get('expected_sha256') or sha(DATA / name) != r['sha256']:
            raise RuntimeError('Unavailable/changed QTL dependency: ' + name)
    lo = LiftOver(str(DATA / 'hg19ToHg38.over.chain.gz'))
    genes = [r for r in rows(HERE / 'locus-alternatives.tsv') if r['pilot'] == 'True']
    candidates = {(r['region_id'], r['gene_id']) for r in genes}
    pilots = [r for r in rows(HERE / 'regions.tsv') if r['pilot'] == 'True']
    mapped = {}
    lift_audit = []
    for r in rows(HERE / 'pilot-gwas.tsv'):
        out = lo.convert_coordinate('chr' + r['CHR'], int(r['POS']) - 1)
        status = 'unmapped_or_nonunique_or_changed_chromosome'
        if out and len(out) == 1 and out[0][0] == 'chr' + r['CHR']:
            c, pos, strand, score = out[0]
            rr = dict(r)
            if strand == '-':
                rr['A1'] = r['A1'].translate(str.maketrans('ACGT', 'TGCA'))
                rr['A2'] = r['A2'].translate(str.maketrans('ACGT', 'TGCA'))
            key = (r['region_id'], c.removeprefix('chr'), pos + 1)
            if key in mapped:
                raise RuntimeError('Multiple GWAS markers at one lifted position')
            mapped[key] = rr
            status = 'unique_' + strand
        lift_audit.append(dict(marker=r['MarkerName'], region_id=r['region_id'], chr37=r['CHR'], pos37=r['POS'],
                               status=status, chr38=out[0][0] if out and len(out) == 1 else None,
                               pos38=out[0][1] + 1 if out and len(out) == 1 else None))
    tsv('liftover-audit.tsv', lift_audit)
    access = dict(url=URL, observed_utc=datetime.now(timezone.utc).isoformat(), study='GTEx v8 reprocessed eQTL Catalogue QTD000176; adult frontal cortex; N=175',
                  index_sha256=manifest['QTD000176.all.tsv.gz.tbi']['sha256'], access='not attempted')
    cache = DATA / 'qtl-pilot.tsv.gz'
    cache_manifest = DATA / 'qtl-cache.json'
    if cache.exists() and cache_manifest.exists():
        old = json.loads(cache_manifest.read_text())
        if sha(cache) != old['sha256'] or old['pilot_gwas_sha256'] != sha(HERE / 'pilot-gwas.tsv') or old['locus_alternatives_sha256'] != sha(HERE / 'locus-alternatives.tsv') or old['chain_sha256'] != manifest['hg19ToHg38.over.chain.gz']['sha256']:
            raise RuntimeError('QTL subset or query dependency checksum mismatch')
        access = old
    else:
        try:
            # Observe actual range support without ever mirroring the bulk file.
            with httpx.Client(timeout=90, follow_redirects=True) as client:
                with client.stream('GET', URL, headers={'Range': 'bytes=0-65535', 'Accept-Encoding': 'identity'}) as resp:
                    access.update(http_status=resp.status_code, final_url=str(resp.url), content_range=resp.headers.get('content-range'),
                                  etag=resp.headers.get('etag'), last_modified=resp.headers.get('last-modified'))
                    if resp.status_code != 206:
                        raise RuntimeError('Server did not establish byte-range support')
                    headerbytes = b''.join(resp.iter_bytes())
                    access['range_response_sha256'] = __import__('hashlib').sha256(headerbytes).hexdigest()
            with pysam.TabixFile(URL, index=str(DATA / 'QTD000176.all.tsv.gz.tbi')) as tab:
                # Catalogue's column line is not always a '#' tabix header.
                import zlib
                first_line = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(headerbytes).splitlines()[0].decode()
                header = (tab.header[-1] if tab.header else first_line).lstrip('#').split('\t')
                with gzip.open(cache, 'wt') as dst:
                    w = csv.DictWriter(dst, ['region_id'] + header, delimiter='\t', lineterminator='\n')
                    w.writeheader()
                    fetched = 0
                    for region in pilots:
                        rid, c = region['region_id'], region['chromosome']
                        positions = [k[2] for k in mapped if k[0] == rid]
                        start, end = min(positions), max(positions)
                        for line in tab.fetch(c, start - 1, end):
                            q = dict(zip(header, line.split('\t')))
                            gid = q['gene_id'].split('.')[0]
                            if (rid, gid) in candidates:
                                w.writerow(dict(region_id=rid, **q))
                                fetched += 1
                        print(rid, 'selected QTL records', fetched, flush=True)
            access.update(access='anonymous HTTPS range/tabix selected local full nominal summaries; no significance filter',
                          selected_rows=fetched, sha256=sha(cache), pilot_gwas_sha256=sha(HERE / 'pilot-gwas.tsv'),
                          locus_alternatives_sha256=sha(HERE / 'locus-alternatives.tsv'), chain_sha256=manifest['hg19ToHg38.over.chain.gz']['sha256'])
            cache_manifest.write_text(json.dumps(access, indent=2) + '\n')
        except Exception as e:
            access.update(access='unavailable; query failed; not a biological null', error=str(e))
            if cache.exists():
                cache.unlink()  # Never analyze a partial query.
    history_path = HERE / 'qtl-access-history.json'
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    previous_path = HERE / 'qtl-access.json'
    if previous_path.exists() and not history:
        history.append(json.loads(previous_path.read_text()))
    if not history or history[-1] != access:
        history.append(access)
    history_path.write_text(json.dumps(history, indent=2) + '\n')
    previous_path.write_text(json.dumps(access, indent=2) + '\n')
    if not cache.exists():
        tsv('coloc-sensitivity.tsv', [], ['region_id', 'gene_id', 'p12', 'H0', 'H1', 'H2', 'H3', 'H4', 'status'])
        tsv('qtl-gene-coverage.tsv', [dict(region_id=g['region_id'], gene_id=g['gene_id'], symbol=g['symbol'], status='QTL access unavailable') for g in genes])
        print(access)
        return
    aligned = defaultdict(dict)
    rawcount = Counter()
    excludes = Counter()
    with gzip.open(cache, 'rt') as f:
        for q in csv.DictReader(f, delimiter='\t'):
            gid = q['gene_id'].split('.')[0]
            key = (q['region_id'], gid)
            rawcount[key] += 1
            g = mapped.get((q['region_id'], q['chromosome'], int(q['position'])))
            if not g:
                excludes['not_in_lifted_gwas'] += 1
                continue
            sign, status = orientation(g['A1'], g['A2'], q['alt'], q['ref'])
            if sign is None:
                excludes[status] += 1
                continue
            try:
                qb, qs, qm, qn = float(q['beta']), float(q['se']), float(q['maf']), float(q['an']) / 2
                if not all(math.isfinite(x) for x in [qb, qs, qm, qn]) or not (qs > 0 and 0 < qm <= .5 and qn > 0):
                    raise ValueError('invalid QTL numeric')
            except ValueError:
                excludes['invalid_qtl_numeric'] += 1
                continue
            # rsID aliases duplicate the identical variant record; collapse, not extra evidence.
            variant = q['variant']
            vals = dict(marker=g['MarkerName'], pos37=int(g['POS']), beta1=float(g['Beta']), se1=float(g['SE']), beta2=qb * sign,
                        se2=qs, maf2=qm, n2=qn, gwas_p=float(g['Pval']), qtl_p=float(q['pvalue']))
            if variant in aligned[key] and aligned[key][variant] != vals:
                raise RuntimeError('Conflicting duplicated QTL variant')
            aligned[key][variant] = vals
    coverage, results = [], []
    for g in genes:
        key = (g['region_id'], g['gene_id'])
        vals = list(aligned[key].values())
        lead = next(r['lead_snp'] for r in pilots if r['region_id'] == g['region_id'])
        coverage.append(dict(region_id=g['region_id'], gene_id=g['gene_id'], symbol=g['symbol'],
                             nominal_rows=rawcount[key], shared_aligned_variants=len(vals),
                             gwas_lead_covered=any(v['marker'] == lead for v in vals),
                             min_qtl_p=min((v['qtl_p'] for v in vals), default=None),
                             status='shared local summaries' if vals else 'not covered/aligned; not null evidence'))
        if len(vals) < 2:
            continue
        lead_pos = int(next(r['lead_pos'] for r in pilots if r['region_id'] == g['region_id']))
        windows = [('gene_cis_shared_region', vals), ('lead_250kb_shared_subset', [v for v in vals if abs(v['pos37'] - lead_pos) <= 250_000])]
        for window, subset in windows:
            if len(subset) < 2:
                continue
            arrays = [np.array([v[k] for v in subset]) for k in ['beta1', 'se1', 'beta2', 'se2', 'maf2', 'n2']]
            for effect_prior in [.1, .15, .2]:
                for p12 in [1e-6, 1e-5, 1e-4]:
                    post, sdy2 = coloc(*arrays, p12, effect_prior)
                    results.append(dict(region_id=g['region_id'], gene_id=g['gene_id'], symbol=g['symbol'], p12=p12,
                                        effect_prior_sd_in_trait_sd=effect_prior, window=window,
                                        shared_variants=len(subset), H0=post[0], H1=post[1], H2=post[2], H3=post[3], H4=post[4],
                                        H4_given_H3_or_H4=post[4] / (post[3] + post[4]), qtl_sdY_est=math.sqrt(sdy2),
                                        gwas_lead_covered=any(v['marker'] == lead for v in subset),
                                        assumptions='one causal variant per trait; shared observed subset; p1=p2=1e-4; effect prior SD as given times sdY; CP sdY=1; window sensitivity is not multi-signal conditioning'))
    tsv('qtl-gene-coverage.tsv', coverage)
    tsv('coloc-sensitivity.tsv', results)
    (HERE / 'qtl-harmonization-summary.json').write_text(json.dumps(dict(exclusions=dict(excludes),
                 aligned_gene_region_pairs=sum(bool(v) for v in aligned.values()), variant_join='unique GRCh37-to-38 lift; exact position and biallelic alleles; no palindrome orientation',
                 prior_choices_are_sensitivity_not_acceptance_thresholds=True), indent=2) + '\n')

if __name__ == '__main__':
    main()
