"""Strict PersonaSpec 1.0 loader. No files, network, or canonical state are modified."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
STATUSES = frozenset({"synthetic", "fictional_canon", "reconstructed", "lived_record", "derived_hypothesis"})
ORIGINS = frozenset({"synthetic", "fictional_canon", "approved_export"})
GROUPS = ("traits", "values", "relationships", "commitments", "biography", "style")
ROOT = frozenset({"schema_version", "persona_id", "display_name", "origin_kind", "evidence", *GROUPS, "symbols"})
ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]{0,63}$")
SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")


class SpecError(ValueError):
    """Persona spec violates the frozen v1 contract."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _object(value: Any, label: str, allowed: set[str] | frozenset[str], required: set[str] | frozenset[str]) -> dict:
    if type(value) is not dict:
        raise SpecError(f"{label} must be an object")
    if missing := (set(required) - value.keys()):
        raise SpecError(f"{label} missing fields: {', '.join(sorted(missing))}")
    if extra := (value.keys() - set(allowed)):
        raise SpecError(f"{label} unknown fields: {', '.join(sorted(extra))}")
    return value


def _string(value: Any, label: str) -> str:
    if type(value) is not str or not value.strip() or "\x00" in value:
        raise SpecError(f"{label} must be a nonempty string without NUL")
    return value


def _id(value: Any, label: str) -> str:
    text = _string(value, label)
    if not ID_PATTERN.fullmatch(text):
        raise SpecError(f"{label} must match {ID_PATTERN.pattern}")
    return text


def _array(value: Any, label: str, nonempty: bool = False) -> list:
    if type(value) is not list or (nonempty and not value):
        raise SpecError(f"{label} must be {'a nonempty' if nonempty else 'an'} array")
    return value


def validate_spec(value: Any) -> dict:
    """Validate an entire specification; return the input object unchanged."""
    spec = _object(value, "PersonaSpec", ROOT, ROOT)
    if spec["schema_version"] != SCHEMA_VERSION:
        raise SpecError("unsupported schema_version")
    name = _string(spec["persona_id"], "persona_id")
    if not SLUG_PATTERN.fullmatch(name):
        raise SpecError("persona_id must be a lowercase slug, length 2 to 64")
    _string(spec["display_name"], "display_name")
    if spec["origin_kind"] not in ORIGINS:
        raise SpecError("invalid origin_kind")
    evidence_ids: set[str] = set()
    for n, record in enumerate(_array(spec["evidence"], "evidence", True)):
        obj = _object(record, f"evidence[{n}]", {"id", "source", "epistemic_status"}, {"id", "source", "epistemic_status"})
        eid = _id(obj["id"], f"evidence[{n}].id")
        if eid in evidence_ids:
            raise SpecError(f"duplicate evidence ID: {eid}")
        evidence_ids.add(eid)
        _string(obj["source"], f"evidence[{n}].source")
        if obj["epistemic_status"] not in STATUSES:
            raise SpecError(f"invalid epistemic status: {eid}")
        if spec["origin_kind"] == "synthetic" and obj["epistemic_status"] != "synthetic":
            raise SpecError("synthetic fixture may only assert synthetic evidence")
    proposition_ids: set[str] = set()
    for group in GROUPS + ("symbols",):
        for n, row in enumerate(_array(spec[group], group, group in ("traits", "values"))):
            loc = f"{group}[{n}]"
            allowed = {"id", "cue", "meaning", "evidence_ids"} if group == "symbols" else {"id", "text", "evidence_ids"}
            if group == "relationships":
                allowed.add("target_id")
            row = _object(row, loc, allowed, allowed - {"target_id"})
            pid = _id(row["id"], loc + ".id")
            if pid in proposition_ids:
                raise SpecError(f"duplicate proposition/symbol ID: {pid}")
            proposition_ids.add(pid)
            if group == "symbols":
                _string(row["cue"], loc + ".cue")
                _string(row["meaning"], loc + ".meaning")
            else:
                _string(row["text"], loc + ".text")
            if "target_id" in row:
                _id(row["target_id"], loc + ".target_id")
            links = _array(row["evidence_ids"], loc + ".evidence_ids", True)
            if len(links) != len(set(_id(x, loc + ".evidence_id") for x in links)):
                raise SpecError(f"{loc} has duplicate evidence references")
            unknown = set(links) - evidence_ids
            if unknown:
                raise SpecError(f"{loc} references unknown evidence: {', '.join(sorted(unknown))}")
    return spec


def load_spec(path: str | Path) -> dict:
    try:
        with open(path, encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SpecError(f"cannot read PersonaSpec: {exc}") from exc
    return validate_spec(value)
