"""Stream Lee CP; conservative LD-robust gene tests, regions, separate knownness."""
from __future__ import annotations
import bisect
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / 'data'


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def rows(p):
    with p.open() as f:
        yield from csv.DictReader(f, delimiter='\t')


def tsv(name, records, fields=None):
    records = list(records)
    if fields is None:
        fields = list(dict.fromkeys(k for r in records for k in r))
    with (HERE / name).open('w') as f:
        w = csv.DictWriter(f, fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        for r in records:
            w.writerow({k: 'NA' if r.get(k) is None else r.get(k, 'NA') for k in fields})


def annotation():
    genes = {}
    with gzip.open(DATA / 'gencode-v19.gtf.gz', 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            c = line.rstrip().split('\t')
            chrom = c[0].removeprefix('chr')
            if c[2] != 'gene' or chrom not in {str(i) for i in range(1, 23)}:
                continue
            a = dict(re.findall(r'(\w+) "([^"]+)"', c[8]))
            gid = a['gene_id'].split('.')[0]
            genes[gid] = dict(gene_id=gid, source_symbol=a['gene_name'], chromosome=chrom,
                              start=int(c[3]), end=int(c[4]), gene_type=a['gene_type'])
    return genes


def index_genes(genes):
    bychr = defaultdict(list)
    for g in genes.values():
        bychr[g['chromosome']].append(g)
    index = {}
    for c, gs in bychr.items():
        gs.sort(key=lambda g: g['start'])
        maxend = []
        for g in gs:
            maxend.append(max(g['end'], maxend[-1] if maxend else 0))
        index[c] = (gs, [g['start'] for g in gs], maxend)
    return index


def overlaps(index, chrom, pos):
    gs, starts, ends = index[chrom]
    i = bisect.bisect_right(starts, pos) - 1
    while i >= 0 and ends[i] >= pos:
        if gs[i]['end'] >= pos:
            yield gs[i]
        i -= 1


def valid(r):
    try:
        p, beta, se, eaf = (float(r[k]) for k in ['Pval', 'Beta', 'SE', 'EAF'])
        pos = int(r['POS'])
        if r['CHR'] not in {str(i) for i in range(1, 23)}:
            return 'non_autosome'
        if not all(math.isfinite(x) for x in [p, beta, se, eaf]) or not (0 < p <= 1 and se > 0 and 0 < eaf < 1 and pos > 0):
            return 'invalid_numeric'
        if r['A1'] not in 'ACGT' or r['A2'] not in 'ACGT' or len(r['A1']) != 1 or len(r['A2']) != 1 or r['A1'] == r['A2']:
            return 'non_biallelic_snv'
    except (ValueError, KeyError):
        return 'parse_error'
    return None


def extract_methods():
    from pypdf import PdfReader
    methods = ' '.join(' '.join(p.extract_text() for p in PdfReader(DATA / 'lee-methods.pdf').pages).split())
    marker = '1.11. Cognitive Performance'
    first = methods.index(marker)
    start = methods.index(marker, first + len(marker))
    end = methods.index('1.13.', start)
    (HERE / 'source-method-excerpts.txt').write_text('Lee 2018 methods PDF; DOI 10.1038/s41588-018-0147-3; whitespace normalized, excerpt only.\n' + methods[start:end].strip() + '\n')


def main():
    manifest = {r['file']: r for r in json.loads((ROOT / 'derived/fetch-manifest.json').read_text())}
    provenance = []
    for n in ['lee2018.txt', 'gencode-v19.gtf.gz', 'hgnc.tsv', 'pharos400.csv', 'lee-methods.pdf']:
        r = manifest[n]
        if r.get('expected_sha256') or r['http_status'] != 200 or sha(DATA / n) != r['sha256']:
            raise RuntimeError('Unavailable or changed pinned input: ' + n)
        provenance.append(dict(r, source_observation='inherited committed downloader record; exact pin checked locally',
            local_file_mtime_utc=datetime.fromtimestamp((DATA / n).stat().st_mtime, timezone.utc).isoformat()))
    for n in ['knownness-ranks.tsv', 'gene-evidence.tsv', 'fetch-manifest.json']:
        provenance.append(dict(file='derived/' + n, sha256=sha(ROOT / 'derived' / n), access='committed data layer; not a fresh source GET'))
    tsv('input-provenance.tsv', provenance)
    extract_methods()
    allgenes = annotation()
    genes = {k: g for k, g in allgenes.items() if g['gene_type'] == 'protein_coding'}
    index = index_genes(genes)
    counts = Counter()
    seen = set()
    significant = defaultdict(list)
    minrows = {}
    for r in rows(DATA / 'lee2018.txt'):
        counts['total_rows'] += 1
        err = valid(r)
        if err:
            counts[err] += 1
            continue
        marker = r['MarkerName']
        if marker in seen:
            # A conflicting duplicate must not be silently counted or assigned.
            raise RuntimeError('Duplicate GWAS marker: ' + marker)
        seen.add(marker)
        counts['valid_rows'] += 1
        c, pos, p = r['CHR'], int(r['POS']), float(r['Pval'])
        mapped = False
        for g in overlaps(index, c, pos):
            mapped = True
            gid = g['gene_id']
            g['snp_count'] = g.get('snp_count', 0) + 1
            if gid not in minrows or p < float(minrows[gid]['Pval']):
                minrows[gid] = r
        counts['rows_overlapping_protein_coding_body'] += mapped
        if p < 5e-8:
            significant[c].append(r)
            counts['genome_wide_significant_rows'] += 1
        if counts['total_rows'] % 2_000_000 == 0:
            print(counts['total_rows'], flush=True)
    del seen
    hgnc = defaultdict(list)
    for r in rows(DATA / 'hgnc.tsv'):
        if r['status'] == 'Approved' and r['ensembl_gene_id']:
            hgnc[r['ensembl_gene_id']].append(r)
    known = {r['ensembl_gene_id']: r for r in rows(ROOT / 'derived/knownness-ranks.tsv')}
    ledger = {r['ensembl_gene_id']: r for r in rows(ROOT / 'derived/gene-evidence.tsv')}
    ntest = len(minrows)
    for gid, g in allgenes.items():
        h = hgnc.get(gid, [])
        g.update(symbol=h[0]['symbol'] if len(h) == 1 else g['source_symbol'],
                 hgnc_mapping='unique' if len(h) == 1 else 'ambiguous' if h else 'unmapped',
                 gene_length_bp=g['end'] - g['start'] + 1)
        g['association_test_scope'] = 'protein_coding_gene_body' if g['gene_type'] == 'protein_coding' else 'not_tested_non_protein_coding_alternative'
        g['snp_count'] = g.get('snp_count', 0) if g['gene_type'] == 'protein_coding' else None
        g['snp_density_per_kb'] = g['snp_count'] * 1000 / g['gene_length_bp'] if g['snp_count'] is not None else None
        r = minrows.get(gid)
        g['body_min_p'] = float(r['Pval']) if r else None
        g['body_lead_snp'] = r['MarkerName'] if r else None
        g['body_lead_pos'] = int(r['POS']) if r else None
        g['gene_bonferroni_p'] = min(1., g['snp_count'] * g['body_min_p']) if r else None
        g['across_gene_bonferroni_p'] = min(1., ntest * g['gene_bonferroni_p']) if r else None
        g['gene_association_fwer05'] = bool(r and g['across_gene_bonferroni_p'] < .05)
        k = known.get(gid, {})
        g['unknome_knownness'] = k.get('knownness')
        g['unknome_rank'] = k.get('rank_least_known_first')
        g['knownness_provenance'] = 'Unknome 18_Mar_2026; maximum over uniquely HGNC-mapped proteins; derived/knownness-ranks.tsv' if k else 'Unknome unmapped/unscored; not zero knownness'
        for key in ['pharos_tdl', 'human_pubmed_count', 'savage_magma_p', 'savage_fuma_mapping', 'savage_fuma_loci', 'rare_significant_qc_pass']:
            g[key] = ledger.get(gid, {}).get(key)
        g['ledger_annotation_coverage'] = gid in ledger
    inventory = sorted(genes.values(), key=lambda g: (g['gene_bonferroni_p'] if g['gene_bonferroni_p'] is not None else 2., g['gene_id']))
    for i, g in enumerate(inventory, 1):
        g['association_rank'] = i
    tsv('gene-associations.tsv', inventory)
    regions = []
    for c, rs in significant.items():
        rs.sort(key=lambda r: int(r['POS']))
        current = None
        for r in rs:
            start, end = max(1, int(r['POS']) - 500_000), int(r['POS']) + 500_000
            if current is None or start > current['end']:
                current = dict(chromosome=c, start=start, end=end, variants=[])
                regions.append(current)
            else:
                current['end'] = max(end, current['end'])
            current['variants'].append(r)
    regions.sort(key=lambda x: min(float(r['Pval']) for r in x['variants']))
    for i, region in enumerate(regions, 1):
        lead = min(region['variants'], key=lambda r: float(r['Pval']))
        region.update(region_id=f'R{i:03d}', region_rank=i, lead_snp=lead['MarkerName'], lead_pos=int(lead['POS']),
                      lead_p=float(lead['Pval']), gws_snp_count=len(region['variants']), pilot=i <= 3)
    tsv('regions.tsv', [{k: v for k, v in r.items() if k != 'variants'} for r in regions])
    alternatives = []
    for region in regions:
        for g in allgenes.values():
            if g['chromosome'] == region['chromosome'] and g['start'] <= region['end'] and g['end'] >= region['start']:
                alternatives.append(dict(region_id=region['region_id'], region_rank=region['region_rank'], pilot=region['pilot'], **g))
    tsv('locus-alternatives.tsv', alternatives)
    # Second stream: bounded pilot regions only, no knownness-dependent selection.
    pilots = regions[:3]
    local = []
    for r in rows(DATA / 'lee2018.txt'):
        if valid(r):
            continue
        for region in pilots:
            if r['CHR'] == region['chromosome'] and region['start'] <= int(r['POS']) <= region['end']:
                local.append(dict(region_id=region['region_id'], **r))
    tsv('pilot-gwas.tsv', local)
    summary = dict(counts, tested_genes=ntest, total_autosomal_protein_coding_genes=len(genes),
                   associated_genes=sum(g['gene_association_fwer05'] for g in genes.values()), regions=len(regions),
                   pilot_regions=[{k: v for k, v in x.items() if k != 'variants'} for x in pilots],
                   knownness_used_to_choose_evidence=False, procedure='SNP-min union bound; gene body; all tested genes Bonferroni',
                   associations_are_not_causal_assignments=True)
    (HERE / 'association-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
