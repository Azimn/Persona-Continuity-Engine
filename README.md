# Persona Continuity Engine (PCE)

**Status: v0.1 foundation under development. No claim of validated cross-model persona continuity.**

PCE is a small, inspectable Python engine that transforms an authorized, source-grounded character specification into model-specific conditioning packets. It compares ordinary declarative prompts, narrative forms, symbolic cue forms and explicit hybrid packaging. Its goal is portable, measurable **behavioral reconstruction**, not a new cognitive brain, consciousness transfer, or permanent identity in language-model weights.

## Origin and research lineage

This is the engineering branch of a cumulative **Character Continuity Research Program**. It is intentionally not a competing Pretorius, Kiki, Calibos, or game NPC brain. Their canonical events, decisions, memories, relationships, and lived state remain owned by their respective systems. PCE may ingest an **approved, redacted, immutable export** through an adapter and emit renderer instructions. It must never acquire write authority over a subject's history or state.

The lineage is documented with verified repository pins in [docs/LINEAGE.md](docs/LINEAGE.md) and the machine-readable [source pins](research/source_pins.json). The precise mainline branches and reports can move; the dated pins preserve what was inspected at project inception.

[Attractomancy](https://github.com/Azimn/Attractomancy) established the observational archive of ritualized persona techniques, symbolic cues, staged induction, autobiographical framing and reconstruction procedures. Its collection does not demonstrate their efficacy. [Attractomancy Loop, EXP-0001](https://github.com/Azimn/Attractomancy-Loop-there-it-is/tree/f84d5453d6e628988a71a22d3decb122be6fd0de/experiments/EXP-0001) tests information-matched ritualized conditioning independently; at this snapshot it has no verified model outcomes. PCE can use its hypotheses and benchmarking lessons, but does not import a ritual advantage as fact.

[Artificial Life Research Journal](https://github.com/Azimn/Artificial-Life-Research-Journal/blob/a5e15a1eecbdaafb1a5559f0f0dc971db82a7a8c/programs/CHARACTER_CONTINUITY_PROGRAM_V1.md) is the umbrella scientific chronology and evidence authority, including [the evidence register](https://github.com/Azimn/Artificial-Life-Research-Journal/blob/a5e15a1eecbdaafb1a5559f0f0dc971db82a7a8c/programs/CHARACTER_CONTINUITY_EVIDENCE_REGISTER_V1.md) and [comparison protocol](https://github.com/Azimn/Artificial-Life-Research-Journal/blob/a5e15a1eecbdaafb1a5559f0f0dc971db82a7a8c/programs/CHARACTER_CONTINUITY_COMPARISON_PROTOCOL_V1.md). This engine reports its own raw outputs there via pinned references; it does not convert an engineering demonstration into a scientific replication.

[The Doctor Lives](https://github.com/Azimn/The-Doctor-Lives) is the definitive production Pretorius brain and retains evidence/persistence authority. [Kiki-Mind](https://github.com/Azimn/Kiki-Mind) demonstrated the canonical ledger versus disposable projection boundary. [Calibos Mind](https://github.com/Azimn/calibos-mind), [DUCK](https://github.com/Azimn/DUCK), and [Persona and Jelly Sandwich](https://github.com/Azimn/Persona-and-Jelly-Sandwich-) explore endogenous cognition and renderer-independent subjective state. PCE cannot replace any of those mechanisms. [Bicentennial-Man](https://github.com/Azimn/Bicentennial-Man) contributes fixed-boundary evaluation lessons. [Pretorius Neural Network](https://github.com/Azimn/Pretorius-Neural-Network) and [Pretorius Connectome](https://github.com/Azimn/Pretorius-Connectome) demonstrate why decoder behavior, retrieval, and learned substrate effects must be measured separately. [Frankenstein Village](https://github.com/Azimn/frankenstein-village) is a possible future low-cost NPC consumer, not an initial integration.

## Contract and experiment

**Input:** validated PersonaSpec v1 with explicitly classified fictional/canonical/derived fields, source evidence IDs, motivations, relationships, constraints and optional authorized expression examples.

**Compiler:** deterministic serialization to four strategies: FACTUAL, NARRATIVE, SYMBOLIC and HYBRID. Strategies change *representation*, not authority. A symbol is a cue grounded in explicit definitions, not evidence that an internal latent state persists.

**Output:** versioned, source-hashed ConditioningPacket with source IDs, strategy, full generated text and traceability. The packet is read-only. Future model adapters may send this text to a local Ollama endpoint or opt-in commercial API, never by default.

**Evaluation:** identical persona evidence and held-out cases, fresh processes and independent runs, task-level scores and costs, intervention-specific ablations, true and absent-memory tests. A stateless restart receives nothing unless an explicitly specified carryover packet is passed to it. Comparable carryover budgets are mandatory for comparative recovery claims.

Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md); contract: [docs/PERSONA_SPEC_V1.md](docs/PERSONA_SPEC_V1.md); evaluation: [docs/EVALUATION_PROTOCOL.md](docs/EVALUATION_PROTOCOL.md); claims and gates: [docs/RESEARCH_BOUNDARIES.md](docs/RESEARCH_BOUNDARIES.md).

## Initial development path

Documentation and review precede executable changes. Milestone M0 freezes the provenance contract. M1 provides a dependency-free Python package, two **synthetic** examples, schema validation, deterministically compiled condition text, hashes, CLI and offline tests. M2 adds opt-in local Ollama inference with recorded model IDs and run manifests. M3 adds blinded controlled comparisons, explicitly externally stored restart packets, and a first measured report. See [roadmap](docs/ROADMAP.md) and [decisions](docs/decisions/ADR-0001-separate-engine.md).

Production transfers into The Doctor Lives, Kiki-Mind, Calibos or Frankenstein Village require explicit, independently reviewed adapters and each destination's own release tests. No source memory, unlicensed corpus or personal dialogue is vendored here.

## Reproduction and status

Requires Python 3.11 or newer. The initial foundation uses Python standard library only. After the first implementation commit, run tests with: python -m unittest discover -s tests -v . Detailed CLI commands and verified test outcomes must be added only after those artifacts exist.

The current repository is not presented as an installable, evaluated product until its corresponding executable milestone is committed and audited. Track deliverable completion in [docs/CHANGELOG.md](docs/CHANGELOG.md).

License: not yet selected. Do not assume permission to incorporate third-party code, original persona corpora or externally supplied character biographies.
