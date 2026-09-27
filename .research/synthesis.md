# Research synthesis and source map

Captured 26 September 2026. This is the research basis and editorial reasoning for the tutorial, not a model benchmark. The independent semantic audit passed all 29 curated claims. Source tiers describe provenance, not proof of real-world quality.

## Coverage

33 source records: 8 T1, 13 T2, 1 T3 and 11 T4. T4 includes the eight supplied files, whose content is treated as research input rather than independently verified fact. Four image-only PDFs were OCRed; the engineering PDF had native text. All 72 PDF pages were processed. All four `links.txt` URLs were captured. Archestra required browser retrieval after shell DNS failed; that failure and successful alternate capture are both retained.

| Theme | Supplied sources | Primary/source records | Tutorial use |
|---|---|---|---|
| Decision contract | guide-to-jev, jev-2, jev-3 | s-005–s-015 | State, questions, Choice/Score/Noul; SDK contract |
| Calibration and learning | jev.txt, jev-3 | s-009, s-010, s-016–s-018 | Distinct training objectives and uncertainty signals |
| Alternatives | lasa, other-model | s-002, s-003, s-021–s-024, s-033 | Compare architectures and deployment choices without a universal winner |
| Empirical limitations | jev-3; Archestra link | s-011, s-020, s-027 | Error analysis, option order, calibration and harmful fallback |
| Workflow orchestration | LangChain link; engineering PDF | s-001, s-028 | Context, graph control and symbolic cost modeling |
| Accountability | jev.txt | s-019, s-030 | Proposed policy boundary, receipts, incentives, monitoring |

## 1. What the interface establishes

Choice, Noul and Score have distinct contracts (c-001–c-004, c-010). TypeSafe's zero-percent formatting figure is a schema claim (c-006). Its own limitation documentation acknowledges numerical, adversarial and consistency problems (c-007). The editorial conclusion is to teach the output contract and action policy separately. This is a design recommendation grounded in those documented boundaries, not a claim of a new architecture.

Evidence is primarily vendor documentation: authoritative for the interface, single-source for claims about proprietary training. A model that returned arbitrary strings under a Choice request would contradict the contract; its choice being wrong would not.

## 2. Calibration and training

The corpus supports keeping RLHF, RLVR and the vendor's RLCD description distinct (c-005, c-027–c-029). Probability calibration concerns groups of predictions. TypeSafe's confidence is a derived signal, and other implementations need not share it (c-004, c-014). The tutorial therefore measures top-probability calibration and treats provider confidence as a separately validated routing score.

No proprietary RLCD training run or dataset was inspected. Exact optimization implementation and independent calibration across application distributions remain unestablished. An internal training objective cannot by itself settle those questions.

## 3. Alternatives

The captured artifacts distinguish readout/calibration tooling (AnyJev and SemIf), encoder checkpoints (Laya and GLiNER2.5-Decide), and a multi-architecture family (Decision 1.0); see c-012–c-021. These are implementation choices to evaluate, not substitutes with interchangeable probabilities. JevK5 must not be renamed Jev (c-020). Decision 1.0 native router integration remains a roadmap statement in this release (c-019).

Evidence is strongest for interface and documented limitations. Vendor benchmark numbers cannot establish a general ranking. Main-branch repositories are mutable; fresh captures already differ from older search snippets about SemIf calibration.

## 4. Testing and cascades

Archestra's source describes a small, judge-filtered evaluation and mostly stable labels with probability/order sensitivity (c-022–c-023). Nhu Hoang's supplied experiment describes a fallback that introduced more errors than it fixed (c-024). These do not establish that Jev is always unstable or that all cascades fail. They justify explicit repeat/order tests and measuring the fallback on the selected difficult subset.

The strongest case against blanket skepticism is that these reports still find useful decisions and useful uncertainty signals in their workloads. The strongest case against blanket adoption is that application harm and rare mistakes are hidden by aggregate accuracy. Both can be true because the metrics and populations differ.

## 5. Controls and incentives

The six control ideas in jev.txt are retained as proposals. The NIST Core provides governance context (c-026); it does not validate a product called a Decision Firewall. There is no captured evidence that Jev or another named vendor secretly optimizes sponsor interests. That part of the notes should become a hypothetical threat model and a testable disclosure/monitoring requirement.

The notes' multiplicative risk equation is a heuristic without a validated scale. Replace it with explicit impact classes, policy checks, calibrated error estimates where available, and hard overrides. A second model may share errors; a hash cannot make records immutable; stored inputs cannot guarantee bit-for-bit hosted-model replay.

## 6. Natural learning path

The proposed order is contract → probabilities → one integration → alternatives → evaluation → policy → accountability → advanced agent applications. This is an editorial design choice. It deliberately introduces failure measurement before advocating automation.

The independent engineering PDF is an attributed synthesis, not an official TypeSafe whitepaper (c-025). Its routing arithmetic is illustrative. The tutorial generalizes the cost equation using symbolic rates and includes reprocessing and handoff costs, avoiding stale list-price comparisons.

## Gaps and limitations

- **Checked in captured material:** TypeSafe publicly documents failure modes; alternative repos document non-interchangeable confidence semantics; required links are accessible through at least one retrieval method.
- **Not checked:** live Jev behavior, local model inference, benchmark replication, all incidental links in notes/comments, video transcripts, price-plan procurement, legal compliance and third-party image permissions.
- **Not disclosed by the captured public sources sufficiently for reproduction:** Jev's full training data, architecture and RLCD recipe. This does not assert that no other public source exists.
- **Single-source dependencies:** each vendor's own API and release claims; Archestra's particular protocol; Nhu Hoang's particular fallback experiment. Removing a practitioner report removes that case study, not the need to test cascades.
- **What would change the recommendations:** a controlled application-specific evaluation showing safe automated coverage and better forwarded-subset performance would justify widening automation; failed subgroup or adversarial tests would narrow it.

Publication should include only the tutorial, code and original diagrams. Do not publish entire captured articles or OCR extracts as part of the article.
