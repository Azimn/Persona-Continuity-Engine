# M1 independent verification and reproducibility record

**Record date:** 2026-10-08 (America/Chicago). **Repository:** [Persona Continuity Engine](https://github.com/Azimn/Persona-Continuity-Engine). **Engineering implementation commit:** [08487bb4917995a5e03382eebeddf8a833fb589e](https://github.com/Azimn/Persona-Continuity-Engine/commit/08487bb4917995a5e03382eebeddf8a833fb589e).

## Provenance and chronology

The document-only foundation was committed first at [7c7645038cdfec0774535b9f32991342688e5359](https://github.com/Azimn/Persona-Continuity-Engine/commit/7c7645038cdfec0774535b9f32991342688e5359). Offline compiler implementation followed at [a875936a76b209d444cdfa695db7cf84c00c6e0f](https://github.com/Azimn/Persona-Continuity-Engine/commit/a875936a76b209d444cdfa695db7cf84c00c6e0f). Synthetic fixtures, tests, CI and reproduction documentation followed at commit 08487bb.

GitHub Actions [run 37874567188](https://github.com/Azimn/Persona-Continuity-Engine/actions/runs/37874567188) completed successfully for implementation commit 08487bb. Both jobs, [Python 3.11](https://github.com/Azimn/Persona-Continuity-Engine/actions/runs/37874567188/job/113640061853) and [Python 3.12](https://github.com/Azimn/Persona-Continuity-Engine/actions/runs/37874567188/job/113640062165), reported successful offline unit-test and deterministic output comparison steps.

The initial run validated Meridian compilation twice, compared their serialized outputs byte-for-byte, and validated both synthetic specs. The follow-up workflow update adds a River full compilation as well. That new workflow run requires separate completed CI evidence; this record must not misrepresent the earlier run as having tested it.

## Verification scope

Unit tests check twenty structural, read-only, CLI and hashing behaviors. Output comparison demonstrates repeatability for the specified fixture, interpreter and code revision. The hash field records source and packet byte identities using deterministic canonical serialization, not empirical proof that any fictional event happened.

**Not tested:** network providers, Ollama interoperability, inference quality, unseen-probe response reliability, cross-model migration, fresh-session carryover effectiveness, token-matched treatment controls, user data authorization, or integration with a production character brain.

## Release gate

M1 is an offline, installable package milestone only. Accepting M1 does not mean EXP-0001 showed a positive result, that narrative/symbolic prompting beats FACTUAL, or that a persistent identity exists inside model weights. M2 must implement an explicit local renderer port with independent tests and complete request/response provenance.
