# Route 1: withheld-treatment plasticity-state prediction

**Result: inconclusive; no candidate-interpretation continuation justified.** See [VERDICT.md](VERDICT.md). Laptop CPU only; no Modal, paid compute, animal work or human experiment. Only this route was run.

## Exact reproduction commands

From the repository checkout, using Python **3.13.15**:

```sh
python3 -m venv experiments/route1/data/venv
experiments/route1/data/venv/bin/python -m pip install -r experiments/route1/requirements.txt
PYTHONDONTWRITEBYTECODE=1 experiments/route1/data/venv/bin/python experiments/route1/prepare.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 experiments/route1/data/venv/bin/python experiments/route1/analyze.py
```

`prepare.py` retrieves missing raw inputs into `data/`, writes `input_provenance.tsv`, then writes `samples.tsv` **before any model fits**. Raw downloads and the environment are ignored only by `data/.gitignore`; the root gitignore is untouched. URLs, observed file hashes and sizes are recorded. The timestamp is the local file modification time, not a claimed remote release date. To reproduce exactly, compare downloaded hashes with the committed manifest. Author code is pinned to commit `5e51f9d9e4e0b196e8d64134b7605b3f12902787`. FTP-over-HTTPS GEO paths avoid the GEO webpage challenge.

`run_versions.json` records the observed platform and package versions. `requirements.txt` pins the installed environment. A single BLAS thread is also enforced in the script. Seed 230679; 200 condition-bootstrap draws. These are computational settings, not scientific acceptance thresholds. There are no configured repository gates.

## Source and mapping audit

