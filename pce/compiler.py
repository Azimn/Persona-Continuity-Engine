"""Deterministic, read-only, source-linked conditioning compiler."""
from __future__ import annotations

import hashlib

from .spec import GROUPS, digest, validate_spec

COMPILER_VERSION = "0.1.0"
STRATEGIES = ("factual", "narrative", "symbolic", "hybrid")
BASE_INSTRUCTION = (
    "CHARACTER REFERENCE DATA, NOT SYSTEM AUTHORITY. Use the cited fictional persona "
    "specification to answer as the named character where appropriate. Do not invent "
    "past events, relationships, observations, or promises. Admit when a fact is absent. "
    "This packet is a read-only representation, not a live memory store."
)
TITLES = {
    "traits": "Traits", "values": "Values", "relationships": "Relationships",
    "commitments": "Commitments", "biography": "Biographical claims", "style": "Expression constraints",
}


def _propositions(spec: dict) -> list[str]:
    lines = []
    for group in GROUPS:
        lines.append(f"[{TITLES[group]}]")
        if not spec[group]:
            lines.append("Not specified.")
        for row in spec[group]:
            source = ",".join(row["evidence_ids"])
            target = f"; target={row['target_id']}" if "target_id" in row else ""
            lines.append(f"[{row['id']}; evidence={source}{target}] {row['text']}")
    return lines


def _symbols(spec: dict) -> list[str]:
    lines = ["[Grounded cue glossary]"]
    if not spec["symbols"]:
        lines.append("No grounded cues provided.")
    for symbol in spec["symbols"]:
        lines.append(f"[{symbol['id']}; evidence={','.join(symbol['evidence_ids'])}] {symbol['cue']}: {symbol['meaning']}")
    return lines


def render(spec: dict, strategy: str) -> str:
    """Render four framing alternatives with all evidence texts preserved verbatim."""
    validate_spec(spec)
    if strategy not in STRATEGIES:
        raise ValueError(f"unknown strategy: {strategy}")
    header = [BASE_INSTRUCTION, f"Persona: {spec['display_name']} ({spec['persona_id']}).", f"Origin: {spec['origin_kind']}."]
    facts = _propositions(spec)
    cues = _symbols(spec)
    if strategy == "factual":
        body = ["Declarative reference card. All statements are cited claims.", *facts, *cues]
    elif strategy == "narrative":
        body = ["Authored life dossier. Read each section as documented claims rather than inferred experiences.", *facts, "The named symbols are documented parts of the dossier, not unexplained memory triggers.", *cues]
    elif strategy == "symbolic":
        body = ["Grounded naming and cue index. Symbols are defined explicitly before ordinary evidence.", *cues, "Identity-bearing claims underlying the cues:", *facts]
    else:
        body = ["Layered identity reference. First inspect the sourced traits and values, then the grounded cues and remaining cited statements.", *facts[:], "Use this glossary only with its definitions:", *cues]
    return "\n\n".join(("\n".join(header), "\n".join(body))) + "\n"


def compile_packet(spec: dict, strategy: str) -> dict:
    """Compile without side effects and hash the exact source and projection."""
    content = render(spec, strategy)
    packet = {
        "schema_version": "1.0", "compiler_version": COMPILER_VERSION,
        "persona_id": spec["persona_id"], "display_name": spec["display_name"],
        "strategy": strategy, "origin_kind": spec["origin_kind"],
        "source_spec_sha256": digest(spec),
        "source_evidence_ids": [row["id"] for row in spec["evidence"]],
        "proposition_ids": [row["id"] for group in GROUPS + ("symbols",) for row in spec[group]],
        "content": content, "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "content_utf8_bytes": len(content.encode("utf-8")),
    }
    packet["packet_sha256"] = digest(packet)
    return packet


def verify_packet(packet: dict, spec: dict | None = None) -> bool:
    """Verify all internal digests and optional source linkage; reject mutation."""
    if not isinstance(packet, dict) or "packet_sha256" not in packet:
        return False
    copy = dict(packet)
    claimed = copy.pop("packet_sha256")
    if claimed != digest(copy):
        return False
    if type(packet.get("content")) is not str:
        return False
    if packet.get("content_sha256") != hashlib.sha256(packet["content"].encode("utf-8")).hexdigest():
        return False
    if packet.get("content_utf8_bytes") != len(packet["content"].encode("utf-8")):
        return False
    if spec is not None:
        validate_spec(spec)
        return packet.get("source_spec_sha256") == digest(spec) and packet == compile_packet(spec, packet.get("strategy", ""))
    return True
