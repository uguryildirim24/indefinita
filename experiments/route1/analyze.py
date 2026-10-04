"""Fixed fold-local ridge analysis; run prepare.py first. No significance list enters fit."""
from pathlib import Path
import itertools
import gzip
import json
import platform
import sys
import numpy as np
import pandas as pd
import scipy
from scipy.stats import rankdata, spearmanr
import sklearn
from sklearn.linear_model import Ridge
from threadpoolctl import threadpool_limits
from prepare import ROOT, DATA, TPM, DE

DRUGS = ['cocaine', 'ketamine', 'LSD', 'MDMA']
SEED = 230679
DRAWS = 200
# Investigator-defined coarse proxies, frozen before fitting; not a cell atlas.
PANELS = {
    'neuronal_proxy': ['Snap25', 'Syt1', 'Rbfox3'],
    'astrocyte_proxy': ['Aldh1l1', 'Aqp4', 'Slc1a3'],
    'oligodendrocyte_proxy': ['Mbp', 'Plp1', 'Mog'],
    'microglia_proxy': ['Aif1', 'C1qa', 'P2ry12'],
    'endothelial_proxy': ['Pecam1', 'Cldn5', 'Kdr'],
    'mural_proxy': ['Pdgfrb', 'Rgs5', 'Cspg4'],
    # Outcome-informed published examples: descriptive reproduction references ONLY.
    'published_ECM_examples': ['Fn1', 'Mmp16', 'Trpv4', 'Tinagl1', 'Nostrin', 'Cxcr4', 'Adgre5', 'Robo4', 'Sema3g'],
    'published_IEG_examples': ['Fos', 'Junb', 'Arc', 'Dusp1'],
}


def save(rows, name):
    pd.DataFrame(rows).to_csv(ROOT / name, sep='\t', index=False, float_format='%.8g', na_rep='NA')


class Predictor:
    """Everything data-learned in this object uses the passed training indices only."""
    def fit(self, x, y, train, day, marker, marker_genes, mode='primary', penalty=1):
        self.mode = mode
        self.nuisance = None
        self.pc = None
        adjusted = x.copy()
        if mode in ('time_residual', 'composition_residual'):
            cov = (day == 14).astype(float)[:, None] if mode == 'time_residual' else marker
            self.cov_mean = cov[train].mean(axis=0)
            self.cov_sd = cov[train].std(axis=0)
            self.cov_sd[self.cov_sd == 0] = 1
            cov = (cov - self.cov_mean) / self.cov_sd
            # Day fit is OLS; composition fit ridge to avoid unstable collinear proxies.
            self.nuisance = Ridge(alpha=0 if mode == 'time_residual' else 1, solver='svd')
            self.nuisance.fit(cov[train], x[train])
            adjusted -= self.nuisance.predict(cov)
        self.mean = adjusted[train].mean(axis=0)
        self.sd = adjusted[train].std(axis=0)
        self.keep = self.sd > 0
        if mode == 'composition_residual':
            self.keep &= ~marker_genes
        self.sd[~self.keep] = 1
        if mode == 'center_only_exploratory':
            # Added after inspecting primary extrapolation, not a replacement fit.
            self.sd[:] = 1
        z = (adjusted - self.mean)[:, self.keep] / self.sd[self.keep]
        if mode == 'pc1_removed':
            # A latent-expression sensitivity, not an inferred batch assignment.
            self.pc = np.linalg.svd(z[train], full_matrices=False)[2][0]
            z -= (z @ self.pc)[:, None] * self.pc
        self.ridge = Ridge(alpha=penalty * int(self.keep.sum()), solver='cholesky')
        self.ridge.fit(z[train], y[train])
        self.scores = self.ridge.predict(z)
        self.coef = np.zeros(x.shape[1])
        c = self.ridge.coef_.copy()
        if self.pc is not None:
            c -= (c @ self.pc) * self.pc
        self.coef[self.keep] = c
        return self


