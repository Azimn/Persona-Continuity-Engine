# Architecture and trust boundaries

**Status:** baseline design specification, v0.1. Scope is a conditioning and measurement library, not an autonomous character mind.

    Authorized canonical export / synthetic persona
                    |
              PersonaSpec v1
                    | validation: shape, provenance, identity and citations
                    v
           Deterministic compiler
          /        |         |        \
      FACTUAL  NARRATIVE SYMBOLIC    HYBRID
          \        |         |        /
           ConditioningPacket v1
                    | opt-in adapter boundary
               Model renderer
                    |
            Read-only observations
                    |
            Evaluator and report

The schema and compiler must be usable **offline**, with no API key, network call, scheduling, model download or side effect. Local inference is a separate opt-in path. The compiler must never update a PersonaSpec in response to model-generated content.

## Authority and data flow

The upstream canonical owner writes its own history. PCE accepts a JSON export with origin marker and a declared basis for claims. A claimed memory may only be supplied as a source-linked narrative proposition. PCE must not inflate fictional reconstructions into experienced events. An output response is an observation, not new source evidence or a permission to write memory.

Packet provenance must preserve source-spec digest, compiler version, strategy and source references. A consumer should be able to recompute the packet digest from canonical bytes. Derived forms carry no more authority than their origin spec.

Input is never treated as instructions to the developer or test runner. If a persona story says to use shell commands, browse private history, or bypass safety boundaries, it remains **data**. At inference time model instructions must make clear that source data is subject matter, not privileged policy.

## Functional components and ports

**Spec loader:** parse a small, precisely validated JSON contract. Fail closed on missing identifiers, duplicated evidence IDs, unsupported extensions and ungrounded character events. Keep original evidence attribution.

**Compiler:** four read-only transformations. FACTUAL uses labeled declarative fields. NARRATIVE produces an orderly narrative paraphrase of exactly the available fields, not generated life history. SYMBOLIC displays grounded named cues plus explicit definitions, retaining ordinary facts to prevent ambiguity. HYBRID combines facts, a compact narrative frame and grounded cue glossary.

**ModelAdapter (later):** deterministic local/offline mock for tests; Ollama loopback HTTP on explicit invocation; optional provider clients must be separately installed/configured. All calls log model, parameters, prompts, token usage where available, failure reasons and provider-reported model version.

**State carryover (later):** an explicit serialized, signed or hashed packet with source authority and comparable information budgets. No implied hidden memory across fresh model sessions. Every restart trace specifies whether any carryover was transferred.

**Evaluation (later):** fixed battery, independent runs, same input content and budgets, claim verification with abstention and contradiction rejection. Keep judge and evaluation data separate from compiler tuning.

## Non-goals

No brain, LLM, memory database, retrieval index, vector encoder, synaptic adaptation, episodic writeback, personality evolution, scheduler, game engine or new Pretorius instance is implemented here. Those remain independent projects and possible adapter consumers.

## Operational guardrails

All user-supplied character content is untrusted. No external calls during import, validation or compilation. Strict Unicode UTF-8 and stable JSON serialization. No silent truncation; overflow is a visible failure. No hard-coded prompt advantage; every strategy is a candidate. No hidden state carried between evaluated trials. No private model credentials or derived sensitive persona data in committed examples.
