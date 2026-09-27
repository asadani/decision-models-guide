# Verification report

**Verdict: PASS**

| | |
|---|---|
| Report | `tutorial/decision-models.md` |
| Sources in ledger | 33 |
| Claims in ledger | 29 |
| Claims cited by the report | 29 |
| Hard failures | 0 |
| Warnings | 80 |

## Hard failures

None. Every cited claim resolves to a ledger row, binds an existing source,
and locates its evidence in a snapshot whose hash still matches.

## Warnings

Advisory. These do not block the report.

### W2 -- Assertion with no marker

- **decision-models.md:3** -- unbound assertion (asserts something about a named entity)
  *A practical tutorial for Python developers, centered on Jev and several alternatives.
- **decision-models.md:7** -- unbound assertion (asserts something about a named entity)
  Please refund the duplicate.”
- **decision-models.md:11** -- unbound assertion (asserts something about a named entity)
  You will build a small decision workflow, learn to interpret its outputs, compare implementation families, measure mistakes, and design a...
- **decision-models.md:27** -- unbound assertion (asserts something about a named entity)
  This is a conceptual contract, not the Jev HTTP schema.
- **decision-models.md:40** -- unbound assertion (asserts something about a named entity)
  The bounded choice contract is based on TypeSafe's [Choice documentation](https://docs.typesafe.ai/primitives/choice); the application bo...
- **decision-models.md:52** -- unbound assertion (asserts something about a named entity)
  An LLM returning a constrained JSON label is a legitimate comparison baseline.
- **decision-models.md:58** -- unbound assertion (asserts something about a named entity)
  Use the current documentation for the contract, rather than copying SDK syntax out of article screenshots.
- **decision-models.md:68** -- unbound assertion (asserts something about a named entity)
  Prefer criteria with operational meaning:
- **decision-models.md:78** -- unbound assertion (asserts something about a named entity)
  Adding `other` gives the model a permitted way to represent taxonomy mismatch.
- **decision-models.md:80** -- unbound assertion (asserts something about a named entity)
  Keep two issues separate: “the model found one option much better than the others” and “the available options adequately represent the si...
- **decision-models.md:93** -- unbound assertion (asserts something about a named entity)
  Time-sensitive issue without a stated outage.
- **decision-models.md:94** -- unbound assertion (asserts something about a named entity)
  Current service outage or inability to operate.
- **decision-models.md:98** -- unbound assertion (contains a figure)
  $$ 0(0.10) + 1(0.30) + 2(0.60) = 1.50. $$
- **decision-models.md:106** -- unbound assertion (asserts 'largest')
  For a categorical distribution, let `p_max` be the largest option probability.
