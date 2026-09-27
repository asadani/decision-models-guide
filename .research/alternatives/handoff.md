# Alternatives: captured first-party evidence

Captured 2026-09-26. Source ledger is isolated in `sources.jsonl`; IDs below are local to this folder. No model execution or benchmark replication performed. Repository documentation is primary evidence of the interface contract, not independent validation of outcome claims. Read current snapshots rather than search snippets: SemIf recently added calibration, and Laya has new negation warnings.

| Claim | Source and locator | Exact short evidence |
|---|---|---|
| AnyJev L0 applies label-prior correction and cyclic option rotations, but this alone does not establish calibration. | s-001, `## L0: debiased, zero labels` | `it does not make the model's own uncertainty` |
| AnyJev L1 temperature scaling has a distribution-shift limit; it cannot repair wrong ranking. | s-001, `## L1: calibrated on labels` | `survive distribution shift beyond the calibration set` |
| Laya provides separate English, multilingual and typed-workflow checkpoints; its base checkpoints' zero-shot performance on typed-decisions must not be confused with the fine-tuned checkpoint. | s-002, `### Honest limits` | `The base checkpoints are near chance on typed-decisions zero-shot` |
| Laya's Jev-compatible request shape does not make confidence thresholds interchangeable: choice/score confidence uses entropy. | s-002, section beginning `Three things differ from Jev when you port a client` | `A threshold carried over from Jev does not transfer.` |
| GLiNER2.5-Decide is a 340M English classifier accepting labels at call time, with non-generative inference. | s-003, introduction | `The 340M English classification model in the GLiNER2.5 family.` |
| GLiNER2.5-Decide's card disclaims general-purpose reasoning, explanation and open-ended answering. | s-003, paragraph after benchmark | `It does not reason, explain, or answer open questions.` |
| SemIf is an independent implementation of a similar interface, not Jev's weights/training, and returns distributions conditioned on supplied options. | s-004, `## Input` | `Returned probabilities are conditional on the supplied options.` |
| SemIf now supports per-workload temperature scaling; calibrated output does not alter the chosen label. | s-004, `### Calibration` | `Calibration does not change the selected option.` |

These excerpts total <=25 quoted words per source. Paraphrases must remain faithful to the section, and tutorial discussion need not quote them verbatim.

## URLs and snapshots

- s-001: https://raw.githubusercontent.com/nokia-applied-research/AnyJev/main/docs/levels.md ; `.research/alternatives/snapshots/s-001.txt`
- s-002: https://raw.githubusercontent.com/NandhaKishorM/laya/main/README.md ; `.research/alternatives/snapshots/s-002.txt`
- s-003: https://huggingface.co/fastino/GLiNER2.5-Decide/raw/main/README.md ; `.research/alternatives/snapshots/s-003.txt`
- s-004: https://raw.githubusercontent.com/TheoLeeCJ/SemIf/master/README.md ; `.research/alternatives/snapshots/s-004.txt`

## Additional distinctions and caveats

- AnyJev is a readout/calibration toolkit over an existing LLM. L0 rotates K options at K prompt cost; L1 needs labeled examples of the same question; L2 fits a closed-form hidden-state head with labels and requires a hidden-state backend. Do not interpret the headline no-training claim as no fitting at every level. L0 batch-prior correction assumes a non-extreme class marginal; the source says it can hurt skewed tasks. L1 artifacts are tied to model, question and option layout.
- Laya is an encoder plus decision heads and router. The typed-workflow checkpoint is specialized. Defaults allocate a separate option budget, so many/long descriptions can be truncated into indistinguishable labels. Latest README documents narrow cancellation-negation failures, even with semantic label keys, including high confidence. This supports adding explicit negation tests; it does not support a universal failure claim.
- GLiNER2.5-Decide is schema-driven classification with single- and multi-label outputs. Model-card outputs are illustrative potential results, not evidence of a tested inference. Its English benchmark cannot settle multilingual quality. Do not compare its vendor aggregate with unrelated benchmark aggregates, and do not infer calibrated confidence merely from exposed confidence scores.
- SemIf uses frozen open model option-logit readout and can reuse the same state prefix across questions. It now supports workload-specific temperature calibration. Its published Jev row is imported from public records, not a live endpoint comparison, and the aligned subset is smaller than TypeSafe's full benchmark. Raw/quantized/runtime variants require separate validation.
- These main-branch URLs are mutable. Pin commit/model revisions for executable integrations. No assumption that similarly named third-party Jev/Laya websites are official.

## Verified API shapes (not executed)

GLiNER2.5-Decide's current card uses `from gliner2 import AutoExtractor`, `AutoExtractor.from_pretrained("fastino/GLiNER2.5-Decide")`, then `model.classify_text(text, {"intent": ["label_a", "label_b"]})`. Use that explicit card over auto-generated Hugging Face snippets, which can contain unrelated entity examples.

Laya's current README uses `from laya import Router`, `router = Router(preload=True)`, and `router.predict(state, questions)`. Its question mapping has `type`, `instructions`, and (for choice) a `criteria` mapping of labels to descriptions. Do not carry Jev confidence thresholds over.

SemIf's README provides a CLI `semif-score --mode direct --model Qwen/Qwen3.5-4B --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --input examples/decisions.jsonl --output results.jsonl`; input JSON rows contain `id`, `state`, `question`, and `options` with `id` and `description`. It requires installation from its repository. No claim the example ran here.