def contrasts(scores, meta, drug):
    result = []
    for day in sorted(meta.loc[meta.drug == drug, 'day'].unique()):
        t = (meta.drug == drug) & (meta.day == day)
        s = (meta.drug == 'saline') & (meta.day == day)
        result.append(dict(drug=drug, day=int(day), state=int(meta.loc[t, 'state'].iloc[0]),
                           drug_score=float(scores[t].mean()), saline_score=float(scores[s].mean()),
                           drug_minus_saline=float(scores[t].mean() - scores[s].mean())))
    if drug == 'ketamine':
        a, b = result
        result.append(dict(drug=drug, day='2-minus-14', state='open-minus-closed',
                           drug_score=a['drug_score'] - b['drug_score'],
                           saline_score=a['saline_score'] - b['saline_score'],
                           drug_minus_saline=a['drug_minus_saline'] - b['drug_minus_saline']))
    return result


def main():
    meta = pd.read_csv(ROOT / 'samples.tsv', sep='\t')
    tpm = pd.read_csv(DATA / TPM, sep='\t', index_col=0)
    assert set(tpm.columns) == set(meta.matrix_sample)
    tpm = tpm.loc[:, meta.matrix_sample]
    assert tpm.index.is_unique
    x = np.log2(1 + tpm.to_numpy(dtype=float).T)
    assert np.isfinite(x).all() and (tpm.to_numpy() >= 0).all()
    genes = tpm.index.to_numpy()
    # Only identifiers/symbols are read here. pval/qval do not enter model code.
    # GEO's R-exported table has an unlabeled row index absent from the header.
    with gzip.open(DATA / DE, 'rt') as handle:
        de_columns = ['row_index'] + handle.readline().strip().split('\t')
    annotation = pd.read_csv(DATA / DE, sep='\t', header=0, names=de_columns,
                             usecols=['target_id', 'ext_gene'])
    assert not annotation.target_id.duplicated().any()
    symbols = pd.Series(genes).map(annotation.set_index('target_id').ext_gene).fillna('').to_numpy()
    panel_indices = {name: np.flatnonzero(np.isin(symbols, members)) for name, members in PANELS.items()}
    markers = [name for name in PANELS if name.endswith('_proxy')]
    marker = np.column_stack([x[:, panel_indices[name]].mean(axis=1) for name in markers])
    marker_genes = np.isin(symbols, sum([PANELS[name] for name in markers], []))
    save([dict(panel=name, gene=g, present=bool(g in symbols),
               provenance='investigator-defined coarse proxy' if name.endswith('_proxy') else 'Nardou ECM section; outcome-informed descriptive reference')
          for name, members in PANELS.items() for g in members], 'gene_sets.tsv')
    y = meta.state.to_numpy(float)
    day = meta.day.to_numpy()
    conditions = meta.condition.to_numpy()
    rng = np.random.default_rng(SEED)
    predictions, metrics, fold_audit, contrast_rows = [], [], [], []
    bootstrap_rows, deletion_rows, rank_pairs, set_rows = [], [], [], []
    primary_coefs = {}
    extrapolation_rows, leakage_rows = [], []
    fit_modes = [('primary', 'primary', 1), ('weaker_penalty', 'primary', .1),
                 ('stronger_penalty', 'primary', 10), ('time_residual', 'time_residual', 1),
                 ('pc1_removed', 'pc1_removed', 1), ('composition_residual', 'composition_residual', 1),
                 ('saline_in_training', 'primary', 1),
                 ('center_only_exploratory', 'center_only_exploratory', 1)]
    for drug in DRUGS:
        train = np.flatnonzero(~meta.drug.isin([drug, 'saline']))
        test = np.flatnonzero(meta.drug.isin([drug, 'saline']))
        assert set(meta.drug.iloc[train]).isdisjoint(set(meta.drug.iloc[test]))
        assert set(y[train]) == {0, 1}
        fold_audit.append(dict(withheld_drug=drug, train_samples=';'.join(meta.matrix_sample.iloc[train]),
                               test_samples=';'.join(meta.matrix_sample.iloc[test]),
                               train_conditions=';'.join(sorted(set(conditions[train]))),
                               train_n=len(train), test_n=len(test),
                               train_open_conditions=len(set(conditions[train][y[train] == 1])),
                               train_closed_conditions=len(set(conditions[train][y[train] == 0]))))
        models = {}
        for label, mode, penalty in fit_modes:
            tr = np.flatnonzero(meta.drug != drug) if label == 'saline_in_training' else train
            model = Predictor().fit(x, y, tr, day, marker, marker_genes, mode, penalty)
            models[label] = model
            for idx in test:
                predictions.append(dict(withheld_drug=drug, model=label, sample=meta.matrix_sample.iloc[idx],
                                        gsm=meta.gsm.iloc[idx], drug=meta.drug.iloc[idx], day=int(day[idx]),
                                        condition=conditions[idx], state=int(y[idx]), score=model.scores[idx],
                                        role='in-training-control' if idx in tr else 'held-out'))
            for row in contrasts(model.scores, meta, drug):
                contrast_rows.append(dict(model=label, **row))
            target = np.flatnonzero(meta.drug == drug)
            control = np.flatnonzero(meta.drug == 'saline')
            for role, indices in [('withheld_drug', target), ('saline_control', control), ('seen_training_optimistic', tr)]:
                metrics.append(dict(withheld_drug=drug, model=label, role=role, n=len(indices),
                                    mse=np.mean((model.scores[indices] - y[indices]) ** 2),
                                    score_mean=model.scores[indices].mean(), variable_genes=int(model.keep.sum())))
        primary = models['primary']
        primary_coefs[drug] = primary.coef
        # Holdout mutation audit: processing/fitting parameters must be identical.
        mutated_x = x.copy()
        mutated_y = y.copy()
        mutated_marker = marker.copy()
        mutated_x[test] = 123
        mutated_y[test] = 1 - y[test]
        mutated_marker[test] = 456
        for label, mode, penalty in fit_modes:
            if label == 'saline_in_training':
                continue  # controls belong to this sensitivity's training, not primary's
            audit = Predictor().fit(mutated_x, mutated_y, train, day, mutated_marker, marker_genes, mode, penalty)
            original = models[label]
            equal = np.array_equal(audit.coef, original.coef) and np.array_equal(audit.mean, original.mean) and np.array_equal(audit.sd, original.sd)
            assert equal
            leakage_rows.append(dict(withheld_drug=drug, model=label,
                                     heldout_expression_and_label_mutation_leaves_fit_identical=equal))
        z = (x - primary.mean) / primary.sd
        for idx in test:
            contributions = z[idx] * primary.coef
            for position, gene_idx in enumerate(np.argsort(-np.abs(contributions))[:10], 1):
                extrapolation_rows.append(dict(withheld_drug=drug, sample=meta.matrix_sample.iloc[idx],
                                               contribution_rank=position, target_id=genes[gene_idx], gene=symbols[gene_idx],
                                               log2_1p_TPM=x[idx, gene_idx], train_mean=primary.mean[gene_idx],
                                               train_sd=primary.sd[gene_idx], standardized_expression=z[idx, gene_idx],
                                               score_contribution=contributions[gene_idx]))
        rank = rankdata(-np.abs(primary.coef), method='average')
        # Training-only day-label baseline, no gene data.
        baseline = np.array([y[train][day[train] == d].mean() for d in day])
        for row in contrasts(baseline, meta, drug):
            contrast_rows.append(dict(model='day_only_label_mean', **row))
        blocks = {c: train[conditions[train] == c] for c in sorted(set(conditions[train]))}
        strata = {s: [c for c, idx in blocks.items() if y[idx[0]] == s] for s in [0, 1]}
        boot_coef, boot_rank = [], []
        for draw in range(DRAWS):
            sampled = [c for s in [0, 1] for c in rng.choice(strata[s], size=len(strata[s]), replace=True)]
            indices = np.concatenate([blocks[c] for c in sampled])
            model = Predictor().fit(x, y, indices, day, marker, marker_genes)
            boot_coef.append(model.coef)
            boot_rank.append(rankdata(-np.abs(model.coef), method='average'))
            for row in contrasts(model.scores, meta, drug):
                bootstrap_rows.append(dict(draw=draw, training_blocks=';'.join(sampled), **row))
        bc, br = np.array(boot_coef), np.array(boot_rank)
        # Entire gene inventory; rank/sign uncertainty not a post-hoc shortlist test.
        stable = pd.DataFrame(dict(target_id=genes, gene=symbols, primary_coefficient=primary.coef,
                                    primary_abs_rank=rank, bootstrap_median_rank=np.median(br, axis=0),
                                    bootstrap_rank_q025=np.quantile(br, .025, axis=0),
                                    bootstrap_rank_q975=np.quantile(br, .975, axis=0),
                                    bootstrap_positive_fraction=(bc > 0).mean(axis=0),
                                    bootstrap_negative_fraction=(bc < 0).mean(axis=0),
                                    bootstrap_zero_fraction=(bc == 0).mean(axis=0)))
        stable.sort_values('primary_abs_rank').to_csv(ROOT / f'gene_rank_stability_{drug}.tsv',
                                                     sep='\t', index=False, float_format='%.8g')
        for c, idx in blocks.items():
            reduced = train[conditions[train] != c]
            if len(set(y[reduced])) < 2:
                deletion_rows.append(dict(drug=drug, deleted_condition=c, status='not estimable: one state remains'))
                continue
            model = Predictor().fit(x, y, reduced, day, marker, marker_genes)
            for row in contrasts(model.scores, meta, drug):
                deletion_rows.append(dict(deleted_condition=c, status='fit', **row))
        for name, ids in panel_indices.items():
            if len(ids) == 0:
                continue
            # Summaries centered/scaled only by training values, not the test samples.
            score = ((x[:, ids] - x[train][:, ids].mean(axis=0)) /
                     np.where(x[train][:, ids].std(axis=0) > 0, x[train][:, ids].std(axis=0), 1)).mean(axis=1)
            for row in contrasts(score, meta, drug):
                set_rows.append(dict(panel=name, genes_present=';'.join(symbols[ids]),
                                     mean_primary_abs_rank=float(rank[ids].mean()),
                                     summed_abs_coefficient=float(np.abs(primary.coef[ids]).sum()), **row))
    save(extrapolation_rows, 'primary_extrapolation_diagnostics.tsv')
    save(leakage_rows, 'holdout_mutation_audit.tsv')
    save(fold_audit, 'folds.tsv')
    save(predictions, 'held_out_predictions.tsv')
    save(metrics, 'fit_metrics.tsv')
    save(contrast_rows, 'transfer_contrasts.tsv')
    save(bootstrap_rows, 'condition_bootstrap_contrasts.tsv')
    boot = pd.DataFrame(bootstrap_rows)
    summaries = []
    for (drug, d), group in boot.groupby(['drug', 'day']):
        for col in ['drug_score', 'saline_score', 'drug_minus_saline']:
            summaries.append(dict(drug=drug, day=d, measure=col, draws=len(group),
                                  q025=group[col].quantile(.025), median=group[col].median(),
                                  q975=group[col].quantile(.975), minimum=group[col].min(), maximum=group[col].max()))
    save(summaries, 'condition_bootstrap_summary.tsv')
    save(deletion_rows, 'condition_deletion_contrasts.tsv')
    save(set_rows, 'gene_set_summaries.tsv')
    for a, b in itertools.combinations(DRUGS, 2):
        rank_pairs.append(dict(fold_a=a, fold_b=b,
                               absolute_coefficient_spearman=spearmanr(np.abs(primary_coefs[a]), np.abs(primary_coefs[b])).statistic,
                               signed_coefficient_cosine=float(primary_coefs[a] @ primary_coefs[b] /
                                  (np.linalg.norm(primary_coefs[a]) * np.linalg.norm(primary_coefs[b])))))
    save(rank_pairs, 'between_fold_gene_stability.tsv')
    # Descriptive expression drug programs: all-sample contrasts NOT predictive inputs.
    patterns = {}
    for condition in sorted(set(conditions)):
        idx = np.flatnonzero(conditions == condition)
        d = day[idx[0]]
        saline = np.flatnonzero((meta.drug == 'saline') & (day == d))
        if meta.drug.iloc[idx[0]] != 'saline':
            patterns[condition] = x[idx].mean(axis=0) - x[saline].mean(axis=0)
    save([dict(condition_a=a, condition_b=b, all_gene_spearman=spearmanr(patterns[a], patterns[b]).statistic,
               contrast_cosine=float(patterns[a] @ patterns[b] / (np.linalg.norm(patterns[a]) * np.linalg.norm(patterns[b]))))
          for a, b in itertools.combinations(patterns, 2)], 'drug_program_similarity.tsv')
    save([dict(condition=c, **{name: x[conditions == c][:, ids].mean() for name, ids in panel_indices.items()})
          for c in sorted(set(conditions))], 'condition_panel_expression.tsv')
    # Rank-based non-identifiability: state is exactly in the condition-indicator span.
    condition_design = pd.get_dummies(meta.condition).to_numpy(dtype=float)
    design = dict(n_samples=len(meta), n_genes=len(genes),
                  n_conditions=len(set(conditions)), state_open_samples=int(y.sum()),
                  saturated_condition_rank=int(np.linalg.matrix_rank(condition_design)),
                  saturated_plus_state_rank=int(np.linalg.matrix_rank(np.column_stack([condition_design, y]))),
                  batch_available=False,
                  unknown_covariates=['rna_isolation_batch', 'num_slices', 'RNA_extraction_order', 'concentration',
                                      'per-sample age', 'individual learning behavior'],
                  processed_TPM_upstream_normalization='supplied by GEO; upstream sample-scaling dependencies not reestimated',
                  tpm_column_sum_min=float(tpm.sum().min()), tpm_column_sum_max=float(tpm.sum().max()))
    (ROOT / 'design_audit.json').write_text(json.dumps(design, indent=2) + '\n')
    # Now and only now read published inferential values for reference-table extraction.
    de = pd.read_csv(DATA / DE, sep='\t', index_col=0)
    reference = de.loc[de.qval <= .1, ['target_id', 'ext_gene', 'pval', 'qval']]
    reference.to_csv(ROOT / 'published_DE_reference.tsv', sep='\t', index=False)
    (ROOT / 'reproduction_reference.json').write_text(json.dumps(dict(
        published_claim=65, supplied_table_q_le_0_1=len(reference), supplied_tested_genes=len(de),
        exact_sleuth_reproduction=False,
        reason='RNA-isolation batch map, kallisto bootstraps, local metadata/cache/helpers unavailable in these inputs'), indent=2) + '\n')
    (ROOT / 'run_versions.json').write_text(json.dumps(dict(python=sys.version, platform=platform.platform(),
        numpy=np.__version__, pandas=pd.__version__, scipy=scipy.__version__, sklearn=sklearn.__version__,
        seed=SEED, condition_bootstrap_draws=DRAWS), indent=2) + '\n')
    print(pd.DataFrame(contrast_rows).query("model == 'primary'").to_string(index=False))
    print('Completed fixed folds and nuisance sensitivities; no thresholds or split selection.')


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()
