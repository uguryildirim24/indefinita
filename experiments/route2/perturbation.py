"""Audit neuronal screen coverage without interpreting RNA detection as perturbation."""
import csv
import gzip
import json
import zipfile
from collections import defaultdict
import openpyxl
from associate import HERE, rows, tsv, sha

DATA = HERE / 'data'


def main():
    manifest = {r['file']: r for r in json.loads((HERE / 'fetch-manifest.json').read_text())}
    pilots = [r for r in rows(HERE / 'locus-alternatives.tsv') if r['pilot'] == 'True']
    access = []
    for name in ['tian2019-primary.xlsx', 'tian2019-validation.xlsx']:
        m = manifest[name]
        valid = m['http_status'] == 200 and zipfile.is_zipfile(DATA / name)
        access.append(dict(file=name, http_status=m['http_status'], sha256=sha(DATA / name),
                           usable_excel=valid, access='XLSX archive available' if valid else 'HTML/browser challenge, not a usable screen table'))
    # Sequence-only CROP-seq mapping is actually accessible, but does not expose target genes.
    with gzip.open(DATA / 'neuron-sgrna.txt.gz', 'rt') as f:
        reader = csv.DictReader(f, delimiter='\t')
        header = reader.fieldnames
        guides = set()
        cells = set()
        count = 0
        for r in reader:
            guides.add(r['barcode'])
            cells.add(r['cell'])
            count += 1
    # Do not guess gene identities from guide sequences. The frozen run did not recover
    # the supplemental primary screen or gene-to-guide design map.
    if any(a['usable_excel'] for a in access):
        raise RuntimeError('Screen access changed: inspect source sheet semantics before claiming reproduced coverage')
    tsv('perturbation-coverage.tsv', [dict(region_id=g['region_id'], gene_id=g['gene_id'], symbol=g['symbol'],
         neuron_guide_coverage='not established; target mapping/primary phenotype table unavailable',
         readout='Tian 2019 iPSC-derived glutamatergic neuron survival D14/D21/D28; CROP-seq D7 transcription; not cognitive performance or mature adult physiology',
         source='GSE124703 / PMC6813890; accessible sequence-only guide map; supplemental XLSX requests returned HTML challenge',
         source_library_scope='H1 kinase/druggable genome 2325 genes; not unbiased whole-genome dark-gene screen',
         k562_evidence='not assessed or substituted; cancer-cell phenotype would not establish neuronal function',
         phenotype_result='unavailable, not a negative phenotype') for g in pilots])
    tsv('perturbation-access.tsv', access)
    summary = dict(sequence_mapping_header=header, sequence_mapping_rows=count, distinct_barcodes=len(guides), distinct_cell_barcodes=len(cells),
                   barcode_counts_are_not_validated_cells_or_gene_coverage=True,
                   candidate_genes_checked=len(pilots), candidate_gene_mapping_established=False,
                   no_expression_matrix_downloaded=True, no_neuronal_cognition_outcome=True,
                   paper='Tian et al. 2019 DOI 10.1016/j.neuron.2019.07.014; main HTML available; relevant screen/method passages inspected',
                   access=access)
    (HERE / 'perturbation-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
