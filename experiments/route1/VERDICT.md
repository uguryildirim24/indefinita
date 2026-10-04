# Verdict: inconclusive

**This run does not establish a transferable plasticity-state program, and does not justify candidate interpretation. It is not a biological null.**

The specification says: "If metadata or design cannot distinguish explanations, record inconclusive, not a biological null." RNA-isolation batch is missing; condition-level state and plausible tissue-composition/time differences remain inseparable. The primary predictor also fails as a useful out-of-treatment predictor because of severe expression extrapolation. Missing information and a failed predictor must not be turned into absent biology.

## Reproduced facts

- The metadata joins all **27** samples uniquely by drug/day/replicate: nine conditions, three replicates each, 12 condition-defined open labels. Ketamine day 2 is open and day 14 closed; LSD both days and MDMA day 2 are open. Cocaine/saline both days are closed. No individual RNA-animal learning scores exist in these inputs.
- The supplied DE table contains **65 genes at q ≤ 0.1**, matching Nardou's reported count. This reproduces a table fact, **not** the original batch-adjusted sleuth inference. Missing batch labels, kallisto bootstraps and local objects preclude that reproduction.

## New predictive associations: not robust transfer

Primary continuous score contrasts (target drug mean minus its same-day held-out saline mean):

| Withheld drug | Day 2 | Day 14 |
| --- | ---: | ---: |
| cocaine (closed both) | +2,712.16 | −73,366.89 |
| ketamine (open → closed) | +3,023.77 | +961.39 |
| LSD (open both) | +421.54 | −4,651.79 |
| MDMA (open day 2) | −32.27 | not sampled |

These are **not probabilities, biological magnitudes, or evidence of enormous effects**. Individual training gene SDs approach 1e-10 log-expression units. Almost-unexpressed training genes dominate held-out scores: Gm8271 contributes roughly +9,256 to one ketamine day-2 sample and +2,747 to one day-14 sample. LSD day 14 is dominated by Gm8127 in one sample. `primary_extrapolation_diagnostics.tsv` exposes this failure rather than filtering it away after seeing labels.

The ketamine mean temporal difference is +2,169.75 before controls and +2,062.37 after saline's time difference. That apparent direction is not reliable: the training-condition bootstrap's control-adjusted 2.5th–97.5th quantiles span **−14,202.34 to +3,504.03**. Deleting LSD day 2 reverses the adjusted contrast to −8,477.03. These are conditional sensitivity ranges, not confidence about independent new perturbations. Optimistic seen-training MSE is 0.040–0.060 while primary withheld-drug MSE ranges from about 3,698 to 114 million. Gene-wise scaling has broken extrapolation; numerical prediction failure is not mechanistic falsification.

The transparent, data-informed **center-only exploratory diagnostic** has ordinary-sized scores but does not rescue the temporal question. Ketamine scores are 0.60436 (day 2) and 0.60345 (day 14), a difference of 0.00091; saline's corresponding difference is 0.15365, yielding an adjusted contrast of **−0.15274**. MDMA remains below same-day saline (−0.01359); LSD is slightly above saline on both days. This diagnostic is not a newly selected winning primary model.

Full gene-rank stability is supplied for every fold, not a retrospectively selected gene list. Cross-fold absolute-coefficient rank correlations are 0.51–0.68. Some coefficient signs remain stable conditionally, but ranks can move widely (ketamine-fold Tinagl1 rank 4; bootstrap rank quantiles 2–409). A coefficient's rank is not its contribution when held-out expression lies far beyond training. No gene mechanism or intervention direction is established.

## Nuisance explanations checked

- **Batch:** unknown RNA-isolation batch, extraction order, slice count and concentration remain unknown in `samples.tsv`. Authors' code references a missing local metadata CSV. Removing training PC1 leaves the same qualitative primary failure and is **not** an inferred batch correction. A batch associated with condition could generate the same measured state association. Public sample sequencing on one flowcell does not remove RNA-isolation uncertainty.
- **Condition resampling:** 200 state-stratified training-block bootstrap draws per fold and whole-condition deletions expose instability. The cocaine fold has only one closed training condition, so its deletion cannot fit both states. Repeated draws of a few conditions are not independent perturbation replication.
- **Time:** the day-only baseline assigns identical scores to drug and saline at each day. It nevertheless generates a ketamine day-2/day-14 difference of 0.16667 from training label prevalence alone. Training-fitted day-expression removal does not restore robust primary transfer. Time-related expression and age/kinetics are not causally resolved by adding a covariate.
- **Drug programs:** descriptive all-gene time-matched contrasts are often closer across state boundaries than across the same drug's days. LSD day-14 versus closed ketamine day-14 has cosine 0.924; LSD day-14 versus open LSD day-2 has cosine −0.149. Shared subtraction of the same saline control can itself induce those similarities. This does not isolate a drug-independent state program.
- **Bulk composition:** oligodendrocyte/microglia proxy mean log-expression is higher in saline day 14 than day 2 (10.635 vs 9.582; 6.041 vs 4.907), while endothelial/mural proxies are lower. The published ECM-example mean is higher at day 2 than day 14 in both saline and ketamine; its training-scaled, control-adjusted ketamine temporal contrast is −0.594, despite the unadjusted +0.283. Marker residualization does not repair primary extrapolation. These coarse panels cannot distinguish cell abundance from cell activation or regulation; no deconvolution or measured cell counts are claimed.
- **Structural non-identifiability:** the nine-condition design has rank **9**, and adding state still gives rank **9** (`design_audit.json`). State is a deterministic function of drug and day. Saturated adjustment cannot identify a separate causal state effect, even with perfect prediction.

All learned processing and fitting in this analysis remain inside training folds, with drug groups intact. Held-out expression/label mutation leaves fitted parameters unchanged for 28 audited fits. Saline is held out in the primary folds; the conventional saline-trained sensitivity is labeled accordingly. The supplied processed matrix's upstream scaling cannot be independently audited from these inputs.

## What remains open

Coverage is **complete** for the named processed inputs, sample audit, fixed folds, rank outputs and listed implementable nuisance sensitivities; **partial** for composition and latent technical explanations; **unavailable** for original batch metadata, cached author inputs, individual behavioral measurements and independent biological replication. No independent-data search or candidate dossier was run.

The specification's "continue" condition—cross-treatment prediction and the temporal contrast supporting the same program—is **not established**. The fixed predictor failed its practical prerequisite, while the design prevents a biological verdict. Save this state for the coordinator; do not optimize new splits or proceed to another route in this lane. This establishes no healthy-human efficacy, broad cognition, acute onset, reversibility, causal enhancer or cognitive enhancement claim.
