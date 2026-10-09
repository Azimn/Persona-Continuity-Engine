"""Fail-closed SHA-256 check for the preregistered M3 fixture, answer keys, and rubric."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {"examples/meridian.json", "examples/river.json", "m3/probes.v1.json",
         "m3/rubric.v1.json", "m3/preregistration.v1.json"}

def verify() -> None:
    manifest = json.loads((ROOT / "m3/freeze.v1.json").read_text(encoding="utf-8"))
    rows = manifest["files"]
    paths = [row["path"] for row in rows]
    if len(rows) != 5 or len(set(paths)) != 5 or set(paths) != FILES:
        raise ValueError("freeze manifest paths incorrect, added, or missing")
    for row in rows:
        content = (ROOT / row["path"]).read_bytes()
        if len(content) != row["bytes"] or hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ValueError("M3 frozen artifact mismatch: " + row["path"])

if __name__ == "__main__":
    verify()
    print("M3 preregistration artifacts verified: 5 exact SHA-256 hashes")
