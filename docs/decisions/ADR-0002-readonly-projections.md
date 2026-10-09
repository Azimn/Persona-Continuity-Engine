# ADR-0002: Read-only, source-linked conditioning packets

**Decision date:** 2026-10-08. **Status:** accepted.

Input PersonaSpec records explicit source evidence, provenance class, relationships and commitments. Compilation is deterministic and read-only. It produces ConditioningPacket with a canonical spec hash, full provenance and technique identifier. Packets are disposable projections, never canonical state.

The initial compiler must avoid generative paraphrase, latent claims, inferred psychological backstory and implicit memory carryover. Every evidence-bearing proposition survives each transformation verbatim to make missing facts observable. External model replies cannot modify the spec. Only source-system-approved exports enter real character adapters.

Rejected: free-form LLM compression as the sole identity authority, hidden memory in a model service, treating answer style as an authenticated source, automatic import of existing agent memory stores.

Test: same spec yields the same compiled bytes; changing any source proposition changes the digest; unknown evidence IDs fail validation; all proposition texts occur in every output.
