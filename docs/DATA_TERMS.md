# Source attribution and data terms

The MIT license covers original code and original documentation. It does not grant additional rights to downloaded data, source-derived tables, author code or reproduced source text. Anonymous access is not a redistribution license.

The terms below were recorded with the source snapshots. They are not a comprehensive legal review. Check each source's applicable terms before redistributing derived tables or using them commercially. Do not treat every result table as MIT-licensed data.

## Core sources

| Source | Attribution | Recorded restriction or scope |
| --- | --- | --- |
| Lee 2018 cognitive performance and EA3 supplement | `10.1038/s41588-018-0147-3`, GWAS Catalog GCST006572 | Catalog/EMBL-EBI and publisher terms apply. EA3 is a separate proxy. SSGAC/EA4 data were not accessed or redistributed. |
| Savage 2018 intelligence | `10.1038/s41588-018-0152-6`, CNCR | Recorded as noncommercial CC BY-NC-SA 4.0, with no re-identification or stigmatizing use. |
| Genebass | Karczewski et al. 2022, `10.1016/j.xgen.2022.100168` | Archived browser terms identify CC BY 4.0 and request attribution to the paper and UK Biobank applications 26041/48511. Browser summaries, not participant records. |
| Unknome | Rocha et al. 2023, `10.1371/journal.pbio.3002222`, 18 March 2026 snapshot | Recorded CC BY 4.0. |
| Pharos/TCRD | Pharos 4.0 canonical proteins, May 2026 release | Retain release attribution and check its source terms. |
| gnomAD | v4.1 constraint metrics | Retain source attribution and check applicable data terms. |
| HGNC, GENCODE, NCBI | HGNC complete set, GENCODE v19, gene2pubmed | Retain attribution and applicable source terms. |

Snapshot URLs and hashes are in `derived/fetch-manifest.json`. HGNC uses the changing complete-set URL. The original literature and VEP pins are retained. The generated source excerpts are not distributed in this tree. The core and Route 2 commands regenerate them at ignored `derived/source-method-excerpts.txt` and `experiments/route2/source-method-excerpts.txt`.

## Experiment sources

Route 1 uses Nardou et al. 2023 (`10.1038/s41586-023-06204-3`), GEO GSE230679 processed data, and author analysis code pinned to `5e51f9d9e4e0b196e8d64134b7605b3f12902787`. The stored provenance includes author-code snapshots from the original audit. Preparation retrieves the three GEO model inputs, the paper XML and the pinned author-code snapshots. Author code is not distributed as original code here. Its missing local metadata and cached objects prevent full reproduction of the original inference. See the Route 1 provenance table and README for source access.

Route 2 also uses 1000 Genomes phase 3 (`10.1038/nature15393`), CNCR's EUR reference, HPA (`10.1126/science.1260419`), GTEx v8 (`10.1126/science.aaz1776`), eQTL Catalogue (`10.1038/s41588-021-00924-w`), coloc (`10.1371/journal.pgen.1004383`), Ensembl/VEP, UCSC and Tian 2019 (`10.1016/j.neuron.2019.07.014`). The recorded eQTL Catalogue and HPA terms are CC BY 4.0. HPA retains third-party constraints. CNCR noncommercial/share-alike restrictions still apply. Consult `experiments/route2/observed-access-notes.md` and its inventories for the actual access boundaries.

## Before public release

Review whether each retained source-derived table can be redistributed under its source terms, including share-alike obligations and publisher supplement restrictions. This tree does not establish unrestricted redistribution permission. History privacy review is separate from current-tree cleanup. No original-code license supersedes source restrictions.
