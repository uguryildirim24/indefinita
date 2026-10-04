# Cognition-gene data layer

Local, reproducible preparation for Project 1 in [`research/drylab-routes.md`](research/drylab-routes.md). **All outputs are hypothesis lists, not findings or intervention targets.** No individual-level data, cloud jobs, drug design or experiments are involved.

## Run

From this repository on Rolf's MacBook, with `uv` installed:

```sh
uv sync --frozen
uv run --frozen python scripts/pipeline.py
```

No account, institutional application, billing project or browser interaction is needed for the selected inputs. The first run fetches about **2.447 GB**; later runs verify and reuse the exact cached bytes. Downloaded data and response snapshots stay in ignored `data/`. The downloader enforces the requested **20 GB decimal** budget, including partial files and existing files in that directory. Do not run two pipeline instances against the same directory.

`derived/fetch-manifest.json` records requested/final URLs, observation time, HTTP status, exact response size, SHA-256, ETag and Last-Modified where available. `derived/access-inventory.tsv` is the readable inventory. Checksums cover the saved response bytes (including Genebass's gzip JSON), not decompressed content. Savage's publisher MD5 is checked as well. All committed derived files are below 5 MB; no raw input is committed.

The committed manifest also pins clean refetches. If a required live resource changes, the new response is retained and analysis stops rather than silently claiming to reproduce this snapshot. Cached observations keep their original observation times: a cached run is not a new network access check. The script prints failures and preserves error responses in the inventory; HTTP 200 alone does not mean access to a portal's underlying dataset.

## First result — 2026-10-04

**No gene meets both direct-cognition common-variant evidence and the selected rare-variant criteria.** The strict `cognition-hypotheses.tsv` therefore has a header and zero rows. This is a result of this particular mapping/data scope, not evidence that convergence does not exist. A nonempty direct-cognition shortlist is **not established**.

The evidence ledger covers **1,339 genes**, including 1,332 with common-variant support and seven genes with a rare p-value crossing a paper threshold before QC. Four rare genes pass the implemented QC: ADAMTS6, KDM5B, NACC1 and the source identifier AC011448.1 (ENSG00000258674). None is in the direct common-variant set. ANKRD12, ASAP1 and BRPF1 cross a rare p-value threshold but fail the paper's expected-allele-count minimum of 50; they are not promoted into the shortlist.

A **separate educational-attainment proxy** table has KDM5B and NACC1 (three association rows). It uses published EA3 gene results from Lee 2018, **not cognitive-performance gene results** and not inaccessible EA4. KDM5B is Pharos Tchem with 253 human gene2pubmed publications; NACC1 is Tbio with 124. Neither is Tdark. This proxy table does not satisfy the stronger direct-cognition convergence claim.

### Outputs

| File in `derived/` | Meaning |
|---|---|
| `cognition-hypotheses.tsv` | Strict direct-cognition intersection; empty in this snapshot |
| `gene-evidence.tsv` | Joined evidence ledger; explicit common/rare significance flags; nonsignificant rare scores do not count as convergence |
| `rare-threshold-audit.tsv` | Every rare threshold-crossing row, including QC failures and all three masks |
| `ea-proxy-hypotheses.tsv` | Separately labelled EA3 proxy intersection; hypothesis only |
| `knownness-ranks.tsv` | Unknome-derived ranks for 19,271 uniquely HGNC-mapped human genes |
| `genebass-coverage.tsv` | Exact phenotype, mask, sample size, fetched row count and phenotype-QC flags |
| `mapping-issues.tsv` | Ambiguous HGNC IDs, missing historical Entrez mappings and unmapped evidence IDs; no guessed symbols |
| `analysis-summary.json` | Source thresholds and coverage/result counts |
| `source-method-excerpts.txt` | Lee MAGMA methods and Savage S15 threshold note (text preserved; trailing extraction whitespace removed) |
| `access-inventory.tsv`, `fetch-manifest.json` | Observed access, sizes, checksums and URLs |

For genes without Unknome coverage, a literature-count rank is supplied when an unambiguous HGNC Entrez mapping exists. Unknome covers 1,050 ledger genes and literature ranks cover 1,195. `NA` annotations/ranks mean unavailable, **not unknown biology or zero knownness**. A gene without a unique HGNC match retains its Ensembl identifier; a missing canonical constraint row is not imputed.

## Exact mappings and thresholds

### Common variants

* **Lee 2018 cognitive performance**, GCST006572: all 10,098,325 SNP rows fetched from the Catalog; 13,714 have `Pval < 5e-8`, the threshold in Supplementary Table 13. Positions are used as GRCh37, consistent with the study's build and same-rsID positions in the GRCh37 Savage file. No liftover is performed.
* **Savage 2018 intelligence**: all 9,295,118 SNP rows fetched from the public CNCR share; 12,110 have `P < 5e-8`. GRCh37 is explicitly documented in the downloaded source README.
* Significant SNPs from either study are mapped to **overlapping GENCODE v19 GRCh37 gene bodies**, inclusive start/end, with **no flanking window**. All overlapping genes are kept; no nearest-gene assignment, LD expansion, fine-mapping or causal assignment is claimed. This is a transparent positional hypothesis mapping, **not a rerun of MAGMA or the papers' complete FUMA mapping**. The SNP threshold is the papers' threshold; the body-only mapping is our conservative mapping choice, not a source-defined statistical test of the gene.
* Also use Savage Supplementary **S15** published MAGMA results: `P < 2.76e-6` (paper's Bonferroni threshold for 18,128 genes). Map historical integer Entrez IDs through the downloaded current HGNC table to unambiguous Ensembl gene IDs. Preserve missing mappings in `mapping-issues.tsv`.
* Also retain published Savage **S12** FUMA positional/eQTL/chromatin assignments from genome-wide-significant loci, without inventing a new eQTL threshold. The mapping type and source minimum GWAS p-value are retained. Loci 8, 40, 66, 82, 124, 134, 197 and 200 flagged low-confidence in S7 are excluded from S12 if they are the gene's only mapped loci, and from our Savage SNP-body mapping using the S5 locus intervals. Published S15 MAGMA results are a distinct gene test and remain as reported.
* Ensembl **gene** IDs (version suffix removed) are the join key. No coordinate join is made to the GRCh38 Genebass positions.

### Rare variants

Use the anonymous API underlying the current Genebass browser, not its requester-pays Hail MatrixTable. The archived UI JavaScript identifies the API base and version `0.13.0-43c83cc-202402232123`. Retrieve every gene row returned by `gene-manhattan`, not just plotted top hits or per-gene searches.

All four **continuous phenotypes in the browser metadata's Cognitive function categories** are included:

* 20016: assessment-centre fluid intelligence, N=128,302;
* 20018: prospective memory result, N=131,007;
* 20023: mean time to correctly identify matches (reaction time), N=392,194;
* 20191: online fluid intelligence, N=100,900.

Masks are `pLoF`, `missense|LC`, and `pLoF|missense|LC`. `LC` includes low-confidence loss-of-function calls, so the missense mask is not exclusively missense. The paper's grouping uses MAF ≤1%. Synonymous masks are not taken as protein-altering evidence. Categorical attempted-test participation is not performance and is excluded. An additional custom fluid-intelligence variable exists without a description/category and is not interpreted here. Other cognitive domains absent from these metadata are not established as covered. These phenotypes, masks, and the common GWAS overlap in participants; they are **not independent replications**.

Thresholds come from Karczewski et al. 2022, DOI `10.1016/j.xgen.2022.100168`:

* **SKAT-O `Pvalue < 2.5e-7`**, or **burden `Pvalue_Burden < 6.7e-7`**. SKAT p-values are retained raw but not used to select a hit. These are empirical per-phenotype thresholds, not a correction over this entire joint search.
* Require source coverage and variant-count flags: at least 20× coverage and at least two variants.
* Calculate expected allele count as source `CAF × n_cases` (N with defined values for these continuous traits); require **≥50**.
* For the qualifying test require source synonymous gene lambda GC **≥0.75**, the paper's lower bound, and a passing source phenotype-QC flag. The latter is available only as a boolean in the endpoint. The browser flags also apply a gene lambda upper bound of 1.5; those flags are preserved separately, not mislabelled as a paper threshold.

**QC limitation:** the gene-Manhattan endpoint does not expose standard errors, so the paper's SE=0 exclusion cannot be independently repeated. Raw variant/carrier checks are not possible from these endpoints either. These are browser-summary hypotheses passing the implemented filters, not a claim to recreate every paper QC operation. Each pLoF/missense/combined association is retained in the audit. A single representative rare row in the main ledger is selected from qualifying rows if present, otherwise by the lowest available p-value; it is not a new combined significance statistic.

### Knownness and constraint

* **Unknome 18 March 2026** protein table: retain taxon 9606, join UniProt accessions to unique approved HGNC Ensembl IDs. The published score is already the maximum weighted GO knowledge over an orthologue cluster. Across matched proteins of a human gene, take the **maximum** score (conservative against calling a gene poorly known). Rank all 19,271 mapped human genes ascending, with competition ranks for ties (`1 + number with a lower score`). No invented dark-gene cutoff is applied.
* **Pharos 4.0 canonical proteins**, May 2026 release: join `ncbi_id` through HGNC, retaining all canonical-protein TDL labels and accessions. The CSV's `ensembl_id` column actually contains **ENSP protein IDs**, not ENSG gene IDs, and is not used as a gene key. Tdark remains the source category, not a label assigned from our counts.
* **NCBI gene2pubmed**: taxon 9606 only; count unique PMIDs per Entrez gene across all literature, not just neuroscience. Rank across current, uniquely HGNC-mapped Ensembl genes with an Entrez ID, least-published first; ties share rank. A mapped gene absent from this file has zero links in this snapshot, not necessarily zero publications in reality. No text-mining score is invented.
* **gnomAD v4.1**: retain canonical **Ensembl** transcript rows and report source LOF observed/expected upper bounds and flags. The file also contains RefSeq/Entrez rows; those are not mistaken for Ensembl rows. Constraint is annotation only: it is **not cognition association evidence**, and there is no invented constraint cutoff.

## Access actually observed and differences from the research report

Every response below was checked by anonymous GET on 2026-10-04; exact dates/bytes/hashes are in the inventory.

| Resource | Observed status / action |
|---|---|
| Catalog GCST006572 | 200; downloaded original `GWAS_CP_all.txt`, **601,075,032 bytes**. No account required. |
| CNCR Savage share | Public share redirects from `vu.data.surfsara.nl` to `vu.data.surf.nl`; 200 file GET, **1,254,191,070 bytes**, plus README and publisher checksum. Research report had only opened the share page; actual files now verified. |
| Published supplements | Savage XLSX **7,366,575 bytes**; Lee XLSX **3,453,892 bytes**; Lee methods PDF **6,648,378 bytes**, all 200. Lee's published MAGMA table is EA3, not cognitive performance: kept separate. |
| Genebass bulk | **400**, body explicitly says requester-pays and no user project. No billing project or Hail bulk compute used. |
| Genebass browser API | **200**, all selected phenotype/mask tables and QC tables downloaded anonymously, roughly 1–2 MB each. This usable small-data path was not established in the research report. |
| gnomAD v4.1 | 200; **95,546,041 bytes**. Mixed Ensembl and RefSeq IDs require explicit selection. |
| Unknome | 200; pinned dated protein table, **59,959,093 bytes**. No 5.9 GiB SQLite download needed. |
| Pharos canonical proteins | 200 with browser user-agent; **44,614,999 bytes**. ENSP-versus-ENSG column mismatch handled as above. |
| gene2pubmed | 200; **288,318,983 bytes**. Human links filtered while streaming. |
| HGNC / GENCODE | 200; mapping inputs **16,963,116 / 37,991,892 bytes**. Historical/ambiguous identifiers are listed, not guessed. |
| SSGAC / EA4 | 200 **login page**, not a data file. Registration/accepted terms required; no sign-up attempted. **EA4 skipped.** Publicly published EA3 gene scores are an explicitly labelled proxy, not an EA4 substitute. |
| SCHEMA | 200 JavaScript shell; downloadable table **not established**. No schizophrenia results substituted for cognition. |
| MetaBrain | 200 homepage links to name/email/institute/use form and emailed download link; not submitted. eQTL analysis deferred. |
| GTEx | 200 anonymous bucket listing includes bulk-qtl v10/v11. Actual brain eQTL files not fetched; colocalization deferred. |
| ABC Atlas | 200 anonymous release listing: 17 releases, latest 20260711. Expression matrices not fetched. Siletti/Census coverage not rechecked in this lane. |
| 1000 Genomes / MAGMA | 200 CNCR download page; data-file access not established here. No new MAGMA, LD, PoPS or fine-mapping run; published gene results and body mappings suffice for this first join. |

No selected summary dataset needed an institution. UK Biobank individual records, ABCD, All of Us and controlled PsychENCODE are outside this fetch and their institutional access was **not rechecked**. neXtProt is not used. Contextual expression/eQTL/LD work remains deferred, not completed Project 1 coverage.

## Source use and limits

Cite Lee et al. 2018 (`10.1038/s41588-018-0147-3`), Savage et al. 2018 (`10.1038/s41588-018-0152-6`), Karczewski et al. 2022 (above), gnomAD, HGNC, GENCODE v19, Rocha et al. 2023 Unknome (`10.1371/journal.pbio.3002222`), Pharos/TCRD 4.0 and NCBI when reusing these tables. CNCR data are for non-commercial use under CC BY-NC-SA 4.0 with no re-identification or stigmatizing use. Unknome is CC BY 4.0. Genebass's archived browser terms identify CC BY 4.0 and request attribution to the paper and UK Biobank applications 26041/48511. SSGAC data were not accessed or redistributed. A resource being anonymously downloadable does not remove its terms.

Population/indirect genetic effects, annotation bias, ancestry limits and gene-mapping uncertainty remain. These tables establish neither causation, direction of a useful perturbation, cognition enhancement nor a biological mechanism. No intervention or wet-lab experiment has been launched.
