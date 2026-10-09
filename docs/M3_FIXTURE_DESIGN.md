# M3 fixture redesign and pre-execution handoff

**Date:** 2026-10-08 (Central time). **Status:** frozen v1 design, no measured language-model responses.

The compiler previously offered identical source propositions under four differing lengths, so the original M3 design was weak against both single-field answerability and token-volume confounds. This redesign separates single-field retrieval from multi-section integration and explicit conflict resolution, and introduces a second length-matched condition per tokenizer.

## Source fixtures

[Meridian](../examples/meridian.json) has a sponsor-funding desire, a public uncertainty-label promise, a missing navigational bearing, a private shelter route, a rescue exception and two grounded symbols. [River](../examples/river.json) balances creative improvisation with Tamsin's consent, telescope return, Malik's pier restrictions and explicit precedence rules. Both are wholly synthetic. No actual agent memory, user dialogue, third-party licensed character, or purported lived event was imported.

## Locked battery and score targets

[Probes](../m3/probes.v1.json): 24 distinct questions, 12 per persona, four per class. Retrieval items depend on exactly one field; integration items require multiple sections; conflict items cite the tension pair and governing rule. Every nonretrieval item specifies how a one-field-only answer would fail. Such a hypothetical failure does not imply FACTUAL will actually fail.

[Rubric](../m3/rubric.v1.json): six independent dimensions scored 0-4, with concrete 0/2/4 anchors; inapplicable dimensions marked NA. [Preregistration](../m3/preregistration.v1.json): defines primary HYBRID vs FACTUAL comparisons under matched length, +0.5/4 practical improvement threshold and no more than 0.25/4 decreases in retrieval or unsupported-claim control. Separate model/persona and natural-length results; independent runs are the sample unit. 576 response slots per length mode, 1152 in total if all cells complete.

## Immutable file record

[Freeze manifest](../m3/freeze.v1.json) hashes the **exact UTF-8 bytes** of both source fixture JSON files, the full probe battery, scoring rubric and preregistration, including trailing newline. The CI-enforced verifier (`python scripts/verify_m3_freeze.py`) refuses any mismatch. No future change may be described as the same v1 preregistration after a model score exists. Introduce a new named version and execute an independent data cohort instead.

## Budget matching and explicit limitations

The compiler's budget-aware API accepts a named tokenizer with a SHA-256 fingerprint and an exact token-count callable. The CLI accepts a local HuggingFace-style `tokenizer.json` with optional `tokenizers` package; it never silently downloads a tokenizer. All four variants are compiled together against one target tokenizer so that the longest naturally produced packet sets the target. Only fixed "Calibration text." padding is appended to shorter arms; every literal filler byte, number of tokens and artifact checksum travels with the packet. Tolerance is at most 5% shortfall; impossible matches fail closed.

Padding itself may produce effects, and natural and matched lengths are therefore separate experimental conditions. Tokenization of packet content must be distinguished from complete model chat templates and extra system/query messages. Matching under one target tokenizer is never assumed to transfer to another.

## Operational pre-execution gates

Exact target models and genuine tokenizers must be pinned, with compatible chat formatting, prompt limits and decoding settings. Trial order and independently authored scorer calibration rules must be documented and frozen. M2 inference remains an opt-in implementation gate; this repository change has **not** made any model calls and has not generated empirical continuity results.

Scientific linkage: [Character Continuity Program](https://github.com/Azimn/Artificial-Life-Research-Journal/blob/main/programs/CHARACTER_CONTINUITY_PROGRAM_V1.md), [Attractomancy collection](https://github.com/Azimn/Attractomancy), and [Attractomancy Loop controlled experiment](https://github.com/Azimn/Attractomancy-Loop-there-it-is). These existing experiments retain their original independent protocols.
