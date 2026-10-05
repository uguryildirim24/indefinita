"""Route 2 entry point; run with the pinned route-specific Python requirements."""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

if __name__ == '__main__':
    subprocess.run([sys.executable, str(ROOT / 'scripts/fetch.py'), 'lee2018.txt', 'gencode-v19.gtf.gz',
                    'hgnc.tsv', 'pharos400.csv', 'lee-methods.pdf'], check=True, cwd=ROOT)
    for script in ['fetch.py', 'associate.py', 'ld.py', 'qtl.py', 'perturbation.py', 'context.py']:
        subprocess.run([sys.executable, str(HERE / script)], check=True, cwd=ROOT)
