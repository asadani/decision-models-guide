# Supplied PDF reading notes

Read all five `.research/extracted/*.txt` files on 2026-09-26. Page references below use the PDF page markers, not article section numbers. These are notes on supplied material, not independently verified research results. OCR contains broken code, displaced table cells, obscured text, and encoding artifacts; do not transplant its code or infer missing numbers. Figures were inventoried from captions/text, not visually inspected here. No source prose or artwork is reproduced.

## Corpus map

| File | Title | Credited author / date | Pages | Role |
|---|---|---|---:|---|
| guide-to-jev.txt | The Ultimate Guide to Jev: The new Frontier AI for faster decisions | unicodeveloper; Medium; 17 September 2026 | 23 | Broad introduction, application catalog, cascade economics, launch benchmark caveats |
| jev-2.txt | JEV vs LLMs: The Non-Generative Paradigm for AI Decisions making | Gershon Celniker; LinkedIn newsletter AI in production playbook; 24 September 2026 | 5 | Short conceptual overview; comments contain research leads |
| jev-3.txt | Jev vs. LLMs: When AI Moves from Generation to Decision-Making | Nhu Hoang; Towards Data Science; 25 September 2026 | 28 | Independent practitioner experiment, calibration, negative cascade result |
| Jev-Engineering-for-Coding-Agents.txt | Jev Engineering for Coding Agents: The TypeSafe Founder's Blueprint for Building with Jev | Unnamed independent compiler; based on attributed Diogo Almeida design notes; September 2026 | 12 | Architectural proposals, context/caching economics, prospective agent harness |
| lasa.txt | Laya: a free, local alternative to Jev — and it can even play Doom(ish) | Christian Graham; Medium; 19 September 2026 | 4 | Small embodied-control experiment with explicit corrective rules and failure |

The filename `lasa` refers to Laya. The engineering PDF does not identify its compiler; do not assign its authorship to Diogo Almeida or present it as an official TypeSafe whitepaper. Page 12 explicitly describes independent synthesis. The blank or near-blank final pages of the guide and the article recommendations at the end of jev-3 contribute no technical evidence.

## Topic grouping across the corpus

- Interface and mental model: guide pp. 1–7; jev-2 pp. 1–3; jev-3 pp. 2–10. Deduplicate into one introductory chapter, distinguishing output constraints from semantic correctness and architecture disclosure.
- Probabilities and calibration: guide pp. 8–9; jev-2 p. 2; jev-3 pp. 10–15, 20–22. Use jev-3 to motivate measuring confidence signals independently. Resolve exact SDK confidence semantics from current first-party documentation.
- Workflow design and model/code boundaries: guide pp. 9–18; jev-3 pp. 15–18, 22–23; Laya pp. 2–4. Separate classifier recommendation, deterministic validation and executable authorization.
- Evaluation and cascade failure: guide p. 19; jev-3 pp. 18–23. This deserves an evaluation chapter before recommendations about automatic escalation.
- Agent harness proposals and future work: engineering pp. 2–11. Present as prospective experiments, not demonstrated shipped capability.
- Further source leads: guide launch projects pp. 12–18; jev-2 comments pp. 3–5; jev-3 references pp. 24–25. These are pointers requiring independent source retrieval, not evidence inherited from the mention.

## Guide to Jev

### Structure and distinctive contributions

- pp. 1–5: launch context, typed decisions vs generative responses, System One metaphor, vendor speed/cost framing.
- pp. 5–7: Choice, Score and Noul, support-ticket example and continuous weighted rubric interpretation.
- pp. 7–9: retrieval plus classification example for research papers; action-specific confidence gates. The important design contribution is that consequences should affect application policy.
- pp. 9–12: suitable vs unsuitable tasks and a worked cascade cost illustration. It explicitly labels the 62/18/20 traffic split as illustrative.
- pp. 12–18: launch-week examples: research-paper topic assignment, browser flight search, OCR-based computer control, trading, drone guidance, Mario, StarCraft and live judgments. It explicitly says these are self-reported launch artifacts rather than production case studies.
- pp. 18–20: literal interpretation, irrelevant-state sensitivity, prompt injection, vendor workflow scores and reference-model agreement caveat. It explains that schema validity does not establish correctness.
- pp. 19–21: FAQs and key idea that decomposition helped multiple tested models, not only Jev. pp. 21–22: reader comments emphasize calibration under shift.

