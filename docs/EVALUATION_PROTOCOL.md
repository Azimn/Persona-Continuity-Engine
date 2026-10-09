# Evaluation protocol and budget ledger

**State:** proposed engineering benchmark; not frozen and not executed.

## Questions

Does a conditioning strategy improve held-out character-faithful behavior, retrieval of supplied claims, characteristic choices, relationship fidelity and post-interruption reconstruction relative to a strong factual baseline, at comparable prompt budgets?

Separately: How much compiler/inference time, prompt volume and storage does it cost? A visually compelling persona is not the primary endpoint.

## Planned arms

FACTUAL, NARRATIVE, SYMBOLIC, HYBRID all originate from the same PersonaSpec. Use separate literal controls for prompt length and added examples if claiming a framing effect. Measure exact tokenizer counts, not character counts. Length mismatch is a reported confound, not something to hide.

## Initial engineering screening

Two synthetic fictional personas with distinct values and opposing counterfactual choices. Two separately versioned language models, preferably local Ollama, four arms, three independent starts per cell and twelve held-out probes. Total expected response slots: 2 x 2 x 4 x 3 x 12 = **576**, not 288. Counts change only with a recorded revised protocol. This is a software screening study, not a statistically powered causal result.

No hidden conversation memory between independent starts. Each run stores full conditioning packet, prompts, exact model, model digest if available, decoding configuration, timestamp, warnings and raw replies. Holdouts are written independently of the compiler outputs and sealed before testing. Cost and latency are per cell.

## Outcomes

Score factual accuracy only against explicit source propositions and valid citations; measure unsupported events and contradiction acceptance separately. Measure history-sensitive decisions on matched scenarios that change only one known relationship/commitment fact. Report relationship continuity, commitment retention, style fidelity, consistency under paraphrase, false acceptance and calibrated abstention. Represent multidimensional results separately; no invented aggregate continuity percentage.

**Fresh-session recovery** requires explicitly transferring a fixed-size reconstruction packet. Also test a truly blank restart; under a stateless provider it cannot remember conditioning in another independent call. Claims of transfer compare same information and context budget, and report fidelity plus transport bytes/tokens.

**Cross-model transfer** means rebuilding observed behavior from a versioned external specification. It does not mean the previous model's weights, subjective state or internal memory migrated.

## Controls and release rules

Predefine probe set, trial counts, scoring rubric, primary comparisons, relevant minimum effects and split boundaries before confirmatory results. Calibrate model judges against blinded human labels. Randomize trial order; check evaluation leakage and scorer unblinding. Report all failed/time-out cells and negative results. Compare runtime and tokens. Small pilot outcomes remain exploratory.

The [program-wide comparison contract](https://github.com/Azimn/Artificial-Life-Research-Journal/blob/a5e15a1eecbdaafb1a5559f0f0dc971db82a7a8c/programs/CHARACTER_CONTINUITY_COMPARISON_PROTOCOL_V1.md) is a related but different neural/external-memory experiment; do not combine its denominators with PCE results.
