# Core join methods

These are positional and published-summary hypothesis mappings. They do not identify causal genes. See `derived/analysis-summary.json` for the stored thresholds and counts, and `derived/fetch-manifest.json` for snapshot checksums and source URLs.

## Common variants

- Lee 2018 cognitive performance, GCST006572: all 10,098,325 SNP rows from the Catalog. There are 13,714 with `Pval < 5e-8`, the Supplementary Table 13 threshold. Positions are treated as GRCh37, consistent with the study build and matching rsID positions in Savage's GRCh37 file. No liftover is performed in the core join.
- Savage 2018 intelligence: all 9,295,118 SNP rows from the CNCR share. There are 12,110 with `P < 5e-8`. The source README explicitly identifies GRCh37.
- Significant SNPs map to overlapping GENCODE v19 GRCh37 gene bodies, inclusive start/end, without a flanking window. All overlapping genes are retained. This is not nearest-gene assignment, LD expansion, fine-mapping, a MAGMA rerun or complete FUMA mapping. The body-only mapping is an analysis choice, not a source-defined gene test.
- Savage S15 supplies published MAGMA results with `P < 2.76e-6`, the paper's Bonferroni threshold for 18,128 genes. Historical integer Entrez IDs map through the pinned HGNC snapshot to unambiguous Ensembl gene IDs. Missing mappings remain in `mapping-issues.tsv`.
- Savage S12 supplies published FUMA positional/eQTL/chromatin assignments. Mapping types and minimum source GWAS p-values are retained, without a new eQTL threshold. Low-confidence loci 8, 40, 66, 82, 124, 134, 197 and 200 from S7 are excluded from S12 when they are a gene's only mapped loci. Their S5 intervals are also excluded from the Savage SNP-body mapping. S15 is a separate gene test and remains as reported.
- Ensembl gene IDs without version suffixes are the join key. No coordinate join is made to GRCh38 Genebass positions.

## Rare variants

The anonymous Genebass browser API supplies every returned `gene-manhattan` row, not just top plotted hits. The archived UI identifies API version `0.13.0-43c83cc-202402232123`. The requester-pays Hail MatrixTable is not used.

All four continuous phenotypes in the browser metadata's Cognitive function categories are included:

| ID | Phenotype | N |
| --- | --- | ---: |
| 20016 | Assessment-centre fluid intelligence | 128,302 |
| 20018 | Prospective memory result | 131,007 |
| 20023 | Reaction time, mean time to correctly identify matches | 392,194 |
| 20191 | Online fluid intelligence | 100,900 |

Masks are `pLoF`, `missense|LC` and `pLoF|missense|LC`. LC includes low-confidence loss-of-function calls, so the missense mask is not exclusively missense. The paper's grouping uses MAF <=1%. Synonymous masks are not protein-altering evidence. Categorical test participation is not performance and is excluded. A custom fluid-intelligence variable lacks a description/category and is not interpreted. Coverage of other cognitive domains is not established. These phenotypes, masks and common GWAS overlap in participants, so they are not independent replications.

Karczewski et al. 2022 (`10.1016/j.xgen.2022.100168`) supplies the thresholds:

- SKAT-O `Pvalue < 2.5e-7`, or burden `Pvalue_Burden < 6.7e-7`. SKAT values are retained but do not select hits. These are empirical per-phenotype thresholds, not a correction over the whole joint search.
- Source coverage and variant-count flags must pass: at least 20x coverage and at least two variants.
- Expected allele count is source `CAF * n_cases`, using N with defined values for continuous traits. Require >=50.
- For the qualifying test require source synonymous gene lambda GC >=0.75 and a passing phenotype-QC boolean. Browser gene flags also impose an upper lambda bound of 1.5. Those flags remain separate rather than being called paper thresholds.

The gene-Manhattan endpoint does not expose standard errors. The paper's SE=0 exclusion cannot be independently repeated. Raw variant/carrier checks are also unavailable. Each mask association remains in the threshold audit. The main ledger chooses one qualifying rare row if present, otherwise the row with the lowest available p-value. This representative row is not a combined significance statistic.

The educational-attainment table uses published EA3 gene scores from Lee 2018 at FDR <0.05. These are not cognitive-performance gene results or inaccessible EA4 data. EA rows are kept separate from the direct-cognition intersection.

## Knownness and constraint

- Unknome 18 March 2026: retain taxon 9606 and join UniProt accessions to unique approved HGNC Ensembl IDs. The published score is maximum weighted GO knowledge over an orthologue cluster. Take the maximum score across matched proteins of each human gene. Rank all 19,271 mapped human genes ascending, with competition ranks for ties (`1 + number with a lower score`). No dark-gene cutoff is invented.
- Pharos 4.0 canonical proteins, May 2026 release: join `ncbi_id` through HGNC, retaining all canonical-protein TDL labels and accessions. Its `ensembl_id` column contains ENSP protein IDs, not ENSG gene IDs, and is not used as a gene key. Tdark is a source category.
- NCBI gene2pubmed: taxon 9606 only, unique PMIDs per Entrez gene across all literature. Rank uniquely HGNC-mapped Ensembl genes with an Entrez ID, least-published first. A mapped gene absent from this file has zero links in this snapshot, not necessarily zero publications in reality.
- gnomAD v4.1: retain canonical Ensembl transcript rows and report source LOF observed/expected upper bounds and flags. RefSeq/Entrez rows are not treated as Ensembl rows. Constraint is annotation, not cognition association evidence. No constraint cutoff selects genes.

Unknome covers 1,050 ledger genes and literature ranks cover 1,195. Missing annotations mean unavailable, not unknown biology or zero knownness. Ambiguous identifiers are not guessed. A missing canonical constraint row is not imputed.

## Access and reproduction boundaries

The stored core snapshot is from October 4, 2026. Its inventory totals 2,446,651,938 bytes, including access snapshots and error bodies. The manifest records requested/final URLs, timestamps, status, sizes, SHA-256 and response headers where available. Genebass `payload_sha256` hashes decoded JSON because its gzip timestamp can change without changing data. Savage's publisher MD5 is checked in addition to SHA-256.

HGNC and NCBI gene2pubmed use changing source URLs. The original source pins and literature annotations are retained. No pin refresh is part of this cleanup.

The downloader reads and rewrites `derived/fetch-manifest.json`. A changed successful response records its previous expected hash. The join rejects changed or unavailable required inputs and checks local raw-byte hashes. Cached responses retain their original observation times. An HTTP 200 login page or JavaScript shell is not dataset access.

EA4 registration was not attempted. SCHEMA table access was not established and schizophrenia results were not substituted for cognition. MetaBrain registration was not submitted. The core join downloaded GTEx bucket metadata and ABC Atlas release metadata only, not expression or eQTL matrices. It performed no new LD, MAGMA, PoPS or fine-mapping. Route 2's separate LD/QTL pilot is documented in its README.

Population and indirect genetic effects, ancestry limits, annotation bias and uncertain gene mapping remain. No intervention, individual-level analysis or wet-lab experiment is part of the core join.