### Claims needing correction or qualification

- pp. 4–6: graphics saying no validation/retry is needed overreach. Semantic checks, response transport/schema checks, application invariants and retries for transient failures still matter.
- pp. 6–9: the article slides between probability and a separate confidence field. Do not equate a confidence value of 0.9 with 90% empirical correctness without defining the signal and measuring it.
- pp. 6, 11: adding questions is not literally free in latency, tokens or resource use. Cascade latency depends on state, queueing, network and fallback share. The diagram's 180,000 specialist-model cases are not costed separately in its simplified total.
- p. 11: $6,480 vs $30,400 is illustrative arithmetic, not a deployment result. Do not present the claimed savings or 800,000 subsecond completions as measured.
- p. 15: the computer-use paragraph has a suspicious attribution reversal about Jev comparing dates versus the classifier requiring parsing. Inspect original linked repository before use.
- p. 19: benchmark percentages measure agreement with reference-model consensus, not independently labeled truth. Launch figures and quoted prices are dated. Avoid universal comparisons with all frontier LLMs or unconstrained JSON prompting.
- pp. 16, 18: drone/game examples support division of labor conceptually; their control rates, success claims and operating boundaries remain author-reported until primary repos are checked. Trading demo is not evidence of profitable or safe trading.

### Visual inventory and attribution

- p. 2: Jev fact-sheet infographic.
- p. 3: generation/parsing burden illustration.
- p. 4: side-by-side output-path diagram with latency/cost annotations.
- p. 5: Jev/LLM comparison matrix.
- p. 6: anatomy of request/response and three primitives.
- p. 8: action-risk/confidence matrix with policy pseudocode.
- p. 10: good-fit/bad-fit diagram.
- p. 11: cascade and illustrative economics.
- pp. 13–18: embedded social posts, video stills and application comparison visuals; they may involve multiple rights holders.
- p. 19: benchmark comparison chart with explicit agreement caveat.

Do not copy/redraw distinctive layouts. Create original tutorial diagrams from the concepts and cite underlying primary documentation. If any guide image is reused, identify the author/rights holder and permission, not merely TypeSafe. Article context does not make these official company artwork.

## LinkedIn overview (jev-2)

### Structure and contribution

- p. 1: metaphor, launch motivation, System One/Two framing, compact comparison matrix.
- p. 2: summary, RLCD description, three primitives, output-path graphic.
- p. 3: primitive graphic, lesson summary, links to launch article/demo.
- pp. 4–5: comments with leads for text-to-SQL schema selection and MCP tool-selection experiments. A comment reports that extra discovery calls can increase cost/latency, a useful hypothesis for the evaluation chapter.

This is mostly duplicative introductory material. Use its comments to identify missing evidence, not as substantiation of product quality.

### Claims needing correction or qualification

- p. 2: Score described as a ten-level 0–9 scale obscures the configurable 2–10 ordered levels. Refer to the actual primitive contract.
- pp. 1–2: speed and cost multipliers use launch-specific comparisons, not universal ceilings/guarantees. System One is a functional metaphor, not proof of a particular neural architecture.
- p. 4: the author's zero-latency/zero-hallucination comment is false as a general statement; typed valid errors still happen.
- p. 4: `jevtypesafeai.com` is called the official playground in a comment, but this extraction does not verify ownership. Prefer known official TypeSafe URLs.
- p. 4: table selection finding is one commenter’s report, with unclear test population. p. 5: toolgate experiment should be examined at source before quoting sample count or results; OCR garbles URL and model details.

### Visuals

p. 1: header plus comparative performance matrix; p. 2: sequential generation vs Jev flow; p. 3: primitives panel. Attribution cannot be established solely from the extraction. Use new independent diagrams and cite official contracts.

## Practitioner experiment (jev-3)

### Structure and unique contribution

- pp. 2–10: approachable interface explanation, bounds vs correctness, prior classifier history, explicit uncertainty about Jev internals, actual example response and weighted score calculation.
- pp. 11–15: calibration, temperature scaling, isotonic regression, proper scoring rules, training claims and multiple confidence signals.
- pp. 15–18: cascade proposal, missing information, hostile state, outside-category inputs and limitations.
- pp. 18–23: own Banking77 experiment, uncertainty estimates, calibration bins and negative fallback result.
- pp. 24–25: dataset, calibration-paper references, SDK/runtime versions and claimed experiment artifacts. pp. 26–28: unrelated site recommendations/footer.

