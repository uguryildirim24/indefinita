"""Download all browser gene rows for explicitly defined cognitive measures."""
from urllib.parse import quote
from fetch import DATA, run
import gzip
import json

# The only continuous phenotypes in the browser's Cognitive function categories.
# Exclude categorical attempted-test status: participation is not performance.
PHENOTYPES = [
    "continuous-20016-both_sexes--irnt",
    "continuous-20018-both_sexes--",
    "continuous-20023-both_sexes--irnt",
    "continuous-20191-both_sexes--irnt",
]
MASKS = {"plof": "pLoF", "missense": "missense|LC", "combined": "pLoF|missense|LC"}
API = "https://main.genebass.org/api"


def load_json(path):
    raw = path.read_bytes()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw)


def main():
    metadata = {r["analysis_id"]: r for r in load_json(DATA / "genebass-phenotypes.json.gz")}
    observed = {r["analysis_id"] for r in metadata.values() if r["trait_type"] == "continuous" and "Cognitive function" in (r["category"] or "")}
    if observed != set(PHENOTYPES):
        raise RuntimeError(f"Cognitive phenotype inventory changed: {observed}")
    sources = {
        f"genebass-{p}-{m}.json.gz": f"{API}/analysis/{p}/gene-manhattan?burdenSet={quote(mask, safe='')}"
        for p in PHENOTYPES for m, mask in MASKS.items()
    }
    sources.update({f"genebass-gene-qc-{m}.json.gz": f"{API}/gene-qc/burden-set/{quote(mask, safe='')}" for m, mask in MASKS.items()})
    return run(sources)


if __name__ == "__main__":
    main()
