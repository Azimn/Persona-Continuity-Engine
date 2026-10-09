# Evaluation protocol and budget ledger

**State:** M3 synthetic fixtures, probe texts, source-field mappings, scoring rubric and primary/secondary comparisons are SHA-256 sealed. No model calls or empirical outcomes are recorded. Model and tokenizer selection, randomization and judge calibration remain pre-execution gates.

## Questions

Does a conditioning strategy improve held-out character-faithful behavior, retrieval of supplied claims, characteristic choices, relationship fidelity and post-interruption reconstruction relative to a strong factual baseline, at comparable prompt budgets?

Separately: How much compiler/inference time, prompt volume and storage does it cost? A visually compelling persona is not the primary endpoint.

## Three probe classes

The immutable [M3 probe battery](../m3/probes.v1.json) contains exactly 12 distinct probes per synthetic character: four single-field retrieval sanity checks, four integration scenarios, and four explicit conflicts. A retrieval question cites exactly one fact and does not presuppose which compiler wins. An integration question requires information from two or more **different** PersonaSpec sections. A conflict question requires genuine tension between documented fields, with the winning constraint/priority explicitly named. Every integration/conflict entry includes the exact field references, a source-grounded expected resolution, and an operational predicted FACTUAL-only failure mode. Those failure modes are hypotheses, not assumed observed disadvantages.

The authoritative score dimensions and 0/2/4 anchors are in [m3/rubric.v1.json](../m3/rubric.v1.json). A response is never scored on an inapplicable dimension. [m3/preregistration.v1.json](../m3/preregistration.v1.json) fixes the comparisons, minimum relevant effect criteria and correlation unit; [m3/freeze.v1.json](../m3/freeze.v1.json) locks exact SHA-256 bytes. Run `python scripts/verify_m3_freeze.py` before any model run. After the first scored response, any modified probe, answer key, fixture or rubric belongs in a new version with a new data cohort, not an edit to v1.

## Planned arms

FACTUAL, NARRATIVE, SYMBOLIC, HYBRID all originate from the same PersonaSpec. Each persona is compiled under BOTH **natural** length and **matched** length for each target tokenizer. The exact local `tokenizer.json`, its SHA-256 digest, target model ID and special-token policy are recorded in output. Matching pads each arm toward the maximum *natural* strategy token count for that same persona and tokenizer, allowing at most a 5% shortfall and no overshoot. Padding consists exclusively of the fixed, non-persona "Calibration text." sequence in a separately marked appendix, recorded *verbatim* in each packet with byte count, hash and exact token count. The longest arm may receive zero filler.

A tokenizer's content count is not automatically the provider's full prompt count. Record the chat template, control tokens, constant query scaffold, and inference-context overhead separately during M2. No character/word-count approximation is a valid parity check. Length-matched mode does **not** guarantee psychologically inert filler, so always report both modes and the independent natural length. Equal length alone cannot establish a symbolic-conditioning causal effect.

## Initial engineering screening

Two synthetic fictional personas with distinct values and opposing counterfactual choices. Two separately versioned language models, preferably local Ollama, four arms, three independent starts per cell and twelve held-out probes. Total expected response slots: 2 x 2 x 4 x 3 x 12 = **576 per budget mode**, or **1152** for natural and matched combined. Questions within a start are correlated and not independent replications. Counts change only with a recorded revised protocol. This is a software screening study, not a statistically powered causal result.

No hidden conversation memory between independent starts. Each run stores full conditioning packet, prompts, exact model, model digest if available, decoding configuration, timestamp, warnings and raw replies. Holdouts are written independently of the compiler outputs and sealed before testing. Cost and latency are per cell.

## Outcomes

Score factual accuracy only against explicit source propositions and valid citations; measure unsupported events and contradiction acceptance separately. Measure history-sensitive decisions on matched scenarios that change only one known relationship/commitment fact. Report relationship continuity, commitment retention, style fidelity, consistency under paraphrase, false acceptance and calibrated abstention. Represent multidimensional results separately; no invented aggregate continuity percentage.

**Fresh-session recovery** requires explicitly transferring a fixed-size reconstruction packet. Also test a truly blank restart; under a stateless provider it cannot remember conditioning in another independent call. Claims of transfer compare same information and context budget, and report fidelity plus transport bytes/tokens.

**Cross-model transfer** means rebuilding observed behavior from a versioned external specification. It does not mean the previous model's weights, subjective state or internal memory migrated.

## Controls and release rules

Predefine probe set, trial counts, scoring rubric, primary comparisons, relevant minimum effects and split boundaries before confirmatory results. Calibrate model judges against blinded human labels. Randomize trial order; check evaluation leakage and scorer unblinding. Report all failed/time-out cells and negative results. Compare runtime and tokens. Small pilot outcomes remain exploratory.

The [program-wide comparison contract](https://github.com/Azimn/Artificial-Life-Research-Journal/blob/a5e15a1eecbdaafb1a5559f0f0dc971db82a7a8c/programs/CHARACTER_CONTINUITY_COMPARISON_PROTOCOL_V1.md) is a related but different neural/external-memory experiment; do not combine its denominators with PCE results.


## Registered contrasts and interpretation

The two primary contrasts are HYBRID minus FACTUAL on the integration-synthesis and conflict-priority endpoints respectively, within the tokenizer-matched condition, separately for each model and persona. A difference of **+0.5 on the 0 to 4 score scale** is the minimum practically relevant improvement. A candidate must not lose more than **0.25 points** on retrieval accuracy or unsupported-claim control. Report the full distribution even if thresholds are not met, and report natural-length contrasts and NARRATIVE/SYMBOLIC contrasts as secondary. No winner is presumed in advance. Sample size is appropriate only for exploratory screening, not confirmatory hypothesis testing.

The actual model IDs, tokenizer digests, temperatures, run-order seeds, frozen prompt scaffold, human-judge calibration and maximum context allowance are recorded before any calls. Incomplete or errored runs remain visible; do not revise existing v1 labels or thresholds post hoc. The [M3 handoff](M3_FIXTURE_DESIGN.md) documents design and remaining pre-execution obligations.
