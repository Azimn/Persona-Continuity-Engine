# M1 implementation and reproduction record

**Date:** 2026-10-08. **Package:** pce 0.1.0. **Status:** offline compiler committed. No model results.

The compiler is read-only, has no runtime dependencies or network calls, and consumes precisely validated source specifications. Four strategies preserve every evidence-bearing statement verbatim and all named cues with their explicit definitions. A packet includes origin, strategy, compiler version, cited source/proposition IDs, original spec hash, content hash, exact UTF-8 size and packet SHA-256.

Canonical hash bytes are Python json.dumps with sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False, encoded UTF-8 with no newline. The packet hash covers every field except the packet_sha256 field. Formatted JSON export bytes are not the hash input.

Reproduce on a clean checkout:

    python -m unittest discover -s tests -v
    python -m pce validate examples/meridian.json
    python -m pce validate examples/river.json
    python -m pce compile-all examples/meridian.json --out-dir output/meridian
    python -m pce compile-all examples/river.json --out-dir output/river

Tests include structural failure, duplicate and unlinked evidence rejection, synthetic evidence-class protection, literal content conservation, repeatability, tampering, CLI output and independent spec digest change.

**Interpretation limit:** Neither the compiler nor its hashes prove that a stated memory occurred. The schema checks author-supplied provenance consistency, not historical truth. Different frames have different token lengths and are not EXP-0001 information-matched conditions. No superiority claim follows from the package compiling successfully.

**M2 gate:** opt-in Ollama adapter with exact model/run manifest, failure records, local-only network boundary and no automatic model download. M3 evaluates restart/carryover under equal information budgets. Production adapters require explicit source-owner approval.
