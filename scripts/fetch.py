"""Fetch public inputs; retain exact response bytes and an auditable inventory."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import threading

import httpx

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "derived"
BUDGET = 20_000_000_000
LOCK = threading.Lock()
RESERVED = 0
UA = "Mozilla/5.0 cognition-data/0.1 (public summary-statistics research)"

# Explicit public URLs, no credentials or billing project. Nextcloud share token
# is public, not an account credential. Raw source versions are retained by hash.
SOURCES = {
    "gencode-v19.gtf.gz": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz",
    "lee-supplement.xlsx": "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41588-018-0147-3/MediaObjects/41588_2018_147_MOESM3_ESM.xlsx",
    "lee-methods.pdf": "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41588-018-0147-3/MediaObjects/41588_2018_147_MOESM1_ESM.pdf",
    "lee-paper.html": "https://www.nature.com/articles/s41588-018-0147-3",
    "lee2018.txt": "https://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST006001-GCST007000/GCST006572/GWAS_CP_all.txt",
    "savage2018.txt": "https://vu.data.surf.nl/index.php/s/9tgwxmO5yosQkmb/download?path=%2F&files=SavageJansen_2018_intelligence_metaanalysis.txt",
    "savage-readme.txt": "https://vu.data.surf.nl/index.php/s/9tgwxmO5yosQkmb/download?path=%2F&files=README_SavageJansen_2018_intelligence_metaanalysis.txt",
    "savage-checksum.txt": "https://vu.data.surf.nl/index.php/s/9tgwxmO5yosQkmb/download?path=%2F&files=CHECKSUM_SavageJansen_2018_intelligence_metaanalysis.txt",
    "savage-supplement.xlsx": "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41588-018-0152-6/MediaObjects/41588_2018_152_MOESM3_ESM.xlsx",
    "savage-paper.html": "https://www.nature.com/articles/s41588-018-0152-6",
    "genebass-paper.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9903662/",
    "genebass-phenotypes.json.gz": "https://main.genebass.org/api/phenotypes",
    "genebass-phenotype-qc.json.gz": "https://main.genebass.org/api/phenotypes/qc",
    "gnomad-v4.1.tsv": "https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1/constraint/gnomad.v4.1.constraint_metrics.tsv",
    "unknome-18_Mar_2026.tsv.gz": "https://unknome.mrc-lmb.cam.ac.uk/download/prot_tsv_gz/18_Mar_2026/",
    "pharos400.csv": "https://opendata.ncats.nih.gov/public/pharos/pharos400_tdls_canonicals.csv",
    "pharos-readme.html": "https://opendata.ncats.nih.gov/public/pharos/pharos400_readme.html",
    "gene2pubmed.gz": "https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz",
    "hgnc.tsv": "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt",
    "cncr-access.html": "https://cncr.nl/research/summary_statistics/",
    "unknome-access.html": "https://unknome.mrc-lmb.cam.ac.uk/download/",
    "ssgac-access.html": "https://thessgac.com/",
    "genebass-bulk-access.json": "https://storage.googleapis.com/storage/v1/b/ukbb-exome-public/o?delimiter=/",
    "schema-access.html": "https://schema.broadinstitute.org/",
    "metabrain-access.html": "https://www.metabrain.nl/",
    "gtex-access.json": "https://storage.googleapis.com/storage/v1/b/adult-gtex/o?delimiter=/&prefix=bulk-qtl/",
    "abc-access.xml": "https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/?list-type=2&delimiter=/&prefix=releases/",
    "ld-reference-access.html": "https://cncr.nl/research/magma/",
    "genebass-ui.js": "https://app.genebass.org/main-ed3ab9ea1857efb02221.js",
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def payload_sha(path):
    """Hash the JSON bytes, not the API's per-request gzip timestamp."""
    with path.open("rb") as f:
        compressed = f.read(2) == b"\x1f\x8b"
    if not compressed:
        return sha(path)
    h = hashlib.sha256()
    with gzip.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_one(name, url, previous):
    global RESERVED
    path = DATA / name
    old = previous.get(name)
    if path.exists() and old and old.get("sha256") == sha(path):
        return old  # cached bytes retain their original observation time/status
    row = {"file": name, "url": url, "observed_utc": datetime.now(timezone.utc).isoformat()}
    tmp = path.with_suffix(path.suffix + ".part")
    try:
        with httpx.Client(follow_redirects=True, timeout=120, headers={"User-Agent": UA, "Accept-Encoding": "identity"}) as client:
            with client.stream("GET", url) as r:
                row.update(http_status=r.status_code, final_url=str(r.url), content_type=r.headers.get("content-type"), last_modified=r.headers.get("last-modified"), etag=r.headers.get("etag"))
                # Reserve actual bytes, including responses whose length is absent.
                count = 0
                with LOCK:
                    if tmp.exists():
                        RESERVED -= tmp.stat().st_size
                with tmp.open("wb") as f:
                    for chunk in r.iter_raw():
                        with LOCK:
                            if RESERVED + len(chunk) > BUDGET:
                                raise RuntimeError("20 GB data budget exceeded")
                            RESERVED += len(chunk)
                        f.write(chunk)
                        count += len(chunk)
                with LOCK:
                    if path.exists():
                        RESERVED -= path.stat().st_size
                tmp.replace(path)
                row.update(bytes=count, sha256=sha(path), access="anonymous GET succeeded" if r.is_success else "unavailable; HTTP error response retained")
                api_json = name.startswith("genebass-") and name.endswith(".json.gz")
                if r.is_success and api_json:
                    row["payload_sha256"] = payload_sha(path)
                if r.is_success and old and old.get("http_status") == 200:
                    key = "payload_sha256" if api_json else "sha256"
                    expected = old.get("expected_" + key, old[key])
                    if row[key] != expected:
                        # Preserve the snapshot pin even on subsequent refetches.
                        # gzip envelope changes do not change the analysis input.
                        row.update(access="source changed since recorded snapshot")
                        row["expected_" + key] = expected
    except Exception as e:
        row.update(access="fetch failed", error=str(e))
        if tmp.exists():
            with LOCK:
                RESERVED -= tmp.stat().st_size
            tmp.unlink()
    print(name, row.get("http_status"), row.get("bytes"), row["access"], flush=True)
    return row


def run(sources, workers=4):
    global RESERVED
    DATA.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    manifest = OUT / "fetch-manifest.json"
    previous = {r["file"]: r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    RESERVED = sum(p.stat().st_size for p in DATA.rglob("*") if p.is_file())
    if RESERVED > BUDGET:
        raise RuntimeError("Existing data exceeds 20 GB")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(lambda item: fetch_one(*item, previous), sources.items()))
    previous.update({r["file"]: r for r in rows})
    manifest.write_text(json.dumps(sorted(previous.values(), key=lambda r: r["file"]), indent=2) + "\n")
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="*", help="Optional source filenames; default: all core sources")
    args = parser.parse_args()
    run({n: SOURCES[n] for n in args.names} if args.names else SOURCES)
