# Milestones and acceptance gates

**M0: provenance and authority documentation.** Repository README, source pins, lineage table, data contract, trust boundaries, engineering benchmark, decision records and no-unverified-results notice. Gate: all links grounded to real repositories or pinned files and no claim of successful experiments.

**M1: offline working compiler.** Standard-library Python >=3.11, importable package, strict PersonaSpec validation, deterministic compile across four techniques, hash-linked ConditioningPacket, inspect/compile CLI, two synthetic example specs and offline unit tests. Gate: clean checkout tests pass; package can compile examples twice to identical bytes and hashes, unknown source references are refused and no external I/O is performed by compiler.

**M2: opt-in model access.** Add Ollama loopback adapter (no automatic network activity), mock adapter, model-config manifest, per-run raw logs and explicit CLI consent flag. Gate: mocked tests and opt-in local smoke tests; no model download or remote API default.

**M3: restart and evaluators.** Persisted explicitly authorized export, simple hash-verified carryover packet, deterministic run IDs, controlled fresh-session assays, independent offline scorer, full budget ledger. Gate: true blank restart versus carryover comparison, explicit equal budgets, no implied hidden persistence.

**M4: measured engineering pilot.** Two synthetic personas, two models, four arms, three starts/cell, twelve probes, 576 response slots if all cells execute. Gate: frozen independent probes, completed traces, rejection tests, per-model results, negative findings, published limitations.

**M5: optional adapters and transfer.** Opt-in stable read-only interfaces for The Doctor Lives/Kiki-Mind/other consumers, release and migration review by each canonical repository. No direct state writeback from renderer packets.

Every milestone requires a dated change note; a higher milestone is never silently inferred from code presence. The package may be released at M1 as a compiler without implying any measured persona advantage.
