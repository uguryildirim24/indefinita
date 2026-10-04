# Dry-lab discovery routes with open data

Checked 2026-10-04. Request q-1791090165681-74715-0, job-0003. Analysis and strategy only. No analysis was run and no dataset was downloaded.

## Verdict

Open data will not hand Rolf an large-scale discovery. Nothing I found gets from public data to a cognition mechanism without wet-lab work. What it can do cheaply is produce a short, ranked, falsifiable list of poorly characterized genes and cell types that several independent lines of genetic evidence tie to cognition. Someone with a lab can then test that list.

The route that best fits "biology nobody has described yet" is Project 1 in section 5: take genes implicated in cognition by common-variant and rare-variant genetics, join them to "knownness" rankings (Unknome, Pharos Tdark, literature counts), and keep the ones nobody has studied. Projects 3 and 4 strengthen that list. The cell-type and brain-structure projects (2 and 5) say where to look, not what is there.

Most of the data is open right now. Several resources need only a free sign-up (SSGAC, MetaBrain, OpenGWAS, MICrONS, HCP open tier). The big cohort resources need an institution: UK Biobank, ABCD, All of Us controlled tier, PsychENCODE individual-level data. Rolf will likely need a supervisor for those.

On timing: in the seven cases I checked, the step from computational finding to a confirmed mechanism took anywhere from inside the same paper to about 8 years (FTO), and about 9.5 years before a human cell model existed for C4. Every one needed experiments. For cognition itself I found no GWAS locus with a confirmed single-gene mechanism. That is "not established", not proof of absence.

Several resources differ from what older papers and tutorials say: neXtProt is closed, OpenGWAS needs a token since May 2024, the GWAS Catalog's legacy API is deprecated, ABCD moved off NDA, and PsychENCODE moved off Synapse. The table says what I saw.

## How I checked

I used HTTP HEAD requests, public-bucket and FTP listings, API metadata, and page reads. I opened index pages and small documentation pages. I downloaded no data files. Access labels:

- **Open**: anonymous download works, no account.
- **Open, free sign-up**: free account or accepted terms, no review.
- **Application**: reviewed, institutional or committee-gated.
- **Not verified**: I could not open the primary page; the status comes from search summaries and is marked.

Many portals are JavaScript shells that returned only a page title to my fetcher (gnomAD downloads, GTEx, Genebass, SCHEMA, Open Targets downloads, NDA). For those I used bucket listings, the papers, or docs pages instead and say so. Section "Could not open" at the end lists the gaps.

## 1. Datasets

