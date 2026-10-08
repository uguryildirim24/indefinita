# indefinita

A Python data layer that joins cognition GWAS, rare-variant evidence and gene-knownness annotations into ranked hypothesis lists.

It exists to study understudied genes tied to human cognition without treating low knownness as evidence of causation. **Outputs are hypotheses, not findings or intervention targets.** The pipeline uses public summary data, not individual records.

## What the stored results show

The core tables retain the October 4, 2026 snapshot. Counts are recorded in `derived/analysis-summary.json` and the TSVs:

- The evidence ledger contains 1,339 genes, including 1,332 with direct common-variant support.
- Four rare-variant genes pass the implemented significance and QC filters: ADAMTS6, KDM5B, NACC1 and AC011448.1 (ENSG00000258674).
- **Zero genes meet both direct-cognition common-variant and qualifying rare-variant criteria.** `derived/cognition-hypotheses.tsv` has a header and no data rows.
- A separate educational-attainment proxy contains three association rows for KDM5B and NACC1. Neither is Pharos Tdark. This is not direct-cognition convergence.

Two implemented experiments are separate from the core join:

| Component | Stored outcome | Reproduction scope |
| --- | --- | --- |
| [Route 1: mouse expression prediction](experiments/route1/README.md) | Inconclusive. A 27-sample withheld-treatment predictor extrapolates badly. Missing batch information and condition-defined labels prevent a causal interpretation. | Processed GEO matrix and metadata, CPU ridge fits and condition resampling. Not raw-read reproduction. |
| [Route 2: cognition-locus alternatives](experiments/route2/README.md) | 406 conservative gene-body associations among 18,913 tested genes. Three pilot regions contain 199 alternatives. No poorly understood causal cognition gene is resolved. | Roughly 4.8 GB of inputs/extracted references, one adult frontal-cortex QTL context and a limited perturbation-access audit. |

The experiment verdicts preserve negative results and uncertainty. The repo contains tables, not a validated mechanism or a demonstrated change in cognitive performance.

## Run from a clean clone

Requirements: Python 3.13 or newer and `uv` on PATH. The stored run used Python 3.13.15. The locked core environment uses httpx, openpyxl and pypdf. Run all commands from the repository root. No paid account, cloud service or GPU is needed.

### Install and inspect without downloading data

```sh
uv sync --frozen
uv run --frozen python - <<'PY'
import csv
import json
from pathlib import Path
summary = json.loads(Path('derived/analysis-summary.json').read_text())
print(json.dumps(summary, indent=2))
for name in ('cognition-hypotheses.tsv', 'ea-proxy-hypotheses.tsv', 'gene-evidence.tsv'):
    with (Path('derived') / name).open() as handle:
        print(name, sum(1 for _ in csv.DictReader(handle, delimiter='\t')), 'rows')
PY
```

This inspects the committed snapshot. It does not reproduce the analysis.

### Reproduce the core join with downloads

```sh
uv run --frozen python scripts/pipeline.py
```

The stored fetch inventory totals about 2.447 GB. Raw responses and partial downloads stay in ignored `data/`. The downloader caps that directory at 20 GB decimal, including existing files. Do not run two instances against the same cache. Successful cached responses are hash-checked and reused.

The downloader reads and rewrites `derived/fetch-manifest.json`. It records changed-source hashes alongside the prior expected hash. The join rejects unavailable or changed required inputs. Genebass JSON uses a decoded payload hash because its gzip envelope can change. Cached responses retain their stored observation times.

HGNC and NCBI gene2pubmed use changing source URLs. The original literature and VEP pins are retained. No literature or VEP refresh is part of this cleanup. Current source bytes may differ from the stored snapshot and block reproduction. A fresh run is not guaranteed to reproduce an older download.

A completed run regenerates `derived/` tables and `derived/source-method-excerpts.txt`. The source excerpts are ignored generated files. Dataset URLs are declared in `scripts/fetch.py` and `scripts/fetch_genebass.py`; no credentials or environment secrets are required.

For the experiments, use the exact dependency and run commands in their READMEs. Route 1 downloads into `experiments/route1/data/`. Route 2 uses both the core cache and `experiments/route2/data/`, and reads the committed core knownness/evidence tables without rebuilding that join. Its complete gene-association export is generated at `experiments/route2/gene-associations.tsv`. This 5.8 MB export is ignored and can be regenerated with the Route 2 command. The smaller association summary and ranked evidence remain committed.

## Project layout

- `scripts/`: core fetch, Genebass retrieval, join and pipeline entry point.
- `derived/`: small result tables, source pins, access inventory and analysis summary.
- `experiments/route1/`: mouse expression analysis, fixed plan, outputs and verdict.
- `experiments/route2/`: gene-body association analysis, LD/QTL follow-up, alternatives and verdict.
- `docs/METHODS.md`: exact core mapping choices, thresholds and coverage limits.
- `docs/DATA_TERMS.md`: source attribution and separate data restrictions.
- `research/`: archived scientific reviews and source evidence, not implemented workflows.
- `data/` and experiment `data/` directories: ignored downloads and environments.

## Limits and known gaps

Body overlap is not causal gene assignment. Common/rare studies overlap in participants and are not independent replications. The rare API cannot support every paper QC step, including SE=0 exclusion. Missing annotations are unavailable, not zero knownness. Educational attainment stays separate from direct cognition. Population effects, ancestry limits, indirect genetic effects and annotation bias remain.

Route 1 cannot reconstruct upstream TPM generation or missing RNA-isolation batch metadata. Route 2 does not perform conditional multiple-signal fine-mapping, all-tissue colocalization or genome-wide perturbation coverage. Its unavailable neuronal target/phenotype tables are not biological negatives.

This cleanup retains the original pins and scientific tables. On October 8, 2026, `uv sync --frozen` and the snapshot inspection above passed. The inspected tables had 0 direct-convergence rows, 3 proxy rows and 1,339 evidence rows. Route 1 environment creation, its pinned dependency installation and `analyze.py` passed using the existing processed inputs and sample map. Its tracked outputs matched the stored files.

The core pipeline and Route 2 entry point were skipped because they collect data and need multi-GB inputs. Route 1 preparation was skipped because uncached paper and author-code inputs would trigger collection, including GitHub requests. No paid account, GPU or GitHub operation was used. This is not a fresh clean-clone reproduction.

Future revisions of required sources can still stop reproduction, especially unversioned literature links and API annotations. Independent biological replication and a comprehensive third-party redistribution review are not documented. Public download access does not waive source terms.

## How this was built

AI coding agents did much of the implementation under Rolf's direction. Rolf set the research direction and the public scope around understudied genes tied to human cognition. Repository review checked runnable setup and agreement between stored counts and documentation. The repo does not document an independent check by Rolf of every scientific claim or a biological validation of these hypotheses. Plans distinguish initial choices from post-run diagnostics.

## License and citation

Original code and original documentation are under the [MIT License](LICENSE), copyright 2026 Rolf. Source data and source-derived tables are not relicensed by MIT. See [data terms](docs/DATA_TERMS.md), including the recorded CNCR noncommercial/share-alike restrictions.

No project paper or preprint is included. When using this work, cite the repository and the underlying sources listed in `docs/DATA_TERMS.md` and the experiment READMEs. Do not cite its hypothesis lists as confirmed findings.
