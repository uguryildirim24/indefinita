"""Lead-SNP LD in the public 1000 Genomes phase 3 EUR PLINK reference."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import zipfile
import numpy as np
from associate import HERE, rows, tsv, sha

DATA = HERE / 'data'
COMP = str.maketrans('ACGT', 'TGCA')


def orientation(a1, a2, ref1, ref2):
    if {a1, a2} in [{'A', 'T'}, {'C', 'G'}]:
        return None, 'palindromic_not_oriented'
    if (a1, a2) == (ref1, ref2):
        return 1, 'direct'
    if (a1, a2) == (ref2, ref1):
        return -1, 'swapped'
    if (a1.translate(COMP), a2.translate(COMP)) == (ref1, ref2):
        return 1, 'complement'
    if (a1.translate(COMP), a2.translate(COMP)) == (ref2, ref1):
        return -1, 'complement_swapped'
    return None, 'allele_mismatch'


def main():
    m = {r['file']: r for r in json.loads((HERE / 'fetch-manifest.json').read_text())}
    r = m['eur.zip']
    if r.get('expected_sha256') or r['http_status'] != 200 or sha(DATA / 'eur.zip') != r['sha256']:
        raise RuntimeError('Reference checksum mismatch')
    with zipfile.ZipFile(DATA / 'eur.zip') as z:
        names = z.namelist()
        print(names)
        for suffix in ['.bed', '.bim', '.fam']:
            name, = [n for n in names if n.endswith(suffix)]
            target = DATA / Path(name).name
            if not target.exists():
                with z.open(name) as src, target.open('wb') as dst:
                    while b := src.read(1024 * 1024):
                        dst.write(b)
    bed, = DATA.glob('*.bed')
    bim, = DATA.glob('*.bim')
    fam, = DATA.glob('*.fam')
    n = sum(1 for _ in fam.open())
    bytes_per_variant = (n + 3) // 4
    pilots = [r for r in rows(HERE / 'regions.tsv') if r['pilot'] == 'True']
    local = {r['MarkerName']: r for r in rows(HERE / 'pilot-gwas.tsv')}
    lookup = {}
    duplicate = set()
    for i, line in enumerate(bim.open()):
        c, marker, cm, pos, a1, a2 = line.split()
        if marker in local:
            if marker in lookup:
                duplicate.add(marker)
            lookup[marker] = (i, c, int(pos), a1, a2)
    audit = []
    vectors = {}
    # PLINK SNP-major 00=A1/A1, 01=missing, 10=heterozygous, 11=A2/A2.
    decode = np.array([2., np.nan, 1., 0.])
    with bed.open('rb') as f:
        if f.read(3) != b'\x6c\x1b\x01':
            raise RuntimeError('Not SNP-major PLINK BED')
        for marker, g in local.items():
            ref = lookup.get(marker)
            sign = None
            status = 'absent_reference'
            if marker in duplicate:
                status = 'duplicate_reference_marker'
            elif ref:
                i, c, pos, a1, a2 = ref
                if c != g['CHR'] or pos != int(g['POS']):
                    status = 'build_or_position_mismatch'
                else:
                    sign, status = orientation(g['A1'], g['A2'], a1, a2)
                    if sign:
                        f.seek(3 + i * bytes_per_variant)
                        b = np.frombuffer(f.read(bytes_per_variant), dtype=np.uint8)
                        v = decode[((b[:, None] >> np.array([0, 2, 4, 6])) & 3).ravel()[:n]]
                        freq = float(np.nanmean(v) / 2)
                        v[np.isnan(v)] = np.nanmean(v)
                        if np.std(v) == 0:
                            status = 'monomorphic_reference'
                        else:
                            vectors[marker] = (v - v.mean()) * sign
                            freq = freq if sign == 1 else 1 - freq
                            status += ';frequency_difference=' + format(freq - float(g['EAF']), '.5g')
            audit.append(dict(region_id=g['region_id'], marker=marker, chr37=g['CHR'], pos37=g['POS'],
                              reference_status=status, beta_allele=g['A1'], other_allele=g['A2']))
    ldrows = []
    for region in pilots:
        lead = vectors.get(region['lead_snp'])
        for marker, g in local.items():
            if g['region_id'] != region['region_id']:
                continue
            v = vectors.get(marker)
            corr = float(np.dot(v, lead) / np.sqrt(np.dot(v, v) * np.dot(lead, lead))) if v is not None and lead is not None else None
            ldrows.append(dict(region_id=g['region_id'], marker=marker, pos37=g['POS'], p=g['Pval'],
                               lead_snp=region['lead_snp'], r=corr, r2=corr * corr if corr is not None else None))
    tsv('ld-harmonization.tsv', audit)
    tsv('pilot-lead-ld.tsv', ldrows)
    altrows = []
    for gene in rows(HERE / 'locus-alternatives.tsv'):
        if gene['pilot'] != 'True':
            continue
        body = [r for r in ldrows if r['region_id'] == gene['region_id'] and int(gene['start']) <= int(r['pos37']) <= int(gene['end'])]
        usable = [r for r in body if r['r2'] is not None]
        strongest = min(body, key=lambda r: float(r['p'])) if body else {}
        strongest_ld = strongest.get('r2')
        altrows.append(dict(region_id=gene['region_id'], gene_id=gene['gene_id'], symbol=gene['symbol'],
                            body_local_snps=len(body), body_ld_covered_snps=len(usable), body_lead=strongest.get('marker'),
                            body_lead_r2_to_region_lead=strongest_ld,
                            body_max_r2_to_region_lead=max((r['r2'] for r in usable), default=None)))
    tsv('gene-ld-alternatives.tsv', altrows)
    summary = dict(reference_samples=n, reference_sha256=r['sha256'], reference='CNCR phase 3 EUR; updated 19/09/2018; GRCh37',
                   dosage='A1 counts; missing mean-imputed; allele-aligned r and r2', local_variants=len(local),
                   harmonized_variants=len(vectors), statuses=dict(Counter(a['reference_status'].split(';')[0] for a in audit)),
                   lead_coverage={r['region_id']: r['lead_snp'] in vectors for r in pilots},
                   absent_ld_is_not_r2_zero=True, causal_gene_assignment=False)
    (HERE / 'ld-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
