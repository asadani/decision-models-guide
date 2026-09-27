# Independent claim entailment audit

Audited 2026-09-26. Scope: all 29 statements in claims.jsonl against their bound snapshots, including surrounding passages. This is a semantic source-entailment audit, not experimental reproduction or validation of vendor performance. PASS means the source supports the statement within its stated scope. No ledger or snapshot was modified.

Result: **29 PASS, 0 FAIL.** Several locator excerpts are narrower than their claims. Their surrounding source text supports the complete statements; the binding improvements below would make automated quote verification more informative.

| Claim | Verdict | Supporting context and limits |
|---|---|---|
| c-001 | PASS | s-006 defines Choice as selecting one option from a defined set; the request criteria and examples establish caller-supplied options. |
| c-002 | PASS | s-008 lines 7 and 240 explicitly define the returned value as probability of yes. This is API semantics, not proof of calibration on every workload. |
| c-003 | PASS | s-007 line 7 and rubric examples establish ordered descriptive levels. |
| c-004 | PASS | s-009's opening prose and “Confidence is derived from the probabilities” section establish both clauses. Confidence summarizes distribution shape; do not equate it with calibrated correctness probability. |
| c-005 | PASS | s-010's training approaches section expands RLCD; the calibration section explicitly limits frequency interpretation to groups. The statement accurately attributes the training terminology to TypeSafe. |
| c-006 | PASS | s-004 line 188 explicitly calls the number non-empirical and attributes 0% to guaranteed schema matching. No support for zero task error is implied. |
| c-007 | PASS | s-011 covers numeric precision (lines 13, 68, 76), adversarial content (106), and cross-question invariance (116–137), specifically for Jev 1.13. |
| c-008 | PASS | s-014 Aliases section says aliases move with releases and advises pinning after threshold tuning. |
| c-009 | PASS | s-005 lines 38 and 46 explicitly give the POST endpoint. This is documentation as captured, not a connectivity test. |
| c-010 | PASS | s-012 ScoreAnswer.score description gives the probability-weighted average and allows values between integer levels. |
| c-011 | PASS | s-015's v0.6.0 breaking changes establishes the ordered-sequence change. Scope is the Python SDK; add “Python” for precision. |
| c-012 | PASS | s-021 L0 limitations explicitly say debiasing does not calibrate the model's uncertainty and an overconfident model remains overconfident. |
| c-013 | PASS | s-021 L1 limitations explicitly warn against surviving distribution shift beyond the calibration set. This is the project's warning about L1, not a proof that every possible shifted distribution must fail. |
| c-014 | PASS | s-022 line 449 explicitly says the Jev threshold does not transfer, explaining that Laya uses normalized entropy. Do not adopt Laya's description of Jev's exact formula as independently verified official behavior. |
| c-015 | PASS | s-022 lines 943–946 distinguish near-chance base zero-shot scores from the checkpoint trained on that benchmark's own training split. Maintainer-reported comparison only. |
| c-016 | PASS | s-023 line 39 explicitly identifies a 340M English classification model. |
| c-017 | PASS | s-024 line 184 explicitly makes probabilities conditional on supplied options and calls for workload validation. |
| c-018 | PASS | s-024 lines 160–168 describe labeled per-workload temperature scaling and unchanged option selection. Source does not establish significant improvement on every workload. |
| c-019 | PASS | s-002 line 86 establishes encoder and adapted Qwen branches; line 265 says local interfaces exist while native integration remains planned in that release. |
| c-020 | PASS | s-033 lines 51–53 explicitly distinguish JevK5, an open reproduction, from TypeSafe Jev. The internal benchmark cannot support a claim that GLiNER beats TypeSafe Jev. |
| c-021 | PASS | s-033 line 73 distinguishes extraction offsets from classification answers and explicitly says classifications do not return evidence spans. |
| c-022 | PASS | s-020 embedded lines L102–L108 describe 100 calls times four labels, 400 decisions, 337 judge-agreed retained decisions, and exclusion of 63 cases with unclear rules. This is model-judge agreement, not human-established ground truth. |
| c-023 | PASS | s-020 embedded L131–L139 describe five repeated/permuted runs and the quoted label stability, probability drift, and option-order sensitivity. Keep attribution and sample scope. |
| c-024 | PASS | s-027 lines 1048–1057 give the threshold-routing procedure and 84 fixes versus 211 introduced errors; nearby table identifies the confidence field at exactly 1.00. This is the supplied author's report, not independently replicated evidence. |
| c-025 | PASS | s-028 lines 6–8 explicitly label a synthesis and independent compilation with no affiliation or endorsement. |
| c-026 | PASS | s-019 lines 133–145 name all four functions and describe their activity organization. These are not necessarily sequential steps or a checklist; Govern is cross-cutting. |
| c-027 | PASS | s-017 abstract describes supervised demonstrations and subsequent reinforcement learning from human feedback, naming resulting models InstructGPT. |
| c-028 | PASS | s-018 abstract explicitly describes reinforcement learning that incentivizes reasoning. The broad statement does not overclaim a specific training recipe. |
| c-029 | PASS | s-016 abstract explicitly studies neural network calibration and temperature scaling. No claim of inventing temperature scaling is made. |

## Exact wording and binding improvements

No semantic correction is required to pass the audit. Recommended precision edits:

- c-011: “Python SDK version 0.6.0 changed Score criteria to an ordered sequence.” The cited changelog does not establish all language SDKs used that version.
- c-013: “AnyJev warns that its L1 calibration does not generally survive distribution shift beyond its calibration set.” This makes the section's scope explicit.
- c-024: “In Nhu Hoang's supplied Banking77 experiment, retaining Jev answers with confidence reported as exactly 1.00 and routing the rest to Qwen fixed 84 errors but introduced 211.” This disambiguates which group gets forwarded.

Recommended locator improvements (the currently bound sources are already sufficient):

- c-004: add the s-009 sentence beginning “`confidence` is a statistic computed from the probability distribution” to support the first clause.
- c-005: add s-010's RLCD expansion or the “TypeSafe's training path is RLCD” sentence.
- c-007: bind the numeric precision and adversarial-content passages in addition to the structural-invariance passage.
- c-018: add s-024's “SemIf includes per-workload temperature scaling fitted on labeled decisions” sentence.
- c-019: add s-002 line 86 on the two architectural branches.
- c-022: include the preceding sentence giving 100 calls and 400 decisions.
- c-023: extend the locator through the option-order clause.
- c-026: replace the one-word GOVERN locator with the s-019 passage naming all four functions (lines 136–139 or 143–145).
- c-027: use the abstract sentence explicitly linking fine-tuning with human feedback and InstructGPT, rather than the generic phrase “human feedback.”
- c-028: use the abstract sentence stating that reasoning abilities can be incentivized through reinforcement learning.
- c-029: use the abstract's calibration definition together with its temperature-scaling finding.

Encoding note: displayed mojibake exists in some captured TypeSafe text and the c-020 locator. The JevK5 distinction is clear in the source; preserve snapshot bytes and use an ASCII-only distinctive excerpt or a line locator when improving the binding, rather than silently editing evidence.
