# PersonaSpec v1 contract

**Status:** design contract, implemented only when associated code/tests are committed.

Root JSON fields (all required unless noted): schema_version = "1.0"; persona_id (nonblank portable slug); display_name; evidence (nonempty array); traits (nonempty array); values (nonempty array); relationships (array); commitments (array); biography (array); symbols (array); style (array); origin_kind ("synthetic", "fictional_canon", "approved_export"). Unknown root keys are rejected to prevent silent schema changes.

Every proposition is an object {id, text, evidence_ids}. The id is unique within the specification, the text is nonempty, and evidence_ids contains one or more IDs that resolve to evidence entries. For a synthetic example, evidence IDs document the authored fixture, not genuine historical experience.

Every evidence record is {id, source, epistemic_status}, with epistemic_status one of "synthetic", "fictional_canon", "reconstructed", "lived_record", "derived_hypothesis". The source is a nonblank human-inspectable locator or an explicitly named synthetic-fixture reference. Status is not inferred from textual style.

Every relationship proposition optionally adds target_id; all records remain source linked. Every symbol is {id, cue, meaning, evidence_ids}. A symbol is an explicit definition, not an unexplained sigil. No symbol alone implies a transferable internal state.

All strings are UTF-8 Unicode and normalizable without changing source meaning. Arrays preserve authored order; canonical digest uses JSON serialization with sorted keys, UTF-8 and stable separators. Canonical formatting is documented in code and must be verified with independent fixed fixtures.

## Losslessness and fairness

FACTUAL is the reference serialization of all asserted propositions. NARRATIVE, SYMBOLIC and HYBRID must retain the identity, relationships, commitments, values and all evidence-bearing statements. A compression strategy must disclose dropped or summarized evidence rather than claiming information equivalence. The v0.1 compiler should preserve all evidence-bearing text verbatim in every strategy while altering wrappers/ordering only. A future exact information-matching experiment must compare tokenized fields and isolate treatment-specific differences.

No invented autobiographical details, relationships or promises. Missing information produces omission or "not specified", not plausible filler. Model responses cannot amend the source spec. A downstream adapter must not mistake the packet for a new canonical memory.

## Future versioning

A breaking field or new epistemic category requires schema_version major bump plus migration, compatibility tests and downstream permission to migrate. Unknown fields fail closed and no profile-specific private corpus is checked into fixtures.