| Group | Resource | URL | Access | What I saw |
|---|---|---|---|---|
| Common-variant cognition GWAS | GWAS Catalog summary statistics | https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/ (browse https://www.ebi.ac.uk/gwas/) | **Open**, but the headline cognition studies are missing | FTP index answers. Via the v2 API: cognitive performance (Lee 2018, N=257,841, GCST006572) has a summary-statistics link. Educational attainment EA3 (GCST006442), EA4 (GCST90105038, GCST90105039) and general cognitive ability (Davies 2018, GCST006269) show full summary statistics as "NA". The legacy v1 REST API is deprecated and rate-limited; v2 base is https://www.ebi.ac.uk/gwas/rest/api/v2/. The docs page I read states CC BY 4.0 for the documentation, not the data. |
| Common-variant cognition GWAS | SSGAC data portal | https://thessgac.com/ (home: https://www.thessgac.org/) | **Open, free sign-up** | Portal shows a login and a registration form. Terms: no re-sharing, even with co-authors; keep data confidential; no re-identification. The file list is behind login, so I did not see which EA4 or cognitive-performance files it serves. |
| Common-variant cognition GWAS | CTG-CNCR summary statistics | https://cncr.nl/research/summary_statistics/ | **Open**, non-commercial | Lists Savage 2018 intelligence (N=269,867), an earlier 78,308-person intelligence GWAS, brain volume, functional connectivity and more. CC BY-NC-SA 4.0, no re-identification, no stigmatizing use; commercial use needs permission. The Savage 2018 download link is a public share page (vu.data.surf.nl, folder "Savage_2018") that loaded with no password prompt; I did not list or download files. Only the 2026 Alzheimer's entry says to enter a directory code. |
| Common-variant cognition GWAS | IEU OpenGWAS | https://opengwas.io/ (API https://api.opengwas.io) | **Open, free sign-in** | Since 1 May 2024 every request needs a token, "even if you are querying a public dataset", and costs come out of a periodic allowance (OpenGWAS blog). I did not test the allowance size. |
| Common-variant cognition GWAS | Psychiatric Genomics Consortium | https://pgc.unc.edu/for-researchers/download-results/ | **Open** for most; request form for some | Page: "Use of these data is NOT unrestricted": research use only, no cross-posting, no identification, no predictive tests for unborn individuals. Suicide-attempt sets (sui2022, sui2023) go through a request form. Individual-level access has a separate portal I did not open. |
| Common-variant cognition GWAS | FinnGen R12 public results | https://r12.finngen.fi/ (bucket gs://finngen-public-data-r12) | **Open** | Anonymous bucket listing returns summary_stats/, finemap/, lof/, annotations/, ld_matrix/, meta_analysis/. A finngen-public-data-r13 bucket also lists. I did not read the site's terms. |
| Brain imaging genetics | ENIGMA GWAS results | https://enigma.ini.usc.edu/research/download-enigma-gwas-results/ | **Open** per the page | Lists summary statistics for subcortical volumes, intracranial volume, hippocampal volume, cortical surface area and thickness. I did not test the downloads. |
| Rare-variant | gnomAD v4.1 | https://gnomad.broadinstitute.org/downloads (buckets gs://gcp-public-data--gnomad, s3 gnomad-public-us-east-1) | **Open** | release/4.1/constraint/gnomad.v4.1.constraint_metrics.tsv (95.5 MB, modified 2024-04-18) answers anonymously on both Google and AWS. Release folders listed run from 2.1 to 4.1.2. CC0 and the v4.1.0 size (730,947 exomes, 76,215 genomes) come from search summaries of gnomAD pages; the policies page rendered empty. The Azure copy was retired in August 2025 (gnomAD news). |
| Rare-variant | Genebass (UK Biobank exomes) | https://app.genebass.org/ | **Open**, browser plus bulk (bulk is requester-pays) | Karczewski 2022: all summary statistics "publicly available as bulk downloads and in a browser interface". 394,841 European-ancestry exomes, 4,529 phenotypes, 993,280,477 gene-level and 28,158,190,538 single-variant statistics. The Hail bucket gs://ukbb-exome-public is requester-pays: listing it without a billing project fails with "Bucket is a requester pays bucket". |
| Rare-variant | SCHEMA schizophrenia exomes | https://schema.broadinstitute.org/ | **Open** in browser; downloads not verified | Site answers but rendered only "Results Browser". Exome meta-analysis of 24,248 cases and 97,322 controls (PubMed abstract). The claim of downloadable gene and variant tables comes from a search summary only. Individual-level exomes not checked. |
| Cell and spatial atlases | Allen Brain Cell Atlas | https://brain-map.org/atlases-and-data/bkp/abc-atlas (bucket s3://allen-brain-cell-atlas) | **Open** | Anonymous S3 listing shows 17 dated releases, newest releases/20260711. Docs: "No account or login is required." Covers mouse whole-brain, human whole-brain and other sets. Licence wording not on the page I read. |
| Cell and spatial atlases | CELLxGENE Discover and Census | https://cellxgene.cziscience.com/ (https://census.cellxgene.cziscience.com/cellxgene-census/v1/release.json) | **Open** | release.json answers. Newest build listed is 2025-11-17 (stable 2025-11-08); nothing newer. Licences are per dataset, not checked. I did not check whether the Siletti 2023 human brain atlas (>3M nuclei, about 100 dissections, 3 donors, 461 clusters and 3,313 subclusters) is in Census. |
| Cell and spatial atlases | SEA-AD (Alzheimer's atlas) | https://sea-ad-single-cell-profiling.s3.us-west-2.amazonaws.com/ | **Open**, processed data | Anonymous listing; README modified 2026-06-23. 84-donor middle temporal gyrus atlas (Gabitto 2024). It is an Alzheimer's atlas, not a cognition one. Donor-level genotypes not checked. |
| Cell and spatial atlases | Human Protein Atlas | https://www.proteinatlas.org/about/download | **Open** | Version 25.1. Brain data: 13 regions and 193 subregions (HPA RNA), single-nucleus data for 11 regions with 260 clusters. Licence page: CC BY 4.0 for copyrightable parts; some integrated sources keep their own licence. |
| Expression and eQTL | GTEx | https://gtexportal.org/ (open bucket gs://adult-gtex) | **Open**, processed data; individual-level controlled, not re-verified | Portal pages rendered empty. The open bucket lists bulk-gex v10 and v11, bulk-qtl v10 and v11 (single-tissue cis-QTL and SuSiE fine-mapping), single-cell v9, long-read v9. The V8 median-expression file answers. V10: 19,788 RNA-seq samples, 946 donors, 54 tissues; V11 re-annotates V10 with GENCODE 47 and adds no samples (AnVIL and portal summaries via search). Individual-level data sit in dbGaP phs000424 (search summary). |
| Expression and eQTL | eQTL Catalogue | https://www.ebi.ac.uk/eqtl/ (https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/) | **Open** | FTP lists sumstats/, susie/, imported/ and r8_beta/ (sumstats and susie, modified 2026-09-09 and 2026-09-10). R8 looks like a beta release. |
| Expression and eQTL | MetaBrain | https://www.metabrain.nl/ | **Open, free sign-up** | Form asks name, email, institute and intended use; a link is emailed. Terms: no redistribution, no re-identification. Cortex cis-eQTL full summary statistics for European ancestry; trans and interaction eQTLs are in the paper's supplement. 8,613 RNA-seq samples from 14 datasets (PubMed abstract). |
| Expression and eQTL | PsychENCODE | https://www.psychencode.org/data | **Application** for most; summary tables open | Primary home is now the NIMH Data Archive; the Synapse transfer is complete. Most collections need a Data Access Request, quoted as about 10 business days. De-identified summary tables (expression matrices, QTLs, regulatory networks) are public on the consortium page. Emani 2024: more than 2.8M nuclei from 388 individuals. I did not open Synapse. |
| Gene prioritization | Open Targets Platform | https://platform.opentargets.org/downloads | **Open** | Docs licence page: CC0 1.0. The downloads page rendered empty, so I did not see the GWAS credible-set or locus-to-gene files; Mountjoy 2021 and Ochoa 2022 describe them. |
| Perturbation | Genome-wide Perturb-seq (Replogle 2022) | https://plus.figshare.com/articles/dataset/20029387 | **Open** | CC BY 4.0 (figshare API). K562 genome-wide pseudobulk 375 MB; K562 genome-wide single-cell 65.8 GB; RPE1 single-cell 8.7 GB; K562 essential-gene single-cell 10.7 GB. Targets genes expressed in those two cell lines. |
| Perturbation | DepMap | https://depmap.org/portal/download/ | **Open**, browser only | CC BY 4.0 from search summaries. My scripted request got a Cloudflare "Verification" page, so downloads need a browser. Cancer cell lines, not neurons. |
| Perturbation | BioGRID ORCS | https://orcs.thebiogrid.org/ (https://downloads.thebiogrid.org/BioGRID-ORCS/) | **Open** | Downloads page: "100% freely available" under the MIT License. Aggregates published CRISPR screens. |
| Perturbation | CRISPRbrain | https://crisprbrain.org/ | **Open** to browse; terms not verified | "Data Commons for functional genomics screens in differentiated human cell types": screens in iPSC-derived neurons and glia (Kampmann lab). No download terms or licence on the page I read. |
| Connectomes | FlyWire | https://codex.flywire.ai/ (https://zenodo.org/records/10676866) | **Open** | Zenodo record is CC BY 4.0 and open access (Zenodo API); v783 files include an 852 MB proofread-connections table and a 9.5 GB synapse table. Paper: Dorkenwald 2024. Codex lists FAFB v783 (139,255 neurons, 3,732,460 connections) plus BANC, MANC, MAOL and MCNS datasets; its server-side tools need a Google sign-in. |
| Connectomes | MICrONS | https://www.microns-explorer.org/ | **Open, free sign-up** | Connectivity queries need a CAVE token ("register as a user"); imagery and segmentation sit in BossDB buckets. Public versions 117 through 1300 (1300 dated 13 January 2025). Terms page not read. |
| Connectomes | H01 human cortex | https://h01-release.storage.googleapis.com/landing.html | **Open** | Public bucket listing works. 1.4 PB, about 1 mm³ of human temporal cortex. Paper (Shapson-Coe 2024): about 57,000 cells and 150 million synapses; the landing page says 183 million annotated synapses. |
| Behavior and imaging | UK Biobank | https://www.ukbiobank.ac.uk/ | **Application**, not verified | ukbiobank.ac.uk returned 403 to curl and to my page fetcher. Search summaries of its pages: registration plus application on the Access Management System, committee review, analysis on the Research Analysis Platform, £3,000 for three years in 2025-26, with support for students and early-career researchers. Whether an undergraduate can apply alone: not established. |
| Behavior and imaging | ABCD 6.0 | https://www.nbdc-datahub.org/data-access-process (https://docs.abcdstudy.org/v/6_0_0/usage/access.html) | **Application** | Data Use Certification through the NIH Brain Development Cohorts Data Hub. Needs an NIH-recognized institution with an active Federal Wide Assurance and a signing official; training score of at least 90%; access valid one year. NDA no longer takes new ABCD requests (search summary). |
| Behavior and imaging | HCP Young Adult | https://www.humanconnectome.org/study/hcp-young-adult/data-use-terms | **Open, free sign-up**, subject to local institutional rules; restricted tier by application | Open tier: ConnectomeDB account plus Open Access terms. Those terms say IRB or Ethics Committee approval may be needed under local rules; a free account is not blanket authorization to use participant data. Restricted tier (family structure, age by year, handedness) needs an application approved by a PI. |
| Behavior and imaging | OpenNeuro | https://openneuro.org/ (s3://openneuro.org) | **Open** | Anonymous S3 listing and file request worked (ds000001 onward). Licence is per dataset, not checked. |
| Behavior and imaging | All of Us | https://www.researchallofus.org/ | **Application**, not verified | Search summaries only: the institution must hold a Data Use and Registration Agreement and a signing official; controlled tier adds requirements; access for independent researchers is described as coming after a beta period. |
| Understudied-gene rankings | Unknome | https://unknome.mrc-lmb.cam.ac.uk/ | **Open** | CC BY 4.0 for the database. Downloads: protein summary tables, orthologue cluster tables, full SQLite. Knownness score = largest GO-term count for any member of the protein's PANTHER orthologue cluster, with evidence weighting. |
| Understudied-gene rankings | Pharos / TCRD 4.0 | https://pharos.nih.gov/ (https://opendata.ncats.nih.gov/public/pharos/) | **Open** | Files listed: pharos400_tdls_canonicals.csv (44.6 MB, 20,654 canonical proteins) and pharos400_tdls_full.csv (87.2 MB), dated May 2026. Tdark = no qualifying drug or small-molecule activity and at least two of: PubMed text-mining score under 5, GeneRIF count 3 or fewer, antibody count 50 or fewer (readme). The site returned 403 to a bare curl and 200 with a browser user agent. |
| Understudied-gene rankings | NCBI gene2pubmed | https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz | **Open** | 288 MB, modified 2026-10-03. Gives literature counts per gene. |
| Understudied-gene rankings | neXtProt | https://www.expasy.org/archives/nextprot | **Closed**, archived | Page: neXtProt "has reached its end of life and no longer provides data or services." Last release (September 2023) archived on Zenodo, DOI 10.5281/zenodo.14163587. Older advice to use its protein-existence levels no longer works live. |

Three points from the table matter for planning.

First, the best-known cognition GWAS (EA3, EA4, Davies) are not in the Catalog's open summary-statistics set. Cognitive performance (Lee 2018) is. Intelligence (Savage 2018) is on the CNCR site. EA3 and EA4 may be served through SSGAC's free sign-up, but I could not see the file list. Plan around Lee 2018 and Savage 2018 first.

Second, the unknown-gene rankings are all open and small. The perturbation data is open but only covers genes expressed in K562 and RPE1 cells, so many brain-specific genes are absent by design.

Third, the individual-level cohorts (UK Biobank, ABCD, All of Us controlled tier, most of PsychENCODE) are the ones that need an institution. A dry-lab plan that stays on summary statistics and atlases avoids that.

## 2. Methods

All of these start from a GWAS or exome summary table and add layers. None of them delivers causation alone. Repository activity below is from the GitHub API on 2026-10-04.

**Gene-level and gene-set tests.** MAGMA (de Leeuw 2015) collapses SNP p-values into gene p-values and tests gene sets. The current download is v1.10 (10/01/2022) under standard copyright (cncr.nl). FUMA (Watanabe 2017) wraps MAGMA plus eQTL and chromatin-interaction mapping as a free web service with registration; its tutorial page lists a 600 MB input limit and GRCh37 only. It can say which genes and pathways carry more signal than expected. It cannot say which gene at a locus is causal, because neighbouring genes share LD. It is also biased toward annotated genes, since gene sets are built from existing knowledge (Haynes 2018, Stoeger 2018). That bias makes dark genes hard to see by construction. This is my inference from those two papers.

**Locus-to-gene scoring.** PoPS (Weeks 2023; FinucaneLab/pops, last push 2025-07) scores genes by polygenic enrichment of gene features such as expression and networks. The Open Targets locus-to-gene model (Mountjoy 2021; opentargets/gentropy, active) is an open model that scores genes at each GWAS locus. The CNCR software page lists FLAMES for the same job; I did not read it. These rank candidate genes. They do not confirm one.

**Fine-mapping.** SuSiE (Wang 2020; stephenslab/susieR, active) and its summary-statistics version (Zou 2022) estimate credible sets of likely causal variants. LD score regression (Bulik-Sullivan 2015; bulik/ldsc, last push 2026-01) separates confounding from polygenicity, and the stratified version (Finucane 2015) partitions heritability across annotations. Fine-mapping narrows variants. It does not link a variant to a gene or a mechanism.

**Colocalization.** coloc (Giambartolomei 2014; chr1swallace/coloc, active) tests whether two association signals at a locus share one causal variant. The original assumes one causal variant per trait per locus; Wallace 2021 relaxes that using SuSiE. eCAVIAR (Hormozdiari 2016) is the older alternative. A positive result says the GWAS and expression signals plausibly share a variant. It does not say expression causes the trait. Two nearby causal variants, or pleiotropy, can look the same. Reference eQTLs come from adult postmortem bulk tissue and miss development and rarer cell types, so a negative result is weak evidence.

**Mendelian randomization.** TwoSampleMR and ieugwasr (Hemani 2018; MRCIEU, active) run inverse-variance, Egger, median and related estimators. MR-PRESSO (rondolab/MR-PRESSO) was last pushed in 2023. Burgess 2023 gives current guidelines and Skrivankova 2021 (STROBE-MR) gives reporting rules. MR can say a trait-to-trait association is consistent with a causal effect if its assumptions hold: the instrument predicts the exposure, shares no confounders with the outcome, and acts only through the exposure. It cannot prove those assumptions, and pleiotropy is the usual failure. For cognition and educational attainment there is a second problem: the EA4 abstract reports that direct effects explain roughly half of the polygenic index's association, and that mate-pair correlation is too large for phenotypic assortment alone. Within-sibship GWAS (Howe 2022) exist to reduce this bias. Cognition-exposure MR on population GWAS therefore carries indirect-effect and assortment confounding. SMR with the HEIDI test (Zhu 2016; yanglab SMR page answers) applies the idea to cis-eQTLs: it tests whether expression and trait share a signal and whether the association is heterogeneous across linked variants.

**Transcriptome-wide association.** PrediXcan and S-PrediXcan (Gamazon 2015; Barbeira 2018; hakyimlab/MetaXcan, active) and FUSION (Gusev 2016; gusevlab/fusion_twas) predict expression from genotype and test it against the trait. TWAS says which genes have expression correlated with the trait through genetic prediction. It does not say that expression causes the trait. Many genes share a locus and co-regulate, and Wainberg 2019 and Mancuso 2019 (FOCUS) discuss why a TWAS hit needs fine-mapping among neighbouring genes before it is a gene call.

**Cell-type enrichment.** MAGMA-celltyping (Skene 2018; neurogenomics/MAGMA_Celltyping, last push 2026-02), LDSC applied to specifically expressed genes (Finucane 2018), CELLECT (Timshel 2020; perslab/CELLECT, last push 2024-08), and scDRS (Zhang 2022; martinjzhang/scDRS, MIT, active) relate GWAS signal to cell types in an atlas. Bryois 2020 applied this to brain cell types. Savage 2018 found enrichment in striatal medium spiny neurons and hippocampal pyramidal neurons. These methods say which cell types' expression programs carry trait heritability. They cannot say that a given cell type causes the trait, and the answer depends on which regions and donors the atlas sampled. Siletti 2023 sampled three donors.

**Gene networks.** WGCNA (Langfelder 2008) and related coexpression and protein-interaction networks group genes by shared behaviour. MetaBrain used brain gene co-regulation networks to link GWAS loci and prioritize additional genes for five central nervous system diseases (de Klein 2023). Networks give guilt-by-association functional hypotheses. They do not give causal direction, and hub genes are over-represented because they are well studied. The useful finding for unknown genes: Pandey 2014 reported that brain "ignorome" genes do not differ from well-studied genes in coexpression connectivity, so coexpression neighbours can annotate them.

**Rare-variant burden tests.** REGENIE (Mbatchou 2021; rgcgithub/regenie, active) and similar gene-based tests collapse rare coding variants per gene; Genebass and SCHEMA are the public results. gnomAD constraint metrics (Karczewski 2020) show which genes tolerate loss-of-function variants. A coding rare-variant burden hit can point more directly at a gene than a typical noncoding common-variant locus. Common coding variants can also implicate a gene directly; neither type of association alone confirms a causal mechanism. It still needs experiments to give mechanism. Singh 2022 reported that the implicated genes include synaptic genes and that GRIN2A and GRIA3 support a glutamatergic hypothesis. That is a hypothesis about mechanism, not a test of it.

**Perturbation phenotypes.** Genome-wide Perturb-seq (Replogle 2022) uses transcriptional phenotypes to predict the function of poorly characterized genes. It says what a knockdown does to the transcriptome in K562 and RPE1 cells. It cannot say anything about cognition, and it only covers genes those lines express.

Putting these together: GWAS-based layers narrow where and which; colocalization, TWAS and MR add direction under assumptions; rare variants and perturbation are the nearest dry-lab analogues of an experiment and are still observational or cell-line-bound.

## 3. What this approach has produced

Cases below are hand-picked successes. They show the shape of the gap, not a typical value. Dates are from Crossref and PubMed records I checked. PCSK9 is kept to the genetics; drug development is left out on purpose.

- **FTO and obesity.** The FTO association was reported in 2007 (Frayling, Science, 11 May). Smemo 2014 (March) showed the obesity-associated FTO region contacts the IRX3 promoter and that obesity-associated SNPs track IRX3 expression, not FTO, in human brain. Claussnitzer 2015 (September) pinned the causal variant rs1421085, an ARID5B repressor motif, and a shift from thermogenic to energy-storing adipocytes, validated with patient samples, mice and CRISPR editing. Gap: about 7 years to the IRX3 link, about 8 to the variant-level mechanism. A 2021 Science paper (Sobreira) with "extensive pleiotropism and allelic heterogeneity" in its title shows the picture kept moving; I read only the title.
- **C4 and schizophrenia.** The MHC association was reported in July 2009 (three Nature papers: Shi, Stefansson, and the International Schizophrenia Consortium). Sekar 2016 (January) tied it to structurally varying alleles of C4 that raise C4A expression in brain, with C4 mediating synapse elimination in mice. Gap: about 6.5 years. Sellgren 2019 added a human iPSC model of increased microglial synapse engulfment (about 9.5 years from the first signal) and reported that the C4 variants "do not fully explain" the effect. Nobody had a gene story for the MHC signal before 2016, and the confirmed mechanism is still partial.
- **SORT1 and LDL cholesterol.** The 1p13 locus appeared in two Nature Genetics papers on 13 January 2008 (Kathiresan; Willer). Musunuru 2010 (August) showed rs12740374 creates a C/EBP binding site, changes hepatic SORT1 expression, and alters VLDL secretion in mouse liver. Gap: about 2.6 years. A 2012 JCI paper (Strong) titled "Hepatic sortilin regulates both apolipoprotein B secretion and LDL catabolism" suggests the first mechanism was refined; I read only the title.
- **TREM2 and Alzheimer's disease.** Guerreiro and Jonsson (both 10 January 2013) found the R47H variant. Homozygous loss of function was already linked to early-onset dementia, so TREM2 had a partial story. Keren-Shaul 2017 (June) used single-cell mapping to describe a disease-associated microglia state with a TREM2-dependent stage. Gap: about 4.4 years to a cell-state mechanism.
- **PCSK9 and LDL cholesterol.** Abifadel 2003 found PCSK9 through family linkage, not GWAS. Cohen 2006 showed loss-of-function carriers have low LDL and lower coronary risk. Gap: about 3 years to the protective human genetics. I did not verify the cell-biology mechanism dates.
- **Atlas-first: airway ionocytes.** Montoro 2018 and Plasschaert 2018 (both 1 August) used single-cell atlases to find a rare cell type that is the major source of CFTR transcripts, then validated in the same papers with lineage tracing, a Foxi1 knockout and electrophysiology. Gap: inside the paper. Clinical relevance in cystic fibrosis was left as a narrative.
- **Perturbation-first: INTS15.** Replogle 2022 used Perturb-seq phenotypes to predict function for poorly characterized genes, including C7orf26 in transcription. Offley 2023 (March) used proteomics and AlphaFold2 to identify INTS15 as an additional Integrator subunit, and a 2024 Nature paper (Fianu, April) gave a cryo-EM structure. A search summary names INTS15 as C7orf26; I did not read Offley's full text, so I can't say whether it cites the Perturb-seq paper. Gap: about 9 months from the Perturb-seq prediction (online June 2022) to biochemical identification, about 22 months to a structure.

So the spread runs from zero (atlas plus experiments in one paper) to about 8 years (FTO), with C4's human cellular confirmation near 9.5. Every case had experimental work: mouse knockouts, CRISPR editing, cell models, proteomics or cryo-EM. None finished in a computer. This list also has survivorship bias. The typical GWAS locus has no confirmed mechanism, and I did not measure what fraction does.

**Cognition specifically.** The scale of the findings is large and the biology is coarse. EA3 reported 1,271 independent significant SNPs (Lee 2018). EA4 reported 3,952 (Okbay 2022). Savage 2018 reported 205 loci and 1,016 genes for intelligence, with enrichment in striatal medium spiny neurons and hippocampal pyramidal neurons and in nervous-system development and synaptic structure pathways. Davies 2018 reported 148 loci and 709 genes. Those are enrichment-level insights. I did not find a cognition locus with a confirmed single-gene mechanism. The closest neighbours are schizophrenia (C4, and the SCHEMA exome genes GRIN2A and GRIA3 as a glutamatergic hypothesis) and Alzheimer's disease (TREM2).

## 4. Searching for unannotated biology

A candidate has to pass four filters in order. The aim is a ranked dossier, not a verdict.

1. **Genetic link to cognition.** Pool gene-level scores (MAGMA, PoPS, locus-to-gene) from Lee 2018, Savage 2018 and, if sign-up works, EA4; fine-mapped coding variants; Genebass burden results for cognitive phenotypes; and gnomAD constraint. Require more than one of these.
2. **Low knownness.** Score each gene on several independent rankings and keep the intersection, because each ranking has blind spots:
   - Unknome knownness score (Rocha 2023): the lowest-scoring human proteins. Rocha screened 260 conserved unknown genes in Drosophila by RNAi and validated a Notch-pathway component and two male-fertility genes with CRISPR.
   - Pharos Tdark (Sheils 2021; Kelleher 2023; Oprea 2018), from the open 4.0 files.
   - Literature counts from NCBI gene2pubmed. Stoeger 2018 showed publication counts per gene can be predicted from a small set of chemical, physical and biological properties, and gave strategies to find "important but hitherto ignored genes". Haynes 2018 documents annotation bias.
   - The brain "ignorome" method (Pandey 2014): genes with intense, selective brain expression and almost no literature. They report that the top 5% of genes absorb 70% of the relevant literature and about 20% have essentially no neuroscience literature.
   - Placeholder names (C#orf#) and Pfam domains of unknown function (InterPro hosts DUF entries). I did not verify current DUF counts.
   - neXtProt protein-existence levels are gone; use the Zenodo archive if needed.
3. **Brain context.** Check cell-type-specific expression in the ABC Atlas, Siletti 2023, SEA-AD and HPA. Check colocalization with MetaBrain, GTEx brain tissues and PsychENCODE eQTLs. MetaBrain's paper prioritized 186 cis-eQTLs for 31 brain-related traits with MR and colocalization, so there is a published precedent.
4. **Function inference.** Use coexpression neighbours (guilt by association, supported by Pandey's finding), Perturb-seq phenotype if the gene is expressed in K562 or RPE1, CRISPRbrain for neuron screens, structure and interface prediction (the INTS15 case used AlphaFold2), and ortholog conservation (Unknome's orthologue tables).

**Cell types and circuits.** Cell types: score each cluster in an atlas for enrichment of cognition heritability (scDRS or MAGMA-celltyping), then ask which enriched clusters have the thinnest literature. Siletti 2023 reports 461 clusters and 3,313 subclusters, with high diversity in midbrain and hindbrain neurons, regions cognition GWAS analyses rarely discuss. Circuits are weaker. FlyWire, MICrONS and H01 are open, but linking a human cognition gene to a circuit needs orthologs and a model organism. The human-data alternative is Project 5.

**Failure modes to expect.** Gene-set and locus-to-gene tools lean on annotation, so truly dark genes may be penalized; test that directly by comparing scores for Tdark versus other genes. Perturb-seq misses genes the cell lines don't express. The nearest gene to a GWAS signal is often not the causal one. Cognition and EA GWAS carry indirect-effect and assortment bias (section 2).

## 5. Scoped projects

All five stop at the same place: none confirms a mechanism, because that needs an experiment (knockdown or editing in neurons, an animal model, or a human cohort). I say that once here and name only the project-specific limits below. Compute figures are my estimates, not measurements. The laptop is the M5 Pro with 24 GB RAM and 1 TB SSD.

### Project 1. Dark-gene cognition shortlist

- **Data:** Cognitive performance (GCST006572 via the Catalog), Savage 2018 intelligence (CNCR), EA4 only if SSGAC delivers; Genebass cognitive-phenotype gene results; gnomAD v4.1 constraint file (95.5 MB); Unknome, Pharos 4.0 and gene2pubmed; ABC Atlas or Siletti cluster expression; MetaBrain and GTEx brain eQTLs; a 1000 Genomes LD reference.
- **Tools:** MAGMA, PoPS, SuSiE, coloc, scanpy, plus a short join script.
- **Compute:** Most steps are minutes to hours on the laptop. The per-locus fine-mapping and colocalization sweep is the part worth bursting; my estimate is tens of cloud CPU-hours.
- **Best case:** A ranked evidence table of poorly characterized genes where at least three independent lines converge (genetic signal, brain cell-type specificity, eQTL or burden support, low knownness), with a note of which line each gene lacks. A handful of genes get a one-paragraph, testable hypothesis.
- **Stops short:** Locus-to-gene assignment can still be wrong. The output is a hypothesis list. Cognitive performance is only one phenotype and Lee 2018 summary statistics carry the population-structure and indirect-effect issues described in section 2.

### Project 2. Cell-type map of cognition heritability

- **Data:** ABC Atlas human whole-brain data, Siletti 2023 (check Census first), SEA-AD, HPA single-nucleus clusters; the same cognition GWAS as Project 1; non-cognition GWAS as controls.
- **Tools:** MAGMA-celltyping, stratified LDSC on specifically expressed genes, scDRS, CELLECT, scanpy and cellxgene-census.
- **Compute:** Pseudobulk per cluster runs on the laptop. Per-cell scDRS on millions of nuclei needs a large-memory cloud machine, or subsampling; my guess is over 100 GB RAM for the full set.
- **Best case:** A ranked cell-type map for cognition against control traits, including clusters outside the classic striatal and hippocampal picture, annotated by how well characterized each cluster is. It would also feed the cell-type filter in Project 1.
- **Stops short:** Enrichment is not a causal cell. Siletti sampled three postmortem donors, and enrichment depends on the regions sampled.

### Project 3. Perturbation-informed function for dark cognition genes

- **Data:** Dark-gene list from Project 1 (or any independent list); Replogle K562 and RPE1 data (CC BY 4.0); CRISPRbrain; DepMap; BioGRID ORCS.
- **Tools:** scanpy and anndata, standard similarity and clustering on perturbation profiles; the genome-wide K562 pseudobulk file is 375 MB, so a first pass fits in laptop memory.
- **Compute:** Laptop for pseudobulk. The single-cell files (65.8 GB K562 genome-wide, 8.7 GB RPE1) need disk and a backed or cloud workflow; skip them in the first pass.
- **Best case:** Functional hypotheses for a few dark genes from their transcriptional phenotype, in the style Replogle used for regulators of ribosome biogenesis, transcription and mitochondrial respiration.
- **Stops short:** Only genes expressed in K562 or RPE1 are covered, and a K562 phenotype is not a neuronal or cognitive one. CRISPRbrain may cover neurons for some genes; I could not confirm its terms or coverage.

### Project 4. Rare- and common-variant convergence for cognition

- **Data:** Genebass gene-based results for cognitive phenotypes; SCHEMA gene-level results if downloadable; gnomAD constraint; the gene scores from Project 1; published neurodevelopmental gene lists from the Kaplanis 2020 and Fu 2022 papers.
- **Tools:** Python or R table joins; REGENIE only if re-running anything, which this project should avoid.
- **Compute:** Laptop. Gene-level tables are far smaller than single-variant ones (993 million versus 28 billion statistics in the Genebass paper), but I did not measure download size and the bucket is requester-pays.
- **Best case:** A list of genes where rare loss-of-function burden and common-variant signal point the same way, filtered by constraint and then by knownness. Rare-variant hits point directly at a gene.
- **Stops short:** Genebass is European-ancestry (394,841 individuals), and I did not check how many of its cognitive phenotypes are strong measures; UK Biobank's cognitive tests are brief, which is my recollection and not verified here. Burden tests can still be driven by a few carriers.

### Project 5. Brain-structure bridge from cognition to regions and circuits

- **Data:** ENIGMA GWAS (subcortical, cortical and hippocampal volumes, cortical thickness and surface area), the CNCR brain-volume (Jansen 2020), connectivity and cerebellar GWAS, the cognition GWAS from Project 1.
- **Tools:** LDSC for genetic correlation, LAVA for local genetic correlation (josefin-werme/LAVA, active), Genomic SEM, TwoSampleMR with MR-PRESSO.
- **Compute:** Laptop; each analysis is a summary-statistics calculation.
- **Best case:** A map of regions and connectivity phenotypes with local genetic correlation to cognition, which tells Project 2 where to look and may show whether any of the correlated regions contain Project 1's dark genes.
- **Stops short:** Structure-to-cognition MR is vulnerable to pleiotropy and to the indirect-effect problem in section 2. It points at where, and produces no new gene biology unless a dark gene sits in a correlated region.

**My order for "unexplained biology" payoff:** 1, 4, 3, then 2 and 5. Projects 1 and 4 are cheapest and run on summary statistics, so there is no institutional gate. Project 3 turns the list into function hypotheses. Projects 2 and 5 are context. This is a recommendation for the coordinator, not a pick.

## Not established

- Whether SSGAC's portal serves EA4 summary statistics, and under what exclusions.
- UK Biobank, All of Us and ABCD details from the primary pages other than ABCD's docs and NBDC pages. UKB returned 403 and All of Us was not opened.
- SCHEMA's downloadable files, CRISPRbrain's terms, GTEx portal text, gnomAD's policies page, Open Targets downloads page.
- Any cognition GWAS locus with a confirmed single-gene mechanism. I searched once and found none; that is not proof.
- What fraction of GWAS loci reach a confirmed mechanism, and the true distribution of gaps.

## Could not open

- https://www.ukbiobank.ac.uk/ and sub-pages, plus community.ukbiobank.ac.uk: 403 to curl and to my page fetcher.
- https://www.nature.com/articles/s41586-022-04556-w: redirected to a login handshake.
- https://web.archive.org/: blocked by my fetch tool.
- Content did not render for: gnomad.broadinstitute.org/downloads and /policies, gtexportal.org, app.genebass.org, schema.broadinstitute.org, platform.opentargets.org/downloads, nda.nih.gov/abcd, openneuro.org/faq. Statuses for those come from bucket listings, papers or search summaries, as noted in the table.
- docs.cellxgene.cziscience.com Census licence page: 404.
- SSGAC file list: behind login.
- Cloudflare check blocked scripted access to depmap.org.

## Sources

### Resource pages and endpoints (all checked 2026-10-04)

- GWAS Catalog downloads: https://www.ebi.ac.uk/gwas/docs/file-downloads; FTP https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/; v2 API https://www.ebi.ac.uk/gwas/rest/api/v2/; migration guide https://gwas-catalog.github.io/blog/rest-api-v2-migration-guide
- SSGAC: https://thessgac.com/ and https://thessgac.com/register/; https://www.thessgac.org/
- CTG-CNCR summary statistics: https://cncr.nl/research/summary_statistics/; software page https://cncr.nl/ctg/software/; MAGMA https://cncr.nl/research/magma/
- OpenGWAS authentication notice: https://blog.opengwas.io/posts/user-auth-spring-2024/
- PGC downloads: https://pgc.unc.edu/for-researchers/download-results/
- FinnGen: https://r12.finngen.fi/; bucket https://storage.googleapis.com/storage/v1/b/finngen-public-data-r12/o?delimiter=/
- ENIGMA: https://enigma.ini.usc.edu/research/download-enigma-gwas-results/
- gnomAD: https://gnomad.broadinstitute.org/downloads; https://gnomad.broadinstitute.org/news/2020-10-open-access-to-gnomad-data-on-multiple-cloud-providers/; https://gnomad.broadinstitute.org/news/2025-07-azure-open-datasets-deprecation/; constraint file https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1/constraint/gnomad.v4.1.constraint_metrics.tsv
- Genebass: https://app.genebass.org/; PMC9903662 https://pmc.ncbi.nlm.nih.gov/articles/PMC9903662/
- SCHEMA: https://schema.broadinstitute.org/
- Allen Brain Cell Atlas: https://brain-map.org/atlases-and-data/bkp/abc-atlas; docs https://alleninstitute.github.io/abc_atlas_access/intro.html; bucket https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/
- CELLxGENE: https://cellxgene.cziscience.com/; https://census.cellxgene.cziscience.com/cellxgene-census/v1/release.json
- SEA-AD bucket: https://sea-ad-single-cell-profiling.s3.us-west-2.amazonaws.com/
- Human Protein Atlas: https://www.proteinatlas.org/about/download; https://www.proteinatlas.org/about/licence
- GTEx: https://gtexportal.org/; bucket https://storage.googleapis.com/storage/v1/b/adult-gtex/o?delimiter=/; V10 on AnVIL https://anvilproject.org/news/2024/11/20/gtexv10
- eQTL Catalogue: https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/
- MetaBrain: https://www.metabrain.nl/
- PsychENCODE: https://www.psychencode.org/data
- Open Targets: https://platform.opentargets.org/downloads; licence https://platform-docs.opentargets.org/licence
- Replogle Perturb-seq data: https://plus.figshare.com/articles/dataset/_Mapping_information-rich_genotype-phenotype_landscapes_with_genome-scale_Perturb-seq_Replogle_et_al_2022_processed_Perturb-seq_datasets/20029387; API https://api.figshare.com/v2/articles/20029387
- DepMap: https://depmap.org/portal/download/; DepMap 23Q4 mirror https://plus.figshare.com/articles/dataset/DepMap_23Q4_Public/24667905
- BioGRID ORCS: https://downloads.thebiogrid.org/BioGRID-ORCS/
- CRISPRbrain: https://crisprbrain.org/
- FlyWire: https://codex.flywire.ai/; Zenodo https://zenodo.org/records/10676866
- MICrONS: https://www.microns-explorer.org/ and https://www.microns-explorer.org/cortical-mm3; CAVEclient authentication https://caveclient.readthedocs.io/en/latest/guide/authentication.html
- H01: https://h01-release.storage.googleapis.com/landing.html
- UK Biobank (not verified on primary pages): https://www.ukbiobank.ac.uk/
- ABCD: https://docs.abcdstudy.org/v/6_0_0/usage/access.html; https://www.nbdc-datahub.org/data-access-process
- HCP: https://www.humanconnectome.org/study/hcp-young-adult/data-use-terms
- OpenNeuro: https://openneuro.org/; bucket https://s3.amazonaws.com/openneuro.org/
- All of Us (not verified on primary pages): https://www.researchallofus.org/
- Unknome: https://unknome.mrc-lmb.cam.ac.uk/
- Pharos: https://pharos.nih.gov/; open files https://opendata.ncats.nih.gov/public/pharos/; readme https://opendata.ncats.nih.gov/public/pharos/pharos400_readme.html
- gene2pubmed: https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz
- neXtProt archive notice: https://www.expasy.org/archives/nextprot; Zenodo DOI 10.5281/zenodo.14163587
- FUMA: https://fuma.ctglab.nl/ and https://fuma.ctglab.nl/tutorial
- SMR: https://yanglab.westlake.edu.cn/software/smr/
- Tool repositories (GitHub, activity as of 2026-10-04): bulik/ldsc, stephenslab/susieR, chr1swallace/coloc, MRCIEU/TwoSampleMR, MRCIEU/ieugwasr, rondolab/MR-PRESSO, gusevlab/fusion_twas, hakyimlab/MetaXcan, rgcgithub/regenie, martinjzhang/scDRS, neurogenomics/MAGMA_Celltyping, perslab/CELLECT, FinucaneLab/pops, opentargets/gentropy, josefin-werme/LAVA, GenomicSEM/GenomicSEM, chanzuckerberg/cellxgene-census, AllenInstitute/abc_atlas_access, CAVEconnectome/CAVEclient, scverse/scanpy

### Papers (DOIs; titles and dates checked on Crossref, abstracts on PubMed where quoted)

- Abifadel 2003, PCSK9 and hypercholesterolemia: 10.1038/ng1161
- Barbeira 2018, S-PrediXcan: 10.1038/s41467-018-03621-1
- Bryois 2020, brain cell types and complex traits: 10.1038/s41588-020-0610-9
- Bulik-Sullivan 2015, LD score regression: 10.1038/ng.3211
- Burgess 2023, MR guidelines: 10.12688/wellcomeopenres.15555.3
- Claussnitzer 2015, FTO and adipocyte browning: 10.1056/NEJMoa1502214
- Cohen 2006, PCSK9 variants and LDL: 10.1056/NEJMoa054013
- Davies 2018, general cognitive function: 10.1038/s41467-018-04362-x
- de Klein 2023, MetaBrain: 10.1038/s41588-023-01300-6
- de Leeuw 2015, MAGMA: 10.1371/journal.pcbi.1004219
- Dorkenwald 2024, FlyWire: 10.1038/s41586-024-07558-y
- Emani 2024, PsychENCODE single-cell: 10.1126/science.adi5199
- Fianu 2024, Integrator termination structure: 10.1038/s41586-024-07269-4
- Finucane 2015, partitioned heritability: 10.1038/ng.3404
- Finucane 2018, specifically expressed genes: 10.1038/s41588-018-0081-4
- Frayling 2007, FTO: 10.1126/science.1141634
- Fu 2022, autism rare variation: 10.1038/s41588-022-01104-0
- Gabitto 2024, SEA-AD: 10.1038/s41593-024-01774-5
- Gamazon 2015, PrediXcan: 10.1038/ng.3367
- Giambartolomei 2014, coloc: 10.1371/journal.pgen.1004383
- Guerreiro 2013, TREM2: 10.1056/NEJMoa1211851
- Gusev 2016, FUSION: 10.1038/ng.3506
- Haynes 2018, annotation bias: 10.1038/s41598-018-19333-x
- Hemani 2018, MR-Base: 10.7554/eLife.34408
- Hormozdiari 2016, eCAVIAR: 10.1016/j.ajhg.2016.10.003
- Howe 2022, within-sibship GWAS: 10.1038/s41588-022-01062-7
- Jonsson 2013, TREM2: 10.1056/NEJMoa1211103
- Kaplanis 2020, developmental disorders: 10.1038/s41586-020-2832-5
- Karczewski 2020, gnomAD constraint: 10.1038/s41586-020-2308-7
- Karczewski 2022, Genebass: 10.1016/j.xgen.2022.100168
- Kathiresan 2008: 10.1038/ng.75; Willer 2008: 10.1038/ng.76
- Keren-Shaul 2017, disease-associated microglia: 10.1016/j.cell.2017.05.018
- Kelleher 2023, Pharos: 10.1093/nar/gkac1033
- Langfelder 2008, WGCNA: 10.1186/1471-2105-9-559
- Lee 2018, educational attainment: 10.1038/s41588-018-0147-3
- Mancuso 2019, FOCUS: 10.1038/s41588-019-0367-1
- Mbatchou 2021, REGENIE: 10.1038/s41588-021-00870-7
- Montoro 2018: 10.1038/s41586-018-0393-7; Plasschaert 2018: 10.1038/s41586-018-0394-6
- Mountjoy 2021, locus-to-gene: 10.1038/s41588-021-00945-5
- Musunuru 2010, SORT1: 10.1038/nature09266
- Ochoa 2022, Open Targets: 10.1093/nar/gkac1046
- Offley 2023, INTS15: 10.1016/j.celrep.2023.112244
- Okbay 2022, EA4: 10.1038/s41588-022-01016-z
- Oprea 2018, understudied genome: 10.1038/nrd.2018.14
- Pandey 2014, brain ignorome: 10.1371/journal.pone.0088889
- Replogle 2022, Perturb-seq: 10.1016/j.cell.2022.05.013
- Rocha 2023, Unknome: 10.1371/journal.pbio.3002222
- Savage 2018, intelligence: 10.1038/s41588-018-0152-6
- Schizophrenia MHC 2009: Shi 10.1038/nature08192; Stefansson 10.1038/nature08186; ISC 10.1038/nature08185
- Sekar 2016, C4: 10.1038/nature16549
- Sellgren 2019, microglial synapse elimination: 10.1038/s41593-018-0334-7
- Shapson-Coe 2024, H01: 10.1126/science.adk4858
- Sheils 2021, TCRD and Pharos: 10.1093/nar/gkaa993
- Siletti 2023, human brain atlas: 10.1126/science.add7046
- Singh 2022, SCHEMA: 10.1038/s41586-022-04556-w
- Skene 2018, brain cell types in schizophrenia: 10.1038/s41588-018-0129-5
- Skrivankova 2021, STROBE-MR: 10.1001/jama.2021.18236
- Smemo 2014, FTO and IRX3: 10.1038/nature13138
- Sobreira 2021, IRX3 and IRX5: 10.1126/science.abf1008
- Stoeger 2018, ignored genes: 10.1371/journal.pbio.2006643
- Strong 2012, hepatic sortilin: 10.1172/jci63563
- Timshel 2020, CELLECT: 10.7554/eLife.55851
- Wainberg 2019, TWAS: 10.1038/s41588-019-0385-z
- Wallace 2021, coloc with multiple causal variants: 10.1371/journal.pgen.1009440
- Wang 2020, SuSiE: 10.1111/rssb.12388
- Watanabe 2017, FUMA: 10.1038/s41467-017-01261-5
- Weeks 2023, PoPS: 10.1038/s41588-023-01443-6
- Zhang 2022, scDRS: 10.1038/s41588-022-01167-z
- Zhu 2016, SMR: 10.1038/ng.3538
- Zou 2022, SuSiE summary statistics: 10.1371/journal.pgen.1010299
