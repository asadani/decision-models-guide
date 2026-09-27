# Tutorial plan: from predictions to accountable actions

Audience assumption: Python developers who have used an LLM API but have not studied calibration. Format: an editable Markdown tutorial, code files, and original Mermaid diagrams. Research captured 26 September 2026.

## Learning spine

Use a single support ticket throughout: a customer reports a duplicate charge and asks for help. First select a team, then distinguish a refund request from refund eligibility, measure uncertainty, decide whether to route automatically, and record what happened. Only then generalize to coding-agent tool and context routing.

This avoids starting with a vendor leaderboard or assuming that a probability authorizes an action. The recurring question is: what should software do with this output?

| Part | Reader question | Teaching artifact | Sources / evidence |
|---|---|---|---|
| 1. The missing decision step | Why use a decision model when an LLM returns JSON? | Original model/code boundary diagram; rules baseline | TypeSafe Choice docs; supplied introductory articles for topic discovery |
| 2. The output contract | What are state, questions, alternatives and rubrics? | One ticket expressed as Choice, Noul and Score | Current TypeSafe primitives and SDK responses |
| 3. Probabilities and training | What do RLHF, RLVR and RLCD optimize? What is calibrated? | Synthetic calibration arithmetic; signal glossary | TypeSafe primer, InstructGPT, DeepSeek-R1, Guo et al. |
| 4. First integration | How do I call Jev without inventing an API? | Optional live Python example; pinned model identifier | Quick start, SDK changelog, model and response docs |
| 5. Model families | What differs beneath similar APIs? | Jev, Laya, Decision 1.0, GLiNER2.5-Decide, AnyJev and SemIf comparison | Maintainer repositories/model cards; vendor release caveats |
| 6. Evaluation | Does it work on my data? | Runnable offline metrics; evaluation protocol | Archestra; supplied Banking77 experiment; calibration paper |
| 7. Cascades | Will escalation improve results? | Original conditional-cascade diagram and cost equation | Banking77 negative fallback result; local illustrative arithmetic |
| 8. Execution policy | When may a judgment cause an action? | Fail-closed policy function; tests | Original application design; documented Jev failure modes |
| 9. Accountability | Who benefits, who can appeal, what can be replayed? | Proposed decision receipt and control architecture | jev.txt as design input; NIST framework as context |
| 10. Agent systems | How do tools, context and cache costs fit? | New agent architecture; symbolic routing-cost model | Independent coding-agent PDF, explicitly labeled proposal; LangChain integration article |
| 11. Next experiments | What should we build and validate next? | Staged implementation milestones and exercises | Gaps identified throughout the research |

## Deduplication decisions

- Merge the repeated “generation versus decisions” introductions into one short explanation. Keep definitions from current primary docs.
- Consolidate all calibration passages into a single sequence: distribution → top probability → provider confidence → empirical calibration → policy threshold.
- Retain the support-ticket running example as original tutorial material. Do not borrow distinctive examples, layouts or graphics from the PDFs.
- Use `jev-3.pdf` for its reported experiment and limits, rather than repeating its whole conceptual introduction.
- Use `lasa.pdf` for its failure-and-correction story, with Laya's current repository governing product claims.
- Move coding-agent ideas to the advanced chapter. They require the earlier model/policy/evaluation distinction.
- Treat `jev.txt` as a proposal backlog: receipts, provenance, incentive disclosure, counterfactual checks, shadow review and outcome monitoring. No allegations about specific companies follow from those hypotheticals.

## Corrections that must survive editing

1. RLVR and RLCD are distinct. Do not promise perfect calibration from a training objective.
2. Schema validity does not mean the selected answer is correct, safe or authorized.
3. `confidence` is not universally a calibrated probability of correctness; Noul has no separate TypeSafe confidence field.
4. Score is an ordered rubric, not reliable exact numeric extraction.
5. A JevK5 comparison is not a comparison against TypeSafe Jev.
6. AnyJev is a toolkit, not simply another pretrained Jev checkpoint. SemIf's current repository includes calibration support.
7. Native vLLM-SR integration is a roadmap item in the captured Decision 1.0 release.
8. A fallback can worsen quality. Evaluate the forwarded subset and entire cascade.
9. Deterministic schema, repeatability, calibrated uncertainty and semantic correctness are separate properties.
10. A hash is not an immutable receipt; a second model is not an independent authority by default.

## Diagram and image plan

Create five original diagrams: decision contract, train/calibrate/test separation, cascade evaluation, execution-control boundary, and agent context/routing architecture. They must have their own composition and wording. Caption each as original tutorial artwork and link the source of any underlying technical contract.

Default to these original diagrams; do not reproduce third-party PDF figures. If a company figure becomes necessary, record the exact asset URL, rights holder, original article URL, license/permission status, capture date, alt text and caption. Credit the company and link the original article directly next to the figure. An official domain alone does not establish reuse rights. See [asset policy](assets.md).

## Completion criteria

- Every supplied file has a reading record; every required URL has a capture or explicit retrieval failure.
- Empirical/vendor assertions have nearby sources and dated scope.
- Main claims pass a source-locator gate and independent semantic review.
- Offline code runs without credentials; tests cover unsafe auto-action, missing evidence, malformed probabilities and arithmetic.
- Live integration is labeled unexecuted until a real API test is performed.
- Readers can follow the path without knowing any of the original articles.