- **decision-models.md:110** -- unbound assertion (contains a figure)
  **Calibration is an empirical relationship.** Consider a hypothetical held-out set where 100 predictions have top probability close to `0...
- **decision-models.md:112** -- unbound assertion (contains a figure)
  Now suppose two groups both have 80 correct predictions out of 100.
- **decision-models.md:116** -- unbound assertion (asserts something about a named entity)
  Use these as descriptions of objectives, not interchangeable labels:
- **decision-models.md:124** -- unbound assertion (asserts something about a named entity)
  The supplied notes group RLVR and RLCD together too closely.
- **decision-models.md:126** -- unbound assertion (asserts something about a named entity)
  Recalibration is another distinct step.
- **decision-models.md:128** -- unbound assertion (contains a figure)
  $$ q_i = \frac{p_i^{1/T}}{\sum_j p_j^{1/T}}, \qquad T>0. $$
- **decision-models.md:132** -- unbound assertion (asserts something about a named entity)
  Fit `T` on a separate labeled calibration set.
- **decision-models.md:138** -- unbound assertion (asserts something about a named entity)
  Create a separate Python environment, install `typesafe-sdk==0.7.1` (the captured [Python changelog](https://docs.typesafe.ai/sdk/python/...
- **decision-models.md:179** -- unbound assertion (asserts something about a named entity)
  The API shape was checked against captured documentation and the Python source was syntax-checked.
- **decision-models.md:187** -- unbound assertion (asserts something about a named entity)
  Select comparison candidates by what you need to control: the hosted service, model weights, runtime, labels, calibration procedure or ap...
- **decision-models.md:193** -- unbound assertion (table cell contains a figure)
  | Decision 1.0 | Family spanning encoder and adapted Qwen branches | Which release/runtime fits our evidence length and latency constrain...
- **decision-models.md:194** -- unbound assertion (table cell contains a figure)
  | GLiNER2.5-Decide | Schema-driven classification with related structured capabilities | Do we need multi-label decisions, extraction or ...
- **decision-models.md:200** -- unbound assertion (contains a figure)
  **Decision 1.0:** the captured release describes encoder and adapted Qwen branches.
- **decision-models.md:208** -- unbound assertion (asserts something about a named entity)
  Let each system use its supported interface, but record differences in prompts, candidates, truncation, quantization, hardware and retries.
- **decision-models.md:214** -- unbound assertion (asserts something about a named entity)
  Representative ordinary tickets, sampled from the intended traffic.
- **decision-models.md:215** -- unbound assertion (asserts something about a named entity)
  Ambiguous and missing-information cases.
- **decision-models.md:216** -- unbound assertion (asserts something about a named entity)
  Rare but costly mistakes, deliberately oversampled for diagnostic testing.
- **decision-models.md:217** -- unbound assertion (asserts something about a named entity)
  Stress cases: negation, contradictory evidence, injected instructions, unfamiliar topics, languages and option permutations.
- **decision-models.md:219** -- unbound assertion (asserts something about a named entity)
  Keep production-weighted results separate from stress-suite results.
- **decision-models.md:233** -- unbound assertion (asserts something about a named entity)
  Original tutorial evaluation protocol.
- **decision-models.md:247** -- unbound assertion (asserts something about a named entity)
  Judge agreement is also an operational reference, not infallible ground truth.
- **decision-models.md:258** -- unbound assertion (contains a figure)
  $$ \text{Brier} = \frac{1}{N}\sum_{i=1}^{N}\sum_{k=1}^{K}(p_{ik}-y_{ik})^2 $$
- **decision-models.md:264** -- unbound assertion (asserts something about a named entity)
  $$ \text{ECE} = \sum_b \frac{|B_b|}{N} \left|\operatorname{accuracy}(B_b)-\operatorname{meanTopProbability}(B_b)\right|. $$
- **decision-models.md:269** -- unbound assertion (asserts something about a named entity)
  The Brier convention sums over classes and averages over cases; some libraries use different normalization.
- **decision-models.md:273** -- unbound assertion (asserts something about a named entity)
  Freeze the threshold before final test evaluation.
- **decision-models.md:277** -- unbound assertion (asserts something about a named entity)
  Instead, compare the two models on exactly those forwarded cases.
- **decision-models.md:279** -- unbound assertion (asserts something about a named entity)
  Let `S` be the subset the gate forwards.
- **decision-models.md:281** -- unbound assertion (asserts something about a named entity)
  $$ \operatorname{Accuracy}(\text{fallback}\mid S) > \operatorname{Accuracy}(\text{primary}\mid S)? $$
- **decision-models.md:310** -- unbound assertion (asserts something about a named entity)
  Add human review, retries and infrastructure when relevant.
- **decision-models.md:318** -- unbound assertion (asserts something about a named entity)
  Validate label membership, finite probabilities and a normalized distribution.
- **decision-models.md:319** -- unbound assertion (asserts something about a named entity)
  Check that required evidence exists.
- **decision-models.md:320** -- unbound assertion (asserts something about a named entity)
  Check whether the action is in the permitted automatic-action class.
- **decision-models.md:321** -- unbound assertion (asserts something about a named entity)
  Handle ties, `other`, and uncertainty.
- **decision-models.md:322** -- unbound assertion (asserts something about a named entity)
  Produce a routing proposal or a review outcome.
- **decision-models.md:324** -- unbound assertion (asserts something about a named entity)
  Even after a policy permits an action, a real executor needs current authorization, business invariants and duplicate-action protection.
- **decision-models.md:348** -- unbound assertion (asserts something about a named entity)
  Original proposed architecture inspired by the supplied concerns.
- **decision-models.md:354** -- unbound assertion (asserts something about a named entity)
  Replaying inputs to a hosted service also does not guarantee bit-identical outputs.
- **decision-models.md:360** -- unbound assertion (asserts something about a named entity)
  Design paired tests that vary a sponsorship field while holding legitimate relevance facts fixed.
- **decision-models.md:362** -- unbound assertion (asserts something about a named entity)
  Use similarly careful tests for irrelevant wording, missing evidence and demographic proxies.
- **decision-models.md:364** -- unbound assertion (asserts something about a named entity)
  Keep deterministic constraints and an accountable review process alongside shadow judgments.
- **decision-models.md:366** -- unbound assertion (asserts something about a named entity)
  Finally, monitor consequences: reversals, appeal outcomes, delayed failures, review volume, subgroup error concentrations and changes aft...
- **decision-models.md:368** -- unbound assertion (asserts something about a named entity)
  Explicit action classes and non-negotiable policy checks are easier to inspect and test.
- **decision-models.md:372** -- unbound assertion (asserts something about a named entity)
  Treat its illustrative cost and token-share figures accordingly.
- **decision-models.md:374** -- unbound assertion (asserts something about a named entity)
  Consider an agent investigating a failing test.
- **decision-models.md:388** -- unbound assertion (asserts something about a named entity)
  Original proposed agent design.
- **decision-models.md:390** -- unbound assertion (asserts something about a named entity)
  Test whether context filtering preserves the evidence needed for the final task.
- **decision-models.md:392** -- unbound assertion (asserts something about a named entity)
  Measure routing at workflow level.
- **decision-models.md:399** -- unbound assertion (asserts something about a named entity)
  Compare that with the direct path under the same success criterion.
- **decision-models.md:401** -- unbound assertion (asserts something about a named entity)
  LangChain's supplied [Jev and LangGraph article](https://www.langchain.com/blog/building-prod-with-jev-and-langgraph) is further reading ...
- **decision-models.md:405** -- unbound assertion (asserts something about a named entity)
  **Choose one reversible decision.** Ticket routing is a better first experiment than moving money.
- **decision-models.md:406** -- unbound assertion (asserts something about a named entity)
  **Create an adjudicated evaluation set.** Keep development, calibration and final test cases separate; include costly edge cases as a nam...
- **decision-models.md:407** -- unbound assertion (asserts something about a named entity)
  **Run baselines and two candidates.** Record exact versions, question schemas, truncation, full distributions and end-to-end timing.
- **decision-models.md:408** -- unbound assertion (asserts something about a named entity)
  **Tune thresholds and probability calibration on calibration data.** Keep prompt and taxonomy development in the development split.
- **decision-models.md:409** -- unbound assertion (asserts something about a named entity)
  **Run in shadow mode.** Compare proposed actions with actual handling, without allowing the candidate to execute them.
- **decision-models.md:410** -- unbound assertion (asserts something about a named entity)
  **Enable limited routing with receipts.** Add rollback, rate limits, review capacity, policy ownership and duplicate-action protection.
- **decision-models.md:411** -- unbound assertion (asserts something about a named entity)
  **Review outcomes before widening authority.** Model quality, policy quality and available evidence each need their own explanation.
- **decision-models.md:413** -- unbound assertion (asserts something about a named entity)
  Try three exercises with the offline lab: change the threshold and inspect coverage; insert a confident wrong prediction and observe cali...
- **decision-models.md:419** -- unbound assertion (asserts something about a named entity)
  The optional Jev example was syntax-checked, not live-tested; its SDK was not installed in this workspace.
- **decision-models.md:421** -- unbound assertion (asserts something about a named entity)
  All five supplied PDFs and four required web links were captured.

### W3 -- Figure in a cited sentence is not in the claim

- **decision-models.md:84** -- the figure 0.03 does not appear in [^c-002] or its quoted evidence
  A Noul is a probability of yes, not a Python Boolean.[^c-002] For illustration, `0.03` supports a different interpretation from `0.97`; both
- **decision-models.md:84** -- the figure 0.97 does not appear in [^c-002] or its quoted evidence
  A Noul is a probability of yes, not a Python Boolean.[^c-002] For illustration, `0.03` supports a different interpretation from `0.97`; both
- **decision-models.md:96** -- the figure 0.10 does not appear in [^c-010] or its quoted evidence
  The SDK represents these as zero-based ordered levels and reports a probability-weighted expected score.[^c-010] With illustrative probabili
- **decision-models.md:96** -- the figure 0.30 does not appear in [^c-010] or its quoted evidence
  The SDK represents these as zero-based ordered levels and reports a probability-weighted expected score.[^c-010] With illustrative probabili
- **decision-models.md:96** -- the figure 0.60 does not appear in [^c-010] or its quoted evidence
  The SDK represents these as zero-based ordered levels and reports a probability-weighted expected score.[^c-010] With illustrative probabili
- **decision-models.md:108** -- the figure 0.9 does not appear in [^c-004], [^c-014] or its quoted evidence
  TypeSafe derives Choice/Score confidence from the distribution; Noul has no separate confidence field.[^c-004] Do not interpret every provid
- **decision-models.md:108** -- the figure 90 does not appear in [^c-004], [^c-014] or its quoted evidence
  TypeSafe derives Choice/Score confidence from the distribution; Noul has no separate confidence field.[^c-004] Do not interpret every provid

---

Rules are defined in `docs/LEDGER-SPEC.md` section 5.
