# Fixed analysis plan (written after sample audit, before fitting)

Source: `hp/indefinita/t-0009-synthesize-research-into-candidate-route:research/synthesis.md`, Route 1 and first experiment; Nardou et al., PMC10284704, read full main text and methods; authors' SupCode4 read in full at commit 5e51f9d9e4e0b196e8d64134b7605b3f12902787.

27 adult male mouse bulk NAc samples, 9 drug/day conditions, 3 replicates each. Open = LSD day 2/day 14, MDMA day 2, ketamine day 2. Closed = saline and cocaine both days, ketamine day 14. These are condition labels from behavioral/electrophysiological experiments, not individual sequenced-animal learning measurements. The behavioral natural-spline comparison used P > 0.1 as not significant; this does not define a predictive success threshold. The paper's 65 genes at q ≤ 0.1 are a reference only.

## Predictor and folds

- Four primary folds, withholding **all** samples of cocaine, ketamine, LSD or MDMA, respectively. Ketamine day 2 and day 14 remain together. Additionally withhold **all saline samples in every primary fold** so each drug can be compared with truly untrained day-matched controls. This stronger control holdout reduces training diversity; report the conventional leave-one-drug-out fit with saline retained as a sensitivity, clearly labeling saline predictions as in-training there. Never switch the primary splits based on results.
- Fixed log2(1 + supplied TPM), training-only variable-gene filter, training-only gene mean and SD, ridge regression on labels 0/1. All variable genes, no supervised preselection, no published significant-gene input. Fit intercept; alpha = number of retained genes (equivalently penalizing an average-gene kernel with alpha 1). No hyperparameter optimization. Continuous scores, not probabilities; no cutoff defining open or success.
- Fixed regularization sensitivity multipliers 0.1 and 10. Interpretable summaries of investigator-defined marker panels plus published ECM/IEG examples are descriptive only, never predictive features selected from this study. Published-panel summaries are explicitly outcome-informed references.
- Report each drug/day score minus saline/day score, individual scores and mean square error, plus ketamine day-2 minus day-14 difference before and after the corresponding saline time difference. Do not pool folds into an independent animal-level significance test.

## Uncertainty and nuisance checks

- 200 seeded, state-stratified bootstrap draws of **training drug/day conditions** (whole three-replicate blocks); refit all processing and ridge. Keep test fixed. Quantiles and coefficient-rank/sign stability are sensitivity descriptions, not independent-condition confidence about new drugs. Also delete each complete training condition when both states remain.
- Remove expression's day association using coefficients fit only in training; compare a day-only label-mean predictor. Time is confounded with sacrifice age and kinetics.
- Unknown RNA-isolation batch stays unknown. Report design ranks, missing metadata and a training-only leading-expression-PC removal sensitivity, explicitly **not** a batch estimate or correction. Condition-confounded batch can produce exactly the same observations.
- Compare held-out expression contrasts with other drug programs using day-matched saline contrasts descriptively (not reused for fitting). In-training fits are optimistic seen-treatment references only.
- Bulk composition: summarize small investigator-defined canonical cell-marker panels, not a validated deconvolution atlas. Remove the marker genes and residualize expression against their scores with training-only nuisance fits. Such scores may reflect cell activation as well as proportions. This is a sensitivity, not cell-count measurement.
- State = function(drug, day); adding state to saturated condition indicators cannot increase rank. No adjustment identifies a causal state coefficient.

## Decision (no new numerical pass threshold)

Quote synthesis: fail if the lead "only separates seen treatments, cannot track the withheld opening/closing contrast, or loses its interpretation under the identifiable nuisance comparisons". If "metadata or design cannot distinguish explanations", report **inconclusive**, not a biological null. Continue only if "cross-treatment prediction and the temporal contrast support the same program without outcome leakage, with uncertainty and missing batch information exposed". Report predictive failure separately from non-identifiability; do not turn missing batch into a biological null. No human efficacy, broad enhancement, acute reversibility or cognitive enhancement claim. Only Route 1 is authorized here.

## Transparent post-run diagnostic addition

The first fit extrapolated to scores in the thousands despite labels 0/1. Inspection found positive training SDs down to approximately 1e-10 log2(1+TPM), not a parsing or zero-variance bug. Added `center_only_exploratory` (same ridge penalty and identical folds, training centering without per-gene SD scaling), and per-sample leading contribution diagnostics. The original primary remains primary, including its bootstrap and gene-rank results. This data-informed sensitivity cannot independently validate or rescue the lead. No splits, labels or published-gene restrictions were changed. Added a holdout-mutation audit of training parameters to establish the requested fold isolation.
