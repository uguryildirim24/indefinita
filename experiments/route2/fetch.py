"""Anonymous inputs for Route 2; reuse the repository downloader and audit format."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import fetch as core

HERE = Path(__file__).resolve().parent
core.DATA = HERE / 'data'
core.OUT = HERE
SOURCES = {
    'eur.zip': 'https://vu.data.surf.nl/index.php/s/VZNByNwpD8qqINe/download',
    'hpa-expression-oldpath.zip': 'https://www.proteinatlas.org/download/rna_tissue_consensus.tsv.zip',
    'hpa-expression-v25.zip': 'https://www.proteinatlas.org/download/tsv/rna_tissue_consensus.tsv.zip',
    'hpa-download.html': 'https://www.proteinatlas.org/about/download',
    'hpa-license.html': 'https://www.proteinatlas.org/about/licence',
    'catalog-original-index.html': 'https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST006001-GCST007000/GCST006572/',
    'catalog-harmonized-index.html': 'https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST006001-GCST007000/GCST006572/harmonised/',
    'catalog-harmonization.yaml': 'https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST006001-GCST007000/GCST006572/harmonised/30038396-GCST006572-EFO_0008354.h.tsv.gz-meta.yaml',
    'catalog-harmonization-readme.txt': 'https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST006001-GCST007000/GCST006572/harmonised/readme.txt',
    'ebi-terms.html': 'https://www.ebi.ac.uk/about/terms-of-use/',
    'catalog-study.json': 'https://www.ebi.ac.uk/gwas/rest/api/v2/studies/GCST006572',
    'eqtl-resources.json': 'https://api.github.com/repos/eQTL-Catalogue/eQTL-Catalogue-resources/contents/data_tables',
    'eqtl-tabix.json': 'https://api.github.com/repos/eQTL-Catalogue/eQTL-Catalogue-resources/contents/tabix',
    'eqtl-doc.html': 'https://www.ebi.ac.uk/eqtl/Studies/',
    'eqtl-metadata.tsv': 'https://raw.githubusercontent.com/eQTL-Catalogue/eQTL-Catalogue-resources/master/data_tables/dataset_metadata_r7.tsv',
    'eqtl-paths.tsv': 'https://raw.githubusercontent.com/eQTL-Catalogue/eQTL-Catalogue-resources/master/tabix/tabix_ftp_paths.tsv',
    'eqtl-columns.md': 'https://raw.githubusercontent.com/eQTL-Catalogue/eQTL-Catalogue-resources/master/tabix/Columns.md',
    'eqtl-readme.md': 'https://raw.githubusercontent.com/eQTL-Catalogue/eQTL-Catalogue-resources/master/tabix/README.md',
    'eqtl-data-access.html': 'https://www.ebi.ac.uk/eqtl/Data_access/',
    'eqtl-license-current.html': 'https://www.ebi.ac.uk/eqtl/License/',
    'QTD000176.all.tsv.gz.tbi': 'https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/sumstats/QTS000015/QTD000176/QTD000176.all.tsv.gz.tbi',
    'vep-rs2352974.json': 'https://grch37.rest.ensembl.org/vep/human/id/rs2352974?content-type=application/json',
    'vep-rs1906252.json': 'https://grch37.rest.ensembl.org/vep/human/id/rs1906252?content-type=application/json',
    'vep-rs13107325.json': 'https://grch37.rest.ensembl.org/vep/human/id/rs13107325?content-type=application/json',
    'tian2019-primary.xlsx': 'https://pmc.ncbi.nlm.nih.gov/articles/instance/6813890/bin/NIHMS1535621-supplement-7.xlsx',
    'tian2019-validation.xlsx': 'https://pmc.ncbi.nlm.nih.gov/articles/instance/6813890/bin/NIHMS1535621-supplement-8.xlsx',
    'tian2019-pmc.html': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6813890/',
    'tian2019-oa.xml': 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC6813890',
    'tian2019-paper.xml': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6813890/fullTextXML',
    'tian2019-filelist.txt': 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE124nnn/GSE124703/suppl/filelist.txt',
    'tian2019.soft.gz': 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE124nnn/GSE124703/soft/GSE124703_family.soft.gz',
    'neuron-sgrna.txt.gz': 'https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM3543nnn/GSM3543624/suppl/GSM3543624_neuron_1_sgRNA_mapping.txt.gz',
    'hg19ToHg38.over.chain.gz': 'https://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz',
}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('names', nargs='*')
    a = p.parse_args()
    core.run({n: SOURCES[n] for n in a.names} if a.names else SOURCES)
