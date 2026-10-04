"""One-command public-data fetch and hypothesis join on the local machine."""
import json
from pypdf import PdfReader
import openpyxl

import fetch
import fetch_genebass
import join

SEMANTIC_ACCESS = {
    "ssgac-access.html": "HTTP 200 login/registration page; EA4 file list inaccessible anonymously; skipped",
    "genebass-bulk-access.json": "HTTP 400 requester-pays bucket; used anonymous per-phenotype browser API instead",
    "schema-access.html": "HTTP 200 JavaScript shell; download not established; schizophrenia is not cognition, skipped",
    "metabrain-access.html": "HTTP 200 homepage/access form; registration needed; eQTLs deferred",
    "gtex-access.json": "Anonymous bucket metadata only; eQTL analysis deferred",
    "abc-access.xml": "Anonymous release listing only; cell-expression analysis deferred",
    "ld-reference-access.html": "MAGMA/1000 Genomes reference download page only; no new LD analysis in this join",
}


def main():
    fetch.run(fetch.SOURCES)
    fetch_genebass.main()
    rows = json.loads((fetch.OUT / "fetch-manifest.json").read_text())
    join.tsv("access-inventory.tsv", [{"file": r["file"], "observed_utc": r["observed_utc"], "http_status": r.get("http_status", ""), "bytes": r.get("bytes", ""), "sha256": r.get("sha256", ""), "payload_sha256": r.get("payload_sha256", ""), "access_observed": SEMANTIC_ACCESS.get(r["file"], r["access"]), "requested_url": r["url"], "final_url": r.get("final_url", "")} for r in rows])
    # Small verbatim evidence excerpts for the threshold choices, not invented
    # p-values or thresholds. PDF page index 74 = printed supplementary page 73.
    pages = PdfReader(fetch.DATA / "lee-methods.pdf").pages
    w = openpyxl.load_workbook(fetch.DATA / "savage-supplement.xlsx", read_only=True, data_only=True)
    evidence = "Lee 2018 supplement, PDF page 75 / printed page 73:\n" + pages[74].extract_text() + "\n\nSavage 2018 Table S15 note:\n" + w["Table S15"]["A2"].value + "\n"
    (fetch.OUT / "source-method-excerpts.txt").write_text("\n".join(line.rstrip() for line in evidence.splitlines()) + "\n")
    join.main()


if __name__ == "__main__":
    main()