### Experimental methodology (reported, not independently reproduced)

| Aspect | Reported setup | Locator |
|---|---|---|
| Dataset | Banking77 test split, 3,080 English bank-support messages, 77 intents, 40 per intent | pp. 18, 24 |
| Data source | CSV files from fixed GitHub commit; training set has 10,003 messages; actual commit not visible in OCR text | p. 24 |
| Jev | `jev-1.13.0`, one Choice question with all 77 options | pp. 9, 19–21 |
| Comparator | Qwen3-Coder-Next-80B-A3B, vLLM, 4-bit weights, temperature 0, thinking disabled | p. 18 |
| Prompt parity | Same categories and short descriptions; Jev Choice vs Qwen asked to produce one category name | pp. 18–19 |
| Pilot / runs | 100-item pilot to settle prompts, then one full-set pass per model; alternating blocks of 250 | p. 19 |
| Label coverage | No other category, because all dataset messages have an in-set gold label | p. 19 |
| Runtime geography | Spark in Japan; Qwen local single GPU with prefix caching, Jev remote request | pp. 20, 23 |
| Accuracy uncertainty | Paired bootstrap for difference; individual 95% intervals also shown | pp. 19–20 |
| Calibration | Confidence field and max-option probability separately; Wilson 95% intervals; six bins, exact 1.00 separate | pp. 14, 21 |
| Artifacts claimed | Category descriptions, request templates/hashes, per-message outputs, commands in `experiments/` and `docs/run-log.md`; full repository URL absent from extracted reference | p. 25 |

It is not clear from supplied text whether pilot examples overlapped the final test set, exactly how descriptions were chosen, which hardware/quantization artifact was used, or whether threshold tuning had a separate validation split. Do not invent these details. Author recommends separate threshold validation on p. 23; recommendation is not proof the present experiment did so.

### Results and fallback outcomes (reported only)

- pp. 19–20: Jev accuracy 81.1% (95% interval 79.6–82.4), Qwen 76.4% (74.8–77.8); difference +4.7 percentage points, paired bootstrap interval +3.7 to +5.7.
- p. 20: p50 per call 245 ms Jev vs 249 ms Qwen; input tokens 2,288 vs 1,350. Author explicitly rejects a clean speed comparison because hosting, network and prefix caching differ.
- p. 20: Qwen returned 53 invalid labels (1.72%). Its output was not constrained. Author observes that even counting all 53 as correct would leave roughly a three-point Jev lead. This is a hypothetical bound, not actual corrected accuracy.
- pp. 14, 21: confidence-field ECE 0.097 for this binning. Bins: [0, 0.5), [0.5, 0.7), [0.7, 0.9), [0.9, 0.99), [0.99, 1.00), and exactly 1.00. Confidence-field bin counts 117, 277, 390, 503, 277, 1,516; max-probability counts 101, 269, 387, 474, 223, 1,626. OCR chart cells on p. 14 are displaced; p. 21 gives consistent counts.
- p. 21: below 0.5 confidence, accuracy about 39% vs average confidence 0.41. At 0.7–0.9, average confidence 0.81 vs accuracy 53%; at 0.9–0.99, 0.95 vs 79%. At exactly 1.00, 44 of 1,516 were wrong, yielding 97.1% accuracy.
- pp. 20–22: at exact-1.00 acceptance, Jev handles 49.2% and Qwen handles the rest; cascade accuracy 76.9%, below Jev alone 81.1%. Qwen's forwarded-set accuracy is approximately 57%. Routing fixed 84 Jev errors but introduced 211 new errors: net 127 additional errors, approximately a 4.12-point drop over 3,080 items, consistent with rounded totals.
- pp. 20–21: visible cascade rows report Jev-handled shares 96.2%, 87.2%, 74.5%, 58.2%, 49.2% and cascade accuracies 80.7%, 80.5%, 79.7%, 77.6%, 76.9%. Several threshold labels are missing/misaligned in OCR, so do not publish the full threshold-to-row mapping without visual verification. Random-routing comparators are reported but their sampling construction is not specified here.
- p. 22: every tested cascade worsened overall accuracy relative to Jev alone. This establishes failure for that fallback/configuration, not that cascades cannot work. A confidence signal can rank task difficulty without ranking the relative advantage of another model.

