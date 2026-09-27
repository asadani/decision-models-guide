# Final independent tutorial review

Reviewed 2026-09-26: tutorial/decision-models.md, all three examples/*.py files, .research/verification-report.md, and relevant captured SDK/source passages. No tutorial, code, ledger, or snapshot edits made. This review did not install dependencies, run the live API, or reproduce vendor benchmarks.

Verdict: **PASS with small teaching and provenance corrections recommended.** No material unsupported vendor-performance assertion, citation mismatch, or executable unsafe policy action was found. The existing gate PASS means structural evidence binding passed; it is not a runtime integration or model-quality certification.

## Concrete corrections

1. **Section 6, synthetic threshold interpretation — clarify the rejected `other` case.** The reported 5/6 overall accuracy, three automatically routed cases, and one routed error are correct. However, the 0.8 routing policy also rejects the confidently correct `other` case. Replace the two sentences starting “But at the demonstration policy threshold” with: “At the demonstration policy threshold of 0.8, only three cases automatically route, and one is wrong; the policy also sends the correctly predicted `other` case to review. A probability-only cutoff would retain four cases with three correct. Both accepted accuracies are lower than the unfiltered five-of-six accuracy in this constructed example.” This separates the threshold effect from the action-class/taxonomy rule.

2. **Figure 3 — apply the same validation/policy boundary on both branches.** The diagram validates fallback outputs explicitly but sends accepted primary outputs directly to joined outcomes. Route `A[Primary decision]` to `V[Validate against same schema and policy]` and remove `A --> J`; both branches can then proceed through `H` and `J`. The surrounding text/code are safe already; this removes an avoidable visual ambiguity when readers reuse the cascade design.

3. **Section 4 and validation disclosure — distinguish compilation from SDK validation.** Replace “The code was syntax-checked against captured documentation” with “The code passed a Python syntax check, and its interface was compared with captured SDK documentation. The SDK dependency was not installed, and no live API request was made.” Syntax checking does not resolve imports or check constructor compatibility. The captured s-013 constructor and s-012 response accessors do support the written interface.

4. **Section 11, step 4 — narrow the calibration-only instruction.** Change “Tune only on calibration data” to “Tune thresholds and probability calibration only on calibration data.” Section 6 correctly reserves development data for wording/taxonomy; the broader instruction could accidentally suggest doing all model/prompt development on the calibration split.

5. **Section 4 package version — attach the existing source.** Link `typesafe-sdk==0.7.1` to the captured Python changelog or cite s-015 through an expanded claim. Its v0.7.1 release entry exists; no fresh discovery is required. This is a provenance improvement, not a factual defect.

## Metric and policy consistency

Independent arithmetic inspection of the six synthetic rows gives:

| Quantity | Expected value |
|---|---:|
| Accuracy | 5/6 = 0.833333... |
| Majority baseline | 3/6 = 0.5 |
| Macro recall across present classes | 8/9 = 0.888888... |
| Multiclass Brier, sum across classes | 2.285/6 = 0.380833... |
| Negative log likelihood | approximately 0.656737 |
| Five-bin top-label ECE | 0.225 |
| Policy coverage at 0.8 | 3/6 = 0.5 |
| Policy selective accuracy | 2/3 = 0.666667... |

These agree with the tutorial's described executed outcome and the code formulas. ECE uses probability intervals with exact boundaries assigned to the bin on their right, except 1.0 in the final bin. Zero-coverage accuracy correctly returns None. The metrics test's Brier 0.76, ECE 0.3 and NLL expression are correct. No additional execution was necessary for this bounded review.

The policy returns proposals, never executes a refund or other external action. It rejects invalid finite distributions, missing evidence, non-route action classes, ties and `other`. The explicit argument `evidence_present` is a teaching stub, not a verifier; the tutorial adequately explains that real evidence and execution authorization must be checked separately. The live example prints an interpretation only and sends a synthetic ticket. It has no exception/retry service wrapper, which is expressly disclosed as required deployment work.

## Gate warning classification

All 81 reported warnings are advisory: 73 W2 unbound-assertion heuristics and eight W3 numeric-token warnings. They should not be described as 81 unresolved factual errors.

- **Original pedagogy, definitions and demonstrable arithmetic:** hypothetical ticket text; invented rubric and probabilities; p_max definition; illustrative calibration groups; temperature-transform algebra; Brier/ECE equations; cost expressions; synthetic metrics; original diagram captions. These do not require vendor attribution. Their mathematical statements and examples are sound within their written assumptions.
- **Original engineering proposals:** split design, diagnostic slices, policy checks, non-executing fallbacks, receipts, incentive probes, permissions, monitoring, and the build sequence. They are recommendations and are identified as tutorial/application design. They do not need fabricated claim-ledger citations.
- **Already supported, heuristic missed adjacency or inline links:** Choice diagram caption; Decision 1.0/GLiNER names and table entries elaborated in immediately following sourced paragraphs; LangChain further-reading link; AnyJev L1 token. No vendor evidence gap is created by these warnings.
- **Process claims requiring local evidence, not web citations:** six tests passed, syntax checked, PDFs/links captured. Preserve run evidence if publishing a verification bundle. This reviewer inspected the test definitions and snapshots but does not independently attest to a prior test run; the parent task's execution record supplies that evidence. Make the live-dependency limitation explicit as correction 3.
- **Small citation improvement:** the exact SDK package version should link to s-015 as correction 5. The temperature scaling formula is elementary algebra and its ranking invariance follows for T > 0; the current Guo citation supports the method's relevance, not a claim that this tutorial reproduced Guo's experiments.
- **All eight W3 warnings are benign:** 0.03/0.97 are explicitly illustrative Noul values, 0.10/0.30/0.60 are illustrative rubric probabilities, 0.9/90 are a caution against conflating signals, and the digit in L1 is a level name rather than an unbound measured figure.

## Evidence boundaries retained

The tutorial distinguishes schema validity from correctness; confidence from probability calibration; TypeSafe's RLCD description from a reproduced training recipe; Laya's specialized versus base checkpoints; JevK5 from TypeSafe Jev; extraction offsets from classification evidence; and vendor/practitioner findings from independently reproduced results. NIST is context rather than certification. The Banking77 fallback result stays attributed and does not imply that all cascades fail. The unsupported-incentive allegation in supplied notes remains a hypothetical threat model. These are all appropriate boundaries.

## Resolution

The root editor applied all four suggested clarifications: explicit SDK-install limitation; threshold/calibration-only tuning scope; shared validation for both cascade branches; and separate probability-only versus policy coverage in the synthetic example. The installation paragraph now links the captured SDK changelog.
