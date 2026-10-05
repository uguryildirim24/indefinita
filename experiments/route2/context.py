"""Separate annotations, matched bias descriptions and a non-causal evidence dossier."""
from collections import defaultdict, Counter
import csv
import gzip
import json
import math
import re
import zipfile
import numpy as np
from scipy.stats import spearmanr
from associate import HERE, ROOT, DATA as CORE_DATA, rows, tsv, sha

DATA = HERE / 'data'
BRAIN = {'brain', 'cerebral cortex', 'cerebellum', 'hippocampus', 'basal ganglia', 'amygdala',
         'hypothalamus', 'midbrain', 'pons', 'medulla oblongata', 'spinal cord', 'thalamus'}


def number(x):
    return None if x in [None, '', 'NA'] else float(x)


def main():
    manifest = {r['file']: r for r in json.loads((HERE / 'fetch-manifest.json').read_text())}
    for name in ['hpa-expression-v25.zip', 'neuron-sgrna.txt.gz']:
        r = manifest[name]
        if r['http_status'] != 200 or r.get('expected_sha256') or sha(DATA / name) != r['sha256']:
            raise RuntimeError('Changed/unavailable context input: ' + name)
    expression = defaultdict(dict)
    with zipfile.ZipFile(DATA / 'hpa-expression-v25.zip') as z:
        name, = z.namelist()
        import io
        with z.open(name) as raw:
            for r in csv.DictReader(io.TextIOWrapper(raw), delimiter='\t'):
                expression[r['Gene']][r['Tissue']] = float(r['nTPM'])
    hgnc = list(rows(CORE_DATA / 'hgnc.tsv'))
    byentrez = defaultdict(set)
    for h in hgnc:
        if h['status'] == 'Approved' and h['ensembl_gene_id'] and h['entrez_id']:
            byentrez[h['entrez_id']].add(h['ensembl_gene_id'])
    pharos = defaultdict(set)
    with (CORE_DATA / 'pharos400.csv').open() as f:
        for r in csv.DictReader(f):
            gs = byentrez.get(r['ncbi_id'], set())
            if len(gs) == 1:
                pharos[next(iter(gs))].add(r['tdl'])
    # The CROP-seq file has guide identifiers, not a screen outcome or an atlas.
    # Guide coverage is handled explicitly in perturbation.py and never inferred from RNA expression.
    perturb = {r['gene_id']: r for r in rows(HERE / 'perturbation-coverage.tsv')}
    inventory = list(rows(HERE / 'gene-associations.tsv'))
    for g in inventory:
        exp = expression.get(g['gene_id'], {})
        brain = {k: v for k, v in exp.items() if k.lower() in BRAIN}
        g.update(hpa_expression_available=bool(exp), hpa_brain_available=bool(brain),
                 hpa_brain_max_ntpm=max(brain.values(), default=None),
                 hpa_brain_max_tissue=max(brain, key=brain.get) if brain else None,
                 pharos_tdl=';'.join(sorted(pharos[g['gene_id']])) or None)
    tsv('gene-context.tsv', [{k: g[k] for k in ['gene_id', 'symbol', 'hpa_expression_available', 'hpa_brain_available',
         'hpa_brain_max_ntpm', 'hpa_brain_max_tissue', 'pharos_tdl', 'hgnc_mapping', 'unknome_knownness']} for g in inventory])
    covered = [g for g in inventory if number(g['gene_bonferroni_p']) is not None]
    length = np.log10([float(g['gene_length_bp']) for g in covered])
    density = np.array([float(g['snp_density_per_kb']) for g in covered])
    length_edges = np.quantile(length, [0.2, .4, .6, .8])
    density_edges = np.quantile(density, [0.2, .4, .6, .8])
    strata = defaultdict(list)
    for g, l, d in zip(covered, length, density):
        key = (int(np.searchsorted(length_edges, l, side='right')), int(np.searchsorted(density_edges, d, side='right')), g['hpa_brain_available'])
        strata[key].append(g)
    matched = []
    for key, gs in sorted(strata.items()):
        hits = [g for g in gs if g['gene_association_fwer05'] == 'True']
        controls = [g for g in gs if g['gene_association_fwer05'] != 'True']
        for group, subset in [('associated', hits), ('other_covered_genes', controls)]:
            k = [number(g['unknome_knownness']) for g in subset if number(g['unknome_knownness']) is not None]
            matched.append(dict(log_length_quintile=key[0] + 1, density_quintile=key[1] + 1, brain_expression_coverage=key[2],
                                group=group, genes=len(subset), knownness_scored=len(k),
                                knownness_mean=float(np.mean(k)) if k else None, knownness_median=float(np.median(k)) if k else None,
                                hgnc_unique=sum(g['hgnc_mapping'] == 'unique' for g in subset),
                                pharos_scored=sum(bool(g['pharos_tdl']) for g in subset),
                                adult_brain_max_ntpm_median=float(np.median([g['hpa_brain_max_ntpm'] for g in subset if g['hpa_brain_max_ntpm'] is not None])) if any(g['hpa_brain_max_ntpm'] is not None for g in subset) else None,
                                comparison_available=bool(hits and controls),
                                gene_length_median=float(np.median([float(g['gene_length_bp']) for g in subset])) if subset else None))
    tsv('bias-matched-strata.tsv', matched)
    pscore = np.array([-math.log10(float(g['gene_bonferroni_p'])) for g in covered])
    bias = dict(tested_genes=len(covered), quantile_edges_log10_length=length_edges.tolist(), quantile_edges_density=density_edges.tolist(),
                spearman_gene_evidence_vs_log_length=float(spearmanr(pscore, length).statistic),
                spearman_gene_evidence_vs_snp_density=float(spearmanr(pscore, density).statistic),
                annotation_coverage={key: dict(Counter(str(g[key]) for g in inventory)) for key in
                                    ['hgnc_mapping', 'hpa_expression_available', 'hpa_brain_available']},
                unknome_scored=sum(number(g['unknome_knownness']) is not None for g in inventory),
                pharos_scored=sum(bool(g['pharos_tdl']) for g in inventory),
                interpretation='Descriptive matching, not a causal adjustment or independent GWAS validation; union-bound power depends on gene boundaries and SNP count')
    paired_diff = []
    for gs in strata.values():
        hits = [number(g['unknome_knownness']) for g in gs if g['gene_association_fwer05'] == 'True' and number(g['unknome_knownness']) is not None]
        controls = [number(g['unknome_knownness']) for g in gs if g['gene_association_fwer05'] != 'True' and number(g['unknome_knownness']) is not None]
        if controls:
            paired_diff.extend(k - np.mean(controls) for k in hits)
    bias.update(matched_associated_scored_genes=len(paired_diff),
                matched_knownness_mean_difference=float(np.mean(paired_diff)) if paired_diff else None,
                matched_controls='all nonassociated scored genes in same length/density quintiles and HPA brain-coverage stratum; reused controls, not independent pairs')
    # Additional expression-level sensitivity, without re-ranking/selecting genes.
    expr_edges = np.quantile([np.log1p(g['hpa_brain_max_ntpm']) for g in covered if g['hpa_brain_max_ntpm'] is not None], [.2, .4, .6, .8])
    expr_strata = defaultdict(list)
    for key, gs in strata.items():
        for g in gs:
            ebin = -1 if g['hpa_brain_max_ntpm'] is None else int(np.searchsorted(expr_edges, np.log1p(g['hpa_brain_max_ntpm']), side='right'))
            expr_strata[key + (ebin,)].append(g)
    differences = []
    expr_comparisons = []
    for key, gs in sorted(expr_strata.items()):
        hits = [g for g in gs if g['gene_association_fwer05'] == 'True']
        controls = [g for g in gs if g['gene_association_fwer05'] != 'True']
        h = [number(g['unknome_knownness']) for g in hits if number(g['unknome_knownness']) is not None]
        c = [number(g['unknome_knownness']) for g in controls if number(g['unknome_knownness']) is not None]
        if c:
            differences.extend(k - np.mean(c) for k in h)
        expr_comparisons.append(dict(length_quintile=key[0]+1, density_quintile=key[1]+1, brain_coverage=key[2],
            expression_quintile=key[3]+1, associated_genes=len(hits), control_genes=len(controls),
            associated_scored=len(h), controls_scored=len(c),
            associated_knownness_mean=float(np.mean(h)) if h else None,
            control_knownness_mean=float(np.mean(c)) if c else None))
    tsv('bias-expression-matched.tsv', expr_comparisons)
    bias.update(expression_match_edges_log1p_ntpm=expr_edges.tolist(), expression_matched_associated_scored_genes=len(differences),
        expression_matched_knownness_mean_difference=float(np.mean(differences)) if differences else None,
        expression_match_limitation='HPA consensus RNA blends HPA/GTEx; an annotation/covariate, not independent GWAS or independent GTEx expression evidence')
    (HERE / 'bias-summary.json').write_text(json.dumps(bias, indent=2) + '\n')
    alternatives = list(rows(HERE / 'locus-alternatives.tsv'))
    region_genes = defaultdict(list)
    gene_regions = defaultdict(list)
    for a in alternatives:
        region_genes[a['region_id']].append(a)
        gene_regions[a['gene_id']].append(a['region_id'])
    ld = {(r['region_id'], r['gene_id']): r for r in rows(HERE / 'gene-ld-alternatives.tsv')}
    qcov = {(r['region_id'], r['gene_id']): r for r in rows(HERE / 'qtl-gene-coverage.tsv')}
    coloc = defaultdict(list)
    for c in rows(HERE / 'coloc-sensitivity.tsv'):
        coloc[(c['region_id'], c['gene_id'])].append(c)
    vep = []
    pilot_markers = {r['MarkerName']: r for r in rows(HERE / 'pilot-gwas.tsv')}
    for marker in ['rs2352974', 'rs1906252', 'rs13107325']:
        response = json.loads((DATA / ('vep-' + marker + '.json')).read_text())
        for record in response:
            gw = pilot_markers[marker]
            ref_allele = record['allele_string'].split('/')[0]
            coordinate_match = record['assembly_name'] == 'GRCh37' and record['seq_region_name'] == gw['CHR'] and record['start'] == int(gw['POS']) and record['strand'] == 1
            for tc in record.get('transcript_consequences', []):
                allele_match = coordinate_match and {ref_allele, tc.get('variant_allele')} == {gw['A1'], gw['A2']}
                vep.append(dict(marker=marker, gene_id=tc['gene_id'], transcript_id=tc['transcript_id'],
                                gene_symbol=tc.get('gene_symbol'), consequence=';'.join(tc['consequence_terms']),
                                amino_acids=tc.get('amino_acids'), protein_position=tc.get('protein_start'),
                                vep_variant_allele=tc.get('variant_allele'), gwas_allele_pair=gw['A1'] + '/' + gw['A2'],
                                gwas_allele_compatible=allele_match,
                                source='Ensembl GRCh37 VEP anonymous snapshot; all transcript/allele alternatives retained; not independent association'))
    tsv('lead-variant-consequences.tsv', vep)
    evidence = []
    for g in inventory:
        if g['gene_association_fwer05'] != 'True':
            continue
        ridlist = gene_regions[g['gene_id']]
        rid = min(ridlist, key=lambda x: int(x[1:])) if ridlist else None
        others = [a for a in region_genes[rid] if a['gene_id'] != g['gene_id']] if rid else []
        cs = coloc[(rid, g['gene_id'])]
        h4 = [float(c['H4']) for c in cs if c.get('H4') not in [None, 'NA']]
        l = ld.get((rid, g['gene_id']), {})
        qc = qcov.get((rid, g['gene_id']), {})
        pt = perturb.get(g['gene_id'], {})
        v = [r for r in vep if r['gene_id'] == g['gene_id'] and r['gwas_allele_compatible']]
        interpret = ('Adult tissue expression observed (' + str(g['hpa_brain_max_tissue']) + '); timing not identified.'
                     if g['hpa_brain_available'] else 'Adult brain expression not covered in HPA; not evidence of absence.')
        contrast = ';'.join(a['symbol'] for a in others)
        coding = any('missense_variant' in r['consequence'] for r in v)
        evidence.append(dict(evidence_rank=len(evidence) + 1, gene_id=g['gene_id'], symbol=g['symbol'],
            association_rank=g['association_rank'], region_id=rid, body_lead_snp=g['body_lead_snp'], body_min_p=g['body_min_p'],
            gene_bonferroni_p=g['gene_bonferroni_p'], across_gene_bonferroni_p=g['across_gene_bonferroni_p'],
            gene_length_bp=g['gene_length_bp'], snp_count=g['snp_count'], locus_alternative_count=len(others), locus_alternatives=contrast,
            unknome_knownness=g['unknome_knownness'], unknome_rank=g['unknome_rank'], knownness_provenance=g['knownness_provenance'],
            pharos_tdl=g['pharos_tdl'], human_pubmed_count=g['human_pubmed_count'], hgnc_mapping=g['hgnc_mapping'],
            body_lead_r2_to_region_lead=l.get('body_lead_r2_to_region_lead'),
            adult_brain_qtl_shared_variants=qc.get('shared_aligned_variants'), adult_brain_qtl_lead_covered=qc.get('gwas_lead_covered'),
            single_signal_coloc_H4_min=min(h4) if h4 else None, single_signal_coloc_H4_max=max(h4) if h4 else None,
            lead_variant_consequences=';'.join(sorted({r['consequence'] for r in v})) or None,
            locus_assignment='lead missense localizes a coding hypothesis, not mediation or exclusive causation' if coding else
                             'unresolved competing genes; gene-body association is not causal assignment',
            developmental_vs_adult='Lifelong developmental, systemic and adult explanations remain. ' + interpret,
            adult_brain_max_ntpm=g['hpa_brain_max_ntpm'], adult_brain_max_tissue=g['hpa_brain_max_tissue'],
            perturbation_coverage=pt.get('neuron_guide_coverage', 'not checked outside pilot'),
            perturbation_readout=pt.get('readout', 'not checked outside pilot'),
            savage_overlapping_magma_p=g['savage_magma_p'], savage_mapping=g['savage_fuma_mapping'],
            rare_direct_qc_hit=g['rare_significant_qc_pass'], independent_replication_established=False,
            data_dependencies='Lee CP GCST006572 + GENCODE v19; HGNC/Unknome/Pharos/HPA separate annotations; '
                              + ('EUR LD + GTEx DLPFC/Catalogue + chain/VEP + Tian guide coverage pilot' if rid in ['R001', 'R002', 'R003'] else 'LD/QTL/perturbation not followed outside pilot')
                              + '; Savage/Genebass overlap; EA excluded',
            specific_disconfirming_observation='Independent ancestry-matched fine-mapping excludes ' + g['body_lead_snp']
                       + ' and assigns a different variant/gene' + (' (e.g. ' + ', '.join(a['symbol'] for a in others[:3]) + ')' if others else '')
                       + '; adult-specific perturbation in the implicated cell type has no predicted functional effect despite verified engagement. '
                       + ('A linked regulatory alternative explains the CP signal after conditioning on the missense variant.' if coding else 'Shared-signal evidence disappears on multiple-signal conditioning or complete variant coverage.'),
            status='association hypothesis only; not an enhancement target'))
    tsv('ranked-evidence.tsv', evidence)
    tsv('pilot-evidence.tsv', [g for g in evidence if g['region_id'] in ['R001', 'R002', 'R003']])
    tsv('access-inventory.tsv', json.loads((HERE / 'fetch-manifest.json').read_text()))
    (HERE / 'context-summary.json').write_text(json.dumps(dict(evidence_rows=len(evidence),
          associated_pharos_tdark=sum(g['pharos_tdl'] == 'Tdark' for g in evidence),
          pilot_associated_pharos_tdark=[g['symbol'] for g in evidence if g['region_id'] in ['R001', 'R002', 'R003'] and g['pharos_tdl'] == 'Tdark'],
          pilot_alternative_genes=sum(a['pilot'] == 'True' for a in alternatives),
          expression_tissues=sorted({t for exp in expression.values() for t in exp if t.lower() in BRAIN}),
          rank_uses_only_genomic_association=True, full_QTL_or_perturbation_scope=False), indent=2) + '\n')
    print(json.dumps(bias, indent=2))

if __name__ == '__main__':
    main()
