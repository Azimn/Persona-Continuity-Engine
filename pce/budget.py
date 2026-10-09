"""Exact-token, model-specific, explicitly neutral padding for conditioning packets.

No tokenizer guesses. A tokenizer is a verified callable with a stable artifact digest.
Each call matches the longest natural strategy for ONE PersonaSpec and ONE tokenizer.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Callable

from .compiler import STRATEGIES, compile_packet, verify_packet
from .spec import digest, validate_spec

PADDING_PREFIX = "\n\n[NON-PERSONA LENGTH-CONTROL MATERIAL]\n"
PADDING_UNIT = "Calibration text. "
MAX_UNITS = 4096
BUDGET_VERSION = "1.0"


class BudgetError(ValueError):
    """Cannot establish exact token parity without changing source facts."""


@dataclass(frozen=True)
class TokenizerProfile:
    tokenizer_id: str
    artifact_sha256: str
    count: Callable[[str], int]
    special_token_policy: str = "disabled"

    def tokens(self, value: str) -> int:
        result = self.count(value)
        if type(result) is not int or result < 0:
            raise BudgetError("tokenizer must return a nonnegative exact integer")
        return result


def load_local_tokenizer_json(path: str | Path, tokenizer_id: str) -> TokenizerProfile:
    """Load a local tokenizer.json with the optional 'tokenizers' dependency.

    No download or network access, no implicit chat-template adjustment.
    The caller must independently confirm compatibility with its target model.
    """
    if not tokenizer_id or not tokenizer_id.strip():
        raise BudgetError("target tokenizer identifier required")
    file = Path(path)
    raw = file.read_bytes()
    try:
        from tokenizers import Tokenizer
    except ImportError as exc:
        raise BudgetError("install optional local dependency: pip install '.[tokenizer]'") from exc
    tokenizer = Tokenizer.from_file(str(file))
    return TokenizerProfile(
        tokenizer_id=tokenizer_id,
        artifact_sha256=hashlib.sha256(raw).hexdigest(),
        count=lambda text: len(tokenizer.encode(text, add_special_tokens=False).ids),
    )


def _decorated(base: dict, content: str, profile: TokenizerProfile,
               natural: int, target: int, padding: str, mode: str, tolerance: float) -> dict:
    packet = dict(base)
    content_bytes = content.encode("utf-8")
    final_tokens = profile.tokens(content)
    packet.update({
        "content": content,
        "content_sha256": hashlib.sha256(content_bytes).hexdigest(),
        "content_utf8_bytes": len(content_bytes),
        "budget_version": BUDGET_VERSION,
        "budget_mode": mode,
        "tokenizer_id": profile.tokenizer_id,
        "tokenizer_sha256": profile.artifact_sha256,
        "special_token_policy": profile.special_token_policy,
        "natural_tokens": natural,
        "target_tokens": target,
        "final_tokens": final_tokens,
        "tolerance": tolerance,
        "padding_text": padding,
        "padding_sha256": hashlib.sha256(padding.encode("utf-8")).hexdigest(),
        "padding_utf8_bytes": len(padding.encode("utf-8")),
    })
    packet.pop("packet_sha256", None)
    packet["packet_sha256"] = digest(packet)
    return packet


def _pad_to_target(text: str, profile: TokenizerProfile, target: int, tolerance: float) -> str:
    lower_bound = target * (1 - tolerance)
    existing = profile.tokens(text)
    if existing > target:
        raise BudgetError("a natural strategy exceeded the target tokenizer maximum")
    if existing >= lower_bound:
        return ""
    best = None
    overshoots = 0
    for repetitions in range(1, MAX_UNITS + 1):
        filler = PADDING_PREFIX + PADDING_UNIT * repetitions
        observed = profile.tokens(text + filler)
        if lower_bound <= observed <= target and (best is None or observed > best[0]):
            best = (observed, filler)
            if observed == target:
                break
        if observed > target:
            overshoots += 1
            if overshoots >= 8:
                break
    if best is None:
        raise BudgetError("no neutral-padding construction meets exact token tolerance")
    return best[1]


def compile_budget_set(spec: dict, profile: TokenizerProfile, *,
                       mode: str, tolerance: float = .05) -> dict[str, dict]:
    """Return all four packets matched per actual tokenizer, or natural packets with counts.

    Matching is deliberately one tokenizer at a time; packet provenance cannot be
    reused as a parity certificate for another model family.
    """
    validate_spec(spec)
    if mode not in ("natural", "matched"):
        raise BudgetError("mode must be natural or matched")
    if not 0 < tolerance <= .05:
        raise BudgetError("tolerance must be greater than 0 and no more than 5%")
    if not profile.tokenizer_id.strip() or len(profile.artifact_sha256) != 64 or any(c not in "0123456789abcdef" for c in profile.artifact_sha256):
        raise BudgetError("exact tokenizer identifier and SHA-256 required")
    if profile.special_token_policy != "disabled":
        raise BudgetError("v1 content-token count requires special-token policy disabled")
    base = {s: compile_packet(spec, s) for s in STRATEGIES}
    natural = {s: profile.tokens(p["content"]) for s, p in base.items()}
    target = max(natural.values())
    if target <= 0:
        raise BudgetError("tokenizer returned empty content")
    result = {}
    for strategy, original in base.items():
        pad = _pad_to_target(original["content"], profile, target, tolerance) if mode == "matched" else ""
        content = original["content"] + pad
        packet = _decorated(original, content, profile, natural[strategy], target, pad, mode, tolerance)
        if mode == "matched" and not target * (1 - tolerance) <= packet["final_tokens"] <= target:
            raise BudgetError("target tokenizer parity was not established")
        result[strategy] = packet
    return result


def verify_budget_set(packets: dict, spec: dict, profile: TokenizerProfile) -> bool:
    """Strict source, tokenizer, filler, byte and result-set verification."""
    try:
        if set(packets) != set(STRATEGIES):
            return False
        modes = {packet["budget_mode"] for packet in packets.values()}
        tolerances = {packet["tolerance"] for packet in packets.values()}
        if len(modes) != 1 or len(tolerances) != 1:
            return False
        mode, tolerance = next(iter(modes)), next(iter(tolerances))
        expected = compile_budget_set(spec, profile, mode=mode, tolerance=tolerance)
        return all(verify_packet(packets[s]) and packets[s] == expected[s] for s in STRATEGIES)
    except (ValueError, KeyError, TypeError, AttributeError):
        return False