### Corrections and limitations

- p. 5 timeline dates the decision model Laya to September 2025. This conflicts with the current first-party decision-model project chronology; do not reproduce it or confuse it with unrelated LAYA papers.
- pp. 12–13 say temperature scaling requires inaccessible logits. That is too strong: with full positive class probabilities, softmax temperature scaling can be expressed by taking log probabilities and renormalizing powers. Rounded/zero probabilities and unavailable pre-softmax information complicate exact recovery. An API can still support probability-based recalibration; do not assert impossibility.
- pp. 11–15 use confidence generically while also distinguishing the specific confidence field. Preserve that distinction. ECE depends on signal, binning and task, and the article's numbers are not global calibration guarantees.
- pp. 3, 14, 17: PriorBench, Supa Journal, scienthoon and themsquared findings are secondhand within this article. Do not treat their reported figures as independently captured evidence.
- p. 6: forced choices without an outside-category option demonstrate taxonomy mismatch, not necessarily calibrated certainty over the broader real-world question.
- p. 16: example LLM fallback returns stripped text without strict enum validation. Rewrite application code with validation and a safe review/error path.
- pp. 20, 23: one English in-distribution dataset, one prompt/configuration, one local quantized LLM and one remote Jev version. No out-of-category, cross-language, longitudinal drift or production reliability evidence. Artifacts are referenced but not checked here, and no runs have been repeated.

### Figure inventory

| Figure | Page(s) | Subject / attribution |
|---|---|---|
| Header photo | 2 | Credited to Ian Deng on Unsplash; photo rights require original source/license check |
| 1 | 4 | LLM JSON vs typed option probabilities; author image, LLM side illustrative |
| 2 | 5 | Historical timeline; author image; Laya date error |
| 3 | 6 | Typed input/output contract; author image |
| 4 | 8–9 | Token generation vs option scoring; illustrative, not speed measurement |
| 5 | 10 | Choice/Score/Noul and weighted mean; author image |
| 6 | 11 | Calibration as grouped outcomes; illustrative |
| 7 | 12 | Temperature scaling; illustrative |
| 8 | 12–13 | Isotonic calibration curve; illustrative points with real fit |
| 9 | 13 | Log scoring rule and expected-loss example; illustrative |
| 10 | 13–14 | RLHF/RLVR/RLCD comparison; vendor-described training, not disclosed implementation |
| 11 | 14 | Measured ECE-bin decomposition; article's own run |
| 12 | 15 | Confidence reliability sketch/plot; article's own run |
| 13 | 16–17 | Cascade flow; illustrative traffic |
| 14 | 18 | Appropriate task boundaries; author image |
| 15 | 19–20 | Banking77 accuracy and intervals; article's own run |
| 16 | 21 | Two confidence signals, Wilson intervals and counts; article's own run |
| 17 | 23 | Code/model/cascade decision tree; author image |

All numbered figures are credited as author-created in the article. New tutorial visuals should independently explain concepts and label any newly generated data as synthetic. Do not recreate the author's measured plots without verified raw results and clear attribution.

## Coding-agent engineering synthesis

### Structure and contributions

- pp. 1–3: explicit state plus per-turn judgments, hypothetical no-KV-cache redesign, six agent-design symptoms.
- pp. 3–4: routing arithmetic includes context loading and handback reprocessing rather than comparing token prices alone.
- pp. 4–6: compaction, sub-agent state handoff, restarts, always-loaded capabilities, token-share estimates, programmable permissions and tool routing.
- pp. 6–8: per-query visibility levels for stored chunks, cache-reuse choice, subgoal deduplication, concurrent shared state, snippets/schema/docs disclosure.
- pp. 9–10: conditional instruction fragments and hooks, explicit variables, trust/data-sensitivity routing, background tasks sharing retrieval.
- pp. 11–12: candidate tool integrations and provenance disclaimer.

### Arithmetic and evidence boundary

p. 4 compares pure-frontier cost `25Y + 5Z` with routed cost `3X + 20Y + 8Z`, using assumed input/output prices and X=0.65, Y=0.12, Z=0.23. Totals are 4.15 vs 6.19. The calculation is internally consistent under its stated model; the routed-minus-direct difference is `3X - 5Y + 3Z`. Routing is more expensive only when that expression is positive, not universally. These are illustrative normalized token units, not measured invoices. Cache retention/pricing, summary size, routing overhead, task quality, tool waiting and repeated handoffs can change the comparison.