- Specification: `git show hp/indefinita/t-0009-synthesize-research-into-candidate-route:research/synthesis.md` (Route 1 and first experiment); synthesis read in full before analysis coding.
- Nardou et al. 2023, DOI [10.1038/s41586-023-06204-3](https://doi.org/10.1038/s41586-023-06204-3), [PMC10284704](https://pmc.ncbi.nlm.nih.gov/articles/PMC10284704/). Main text and methods read for behavioral, electrophysiological and RNA-state definitions. Europe PMC full-text XML is the retrieved copy.
- [GSE230679](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE230nnn/GSE230679/): processed matrix, complete critical-period DE table and series SOFT. **Not raw reads or kallisto bootstraps.**
- [Author code](https://github.com/genesofeve/DolenPsychedelicOpenState): SupCode4 read in full. Its local CSV includes RNA-isolation batch, slice count, extraction order and concentration; these values and local cache/helper dependencies are absent from the retrieved inputs. The repository tree contains no metadata mapping. No batch labels are inferred.

The matrix's names (e.g. `19ketamine2`) are sample IDs, not GEO accessions or replicate numbers. SOFT titles supply drug/day/replicate, characteristics independently confirm drug/day/state, and descriptions explicitly associate the matrix IDs with those titles. The join is one-to-one on **drug, day and replicate**, not position. Lexicographic matrix column order is never interpreted as design. `samples.tsv` contains every sample's join fields, full characteristics, source, and unknown covariates. Three samples in each of nine conditions; 27 total; 12 open-state labels.

State is behavioral-condition membership, not a sequenced animal's measured learning ability. Open: LSD day 2 and 14, ketamine day 2, MDMA day 2. Closed: saline/cocaine day 2 and 14, ketamine day 14. Only MDMA day 2 is represented. The paper's RNA methods omit MDMA in one treatment sentence, but its results and GEO explicitly include it. Age is a protocol range P98–P112, not an individual covariate. Batch is **RNA isolation**, not sequencing flowcell; a single reported flowcell does not supply the missing batch.

Supplied TPM column sums range from about 805,096 to 1,663,060. We use these processed values as supplied. Their upstream normalization dependencies cannot be reconstructed from these inputs; fold-local processing here does not establish fold isolation of the authors' upstream generation. This is explicitly not a raw-count or sleuth reproduction.

## Method and leakage boundary

[PLAN.md](PLAN.md) records the initial choices and one transparent post-run diagnostic addition. Four primary folds withhold an entire named drug **and all saline samples**, allowing honest untrained time-matched controls. Ketamine's two days always stay together. Training includes 15 samples (5 conditions), except MDMA's fold with 18 (6 conditions). The cocaine fold has only one closed training condition. `folds.tsv` records exact membership and state support. Controls repeat across folds, so fold results are not independent.

Primary = fixed log2(1+TPM), training-variable genes, training-only centering and SD scaling, linear ridge with intercept and alpha = retained gene count. No supervised gene screening, classifier cutoff, learned tuning, neural network or random sample split. The scaling amplifies almost-unexpressed training genes catastrophically at test; these original results are retained, not disguised as biology. Scores are real-valued label predictions, **not probabilities or effect sizes**.

The published DE table supplies the full ID-to-symbol map, not outcome-based feature selection. Its p/q values are only loaded for the reference extraction after model outputs. The 65-gene reference and published ECM/IEG panels are never predictive input sets. Panels in `gene_sets.tsv` are interpretive means, not formal enrichment tests. Cell panels are small investigator-defined coarse proxies, not externally validated cell-count estimators. Dusp1 is the chosen IEG example; the main paper abbreviates this as Dusp.

Fixed sensitivities: ridge penalty ×0.1/×10; training-fitted day-expression removal; training-only leading-PC removal; training-fitted cell-marker residualization with 18 marker genes removed; conventional drug-withheld model with saline in training. This last model labels its control scores `in-training-control`, never held out. A later center-only diagnostic removes per-gene SD scaling but leaves splits and ridge penalty unchanged; it is marked `center_only_exploratory` and cannot rescue the original analysis.

`holdout_mutation_audit.tsv` verifies unchanged fitted gene coefficients, centering and scaling when all primary test expressions, marker scores and labels are replaced. This audit covers 28 primary/sensitivity fits. The conventional saline-trained sensitivity is excluded from that audit because saline is training data there. Model processing and fits use only the explicitly passed training indices, including bootstrap/deletion refits. This audit establishes our fitting isolation, not independence of the supplied upstream TPM normalization or causal validity.

## Output inventory

| Artifact | Meaning |
| --- | --- |
| `input_provenance.tsv`, `samples.tsv`, `design_audit.json` | Sources, audited sample map, missing covariates, design ranks and upstream limitation |
| `folds.tsv`, `held_out_predictions.tsv`, `transfer_contrasts.tsv`, `fit_metrics.tsv` | Fixed splits, every target/control score, drug/day transfer and optimistic seen-training references |
| `condition_bootstrap_contrasts.tsv`, `condition_bootstrap_summary.tsv` | State-stratified whole-condition training resampling, fixed test samples; quantiles are conditional sensitivity, not independent-drug confidence intervals |
| `condition_deletion_contrasts.tsv` | Delete one whole training drug/day block; one-class refit explicitly unavailable |
| `gene_rank_stability_<drug>.tsv`, `between_fold_gene_stability.tsv` | Full 36,047-gene primary coefficient rank/sign bootstrap results and cross-fold stability; unretained genes have zero coefficients and tied ranks |
| `gene_sets.tsv`, `gene_set_summaries.tsv`, `condition_panel_expression.tsv` | Panel definitions, fold-training-scaled control contrasts, raw condition mean log-expression; descriptive only |
| `drug_program_similarity.tsv` | All-gene drug-minus-day-matched-saline similarities, computed descriptively after fits; shared control subtraction can induce similarity |
| `primary_extrapolation_diagnostics.tsv` | Ten largest absolute per-gene score contributions per test sample, training SD and test standardized expression |
| `holdout_mutation_audit.tsv` | Fold-fitting isolation evidence |
| `published_DE_reference.tsv`, `reproduction_reference.json` | 65 q ≤ 0.1 rows recovered from supplied table; original inference not independently reproduced |
| `run_versions.json`, `requirements.txt`, `PLAN.md`, `VERDICT.md` | Execution environment, choices/amendment and bounded decision |

Condition bootstrap resamples training drug/day blocks within open/closed strata, with all three replicates traveling together. Stratification retains both states; it does not add new perturbations. Test animals are not resampled, no label-permutation significance is claimed, and no sample-level inferential p-value treats correlated replicates as independent conditions. Gene-rank stability is sensitivity of this predictor, not causal gene prioritization. Candidate doses, synthesis, sourcing and self-experimentation are outside this analysis.
