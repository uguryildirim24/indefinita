"""Fetch pinned public inputs; construct audited drug/day/replicate join before modeling."""
from pathlib import Path
import datetime
import gzip
import hashlib
import json
import re
import urllib.request
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
AUTHOR_COMMIT = '5e51f9d9e4e0b196e8d64134b7605b3f12902787'
TPM = 'GSE230679_20230425_psychadelic_study_tpm_matrix.tsv.gz'
DE = 'GSE230679_criticalPeriodDE_all_test_results.tsv.gz'
BASE = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE230nnn/GSE230679/'
SOURCES = {
    TPM: BASE + 'suppl/' + TPM,
    DE: BASE + 'suppl/' + DE,
    'GSE230679_family.soft.gz': BASE + 'soft/GSE230679_family.soft.gz',
    'paper.xml': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10284704/fullTextXML',
    'SupCode4_RNAseqAnalysis.Rmd': f'https://raw.githubusercontent.com/genesofeve/DolenPsychedelicOpenState/{AUTHOR_COMMIT}/SupCode4_RNAseqAnalysis.Rmd',
    'author_tree.json': f'https://api.github.com/repos/genesofeve/DolenPsychedelicOpenState/git/trees/{AUTHOR_COMMIT}?recursive=1',
}


def prepare():
    DATA.mkdir(exist_ok=True)
    manifest = []
    for name, url in SOURCES.items():
        path = DATA / name
        if not path.exists():
            with urllib.request.urlopen(url) as response:
                path.write_bytes(response.read())
        content = path.read_bytes()
        manifest.append(dict(file=name, url=url, bytes=len(content),
                             sha256=hashlib.sha256(content).hexdigest(),
                             local_file_mtime_utc=datetime.datetime.fromtimestamp(
                                 path.stat().st_mtime, datetime.timezone.utc).isoformat()))
    pd.DataFrame(manifest).to_csv(ROOT / 'input_provenance.tsv', sep='\t', index=False)
    records = []
    current = None
    with gzip.open(DATA / 'GSE230679_family.soft.gz', 'rt') as f:
        for line in f:
            line = line.strip()
            if line.startswith('^SAMPLE = '):
                current = {'gsm': line.split(' = ')[1], 'characteristics': {}, 'descriptions': []}
                records.append(current)
            elif current and line.startswith('!Sample_title = '):
                current['title'] = line.split(' = ', 1)[1]
            elif current and line.startswith('!Sample_characteristics_ch1 = '):
                key, value = line.split(' = ', 1)[1].split(': ', 1)
                current['characteristics'][key] = value
            elif current and line.startswith('!Sample_description = '):
                current['descriptions'].append(line.split(' = ', 1)[1])
    rows = []
    for r in records:
        drug, day, replicate = re.fullmatch(r'NAc (\w+) (\d+) days replicate (\d+)', r['title']).groups()
        day, replicate = int(day), int(replicate)
        c = r['characteristics']
        assert drug == c['treatment -_drug'] and day == int(c['treatment -_time_(days)'])
        state = c['treatment -_critical_period']
        expected = 'open' if drug in ('LSD', 'MDMA') or (drug == 'ketamine' and day == 2) else 'closed'
        assert state == expected  # Nardou main text, ECM section
        desc = [d for d in r['descriptions'] if re.fullmatch(r'\d+(saline|cocaine|ketamine|LSD|MDMA)(2|14)', d)]
        assert len(desc) == 1
        rows.append(dict(gsm=r['gsm'], drug=drug, day=day, replicate=replicate,
                         matrix_sample=desc[0], critical_period=state, state=int(state == 'open'),
                         condition=f'{drug}_{day}', title=r['title'], tissue=c['tissue'],
                         strain=c['strain'], sex='male (series protocol)',
                         age='P98-P112 (range only)', rna_isolation_batch='unknown',
                         num_slices='unknown', RNA_extraction_order='unknown',
                         concentration='unknown', individual_behavior='not available',
                         metadata_source='GSE230679_family.soft.gz; title + characteristics + description',
                         state_source='PMC10284704 ECM section; GEO critical-period characteristic',
                         characteristics_json=json.dumps(c, sort_keys=True)))
    meta = pd.DataFrame(rows)
    assert not meta.duplicated(['drug', 'day', 'replicate']).any()
    assert not meta.matrix_sample.duplicated().any()
    with gzip.open(DATA / TPM, 'rt') as f:
        columns = f.readline().strip().split('\t')
    # Column names have a sample identifier, NOT a replicate number. SOFT explicitly
    # maps that identifier to a replicate. Never interpret matrix column position.
    by_name = meta.set_index('matrix_sample')
    matrix_keys = []
    for name in columns:
        _, drug, day = re.fullmatch(r'(\d+)(saline|cocaine|ketamine|LSD|MDMA)(2|14)', name).groups()
        row = by_name.loc[name]
        assert drug == row.drug and int(day) == row.day
        matrix_keys.append(dict(drug=drug, day=int(day), replicate=int(row.replicate), matrix_name=name))
    joined = pd.DataFrame(matrix_keys).merge(meta, on=['drug', 'day', 'replicate'], validate='one_to_one')
    assert (joined.matrix_name == joined.matrix_sample).all()
    assert set(columns) == set(meta.matrix_sample) and len(joined) == 27
    assert (joined.groupby('condition').size() == 3).all()
    joined.drop(columns='matrix_name').sort_values(['drug', 'day', 'replicate']).to_csv(
        ROOT / 'samples.tsv', sep='\t', index=False)
    print('Wrote samples.tsv: 27 one-to-one joins, 9 conditions, missing batch retained as unknown.')


if __name__ == '__main__':
    prepare()
