# Change log and research handoff

## 2026-10-08, M0 documentation baseline

Established independent project scope, canonical source ownership, verified upstream repository commit pins, PersonaSpec v1 data contract, four conditioning strategies, research and measurement limits, roadmap and architectural decisions. These are specifications, not empirical findings.

Engineering start is tracked separately. Any successful tests or implemented functionality must be recorded in a subsequent entry only after code and test evidence are committed.

## 2026-10-08, M1 offline compiler foundation

Introduced PersonaSpec v1 structural checks; deterministic FACTUAL, NARRATIVE, SYMBOLIC and HYBRID packets with SHA-256 linkage; verify_packet, CLI, Python packaging, two synthetic fixtures, twenty offline unit tests and dual-version GitHub Actions CI. Local unit tests passed before commit; repository CI must be confirmed separately.

The four strategies preserve sourced text but are not token-length matched. No cross-model outcomes or memory resurrection are claimed. See [M1 implementation](M1_IMPLEMENTATION.md).

## 2026-10-08, M1 independent CI verification and workflow refinement

Confirmed green repository CI on commit 08487bb under Python 3.11 and 3.12, with raw [run link](https://github.com/Azimn/Persona-Continuity-Engine/actions/runs/37874567188). Refined the CI smoke test to compile the second synthetic character as well, corrected README invocation text, and published a bounded verification record. Await a new CI result before claiming the refined workflow passed.

## 2026-10-08: M3 fixture redesign and budget matching

Revised both synthetic fixture personas with multi-section promises and explicit priority rules; registered 24 field-linked retrieval, integration and conflict probes and all expected answers, predicted single-field failure mechanisms and anchored score dimensions. Pinned preregistration and its five source artifacts using exact SHA-256; added independent hash verifier, tokenizer-aware budget parity compiler, optional local tokenizer.json loader and CLI natural/matched modes, plus offline tests. No model calls or outcome scores were made. Refer to [M3 design](M3_FIXTURE_DESIGN.md).