The token-share table on p. 5 is explicitly an illustrative estimate, not observed telemetry. The separately attributed Microsoft fastcontext figures (56.2% of tool-use turns, 46.5% of main-agent tokens) on pp. 5–6 require primary-source verification. The tool project rankings/performance suggestions on p. 11 are unverified leads.

### Questionable generalizations / tutorial safeguards

- pp. 3–4: not all agents require every schema to be permanently loaded or invalidate every cache on a routing transition. Treat as a motivating design case, not universal architecture.
- p. 6: choosing a tool does not construct arbitrary arguments by itself; Jev's bounded decisions must be composed with validated state extraction or a generation tool.
- pp. 6–9: deciding context visibility must not silently discard binding policy, unresolved user constraints or facts needed to recognize uncertainty. Query compression's superiority is a hypothesis requiring retrieval/decision-quality evaluation.
- pp. 7, 10: read-only tasks can still contend for compute, bandwidth and service quotas, and can leak data; they merely avoid some write conflicts. Locks do not alone establish concurrency correctness.
- pp. 9–10: low cost or open weights does not establish a provider's privacy practices. Data policies need verified provider terms and hard enforcement; a model's prediction of file sensitivity cannot authorize disclosure.
- pp. 1, 6: permission judgments should be advisory within deterministic authorization boundaries. A learned allow score is not proof a command is safe.
- p. 12: attribution to private founder notes is not independently verified here; none of the proposed integrations should be described as existing Jev features or proven gains.

### Visual inventory

Figure 1 p. 1 explicit-state harness; Figure 2 p. 4 routing cost bars; Figure 3 p. 6 estimated token allocation; Figure 4 p. 7 visibility ladder; Figure 5 p. 8 tiered tool disclosure; Figure 6 p. 9 conditional instructions; Figure 7 p. 10 shared retrieval/background tasks. Tables: decision points p. 3, six symptoms p. 3, token estimates p. 5, sensitivity routing p. 10, integration shortlist p. 11. Page 12 says all diagrams are original to this independent synthesis; that is an authorship assertion, not a reuse license. Build original diagrams and attribute the conceptual inspiration accurately.

## Laya/Doom practitioner note

### Structure, contribution and failure

- pp. 1–2: local model motivation, 421M model description, rough self-reported comparison claim and links to Convai model artifacts.
- pp. 2–3: structured game telemetry rather than pixels is fed to the decision model, followed by a deterministic safety layer.
- p. 3: initial multiclass action selection never chose shoot; reframing as a focused binary shooting question improved behavior. Ammo/alignment checks remained necessary.
- p. 4: explicit overrides for corner spinning, oscillation and failure to face enemies, with logs; turning amount measured rather than guessed; exploration, door/wall probing and wall following added.
- p. 4: game exit remained unsolved. Author says Claude produced most code. This is a candid harness case study, not evidence of autonomous game mastery.

The article's approx-10x speed and accuracy comparison is a cited table pitch without controlled methodology here. Calibration/trustworthiness language on p. 2 is not supported by a reliability study in this article. No run count, seeds, version pins, success-rate distribution or replay logs are provided in the extracted text. Avoid presenting a demo as benchmark evidence. Its strongest pedagogical use is to show how state representation, question decomposition and deterministic rules materially affect behavior.

### Visuals and attribution

p. 1 game screenshot with telemetry; p. 3 telemetry-to-model-to-safety-to-action pipeline; p. 4 embedded video still credited to Christian Graham. These are practitioner graphics, not official Convai website images. Build a fresh state/decision/policy/action diagram, cite this article for the reported experience, and retain its unsuccessful exit outcome.

## Suggested use in the tutorial

Start with a new small support-ticket example, then probabilities and score semantics, then independent model families, then measurement, then action policy and validated fallback. Only after those foundations introduce coding-agent context/routing ideas as research directions. The corpus's most important tension is between the guide's attractive illustrative cascade and the practitioner's measured harmful fallback. Use that tension to teach the need for conditional fallback evaluation rather than repeat either as a universal conclusion.
