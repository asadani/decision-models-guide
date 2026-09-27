# Appendix A. What Was and Was Not Validated

This appendix lists what was checked in preparing the book, how, and what was not. Read it before you rely on any number in the text.

## Checked

**The offline lab.** The lab in `examples/decision_workflow.py` runs offline, and its six unit tests pass. The metrics quoted in Chapter 10 were produced by running it: accuracy 0.833, majority baseline 0.500, Brier 0.381, negative log likelihood 0.657, expected calibration error 0.225, coverage 0.500 and selective accuracy 0.667 on the six synthetic cases.

**Figures against page images.** Four of the supplied PDFs were image-only, so their text came from OCR, which garbles tables and numbers. Where a figure in the book comes from one of those PDFs and matters to an argument, I compared it with a rendered image of the page:

- Hoang's cascade table, with its thresholds, shares and accuracies (Chapter 7), and the confidence-group table with group sizes, gaps and weighted contributions (Chapter 6).
- Hoang's statements of the 57 percent forwarded-set accuracy and of 84 mistakes fixed and 211 introduced (Chapters 6 and 7).
- The launch-week guide's cost figure: $0.0004 and $0.0304 per case, $30,400 and $6,480 in total (Chapter 7).
- The drone layer table in the same guide, whose rates OCR had scrambled (Chapter 12).

**Internal consistency, by my arithmetic.** These checks are mine, and each is marked as derived where it appears:

- The six confidence-group sizes sum to 3,080, and the weighted gaps sum to the reported 0.097.
- 53 invalid labels is 1.72 percent of 3,080.
- The guide's $6,480 cascade cost reproduces from its own per-case figures.
- The coding-agent document's routing totals reproduce (4.15 and 6.19), and so do the components in its chart.
- Hoang's overall accuracy, kept-set accuracy and 84/211 counts agree with one another to within one answer.
- The ten-ticket tray in Chapter 2 is invented for teaching. Its arithmetic (7 of 10 right, 50 percent coverage at a 0.90 threshold, 80 percent accuracy on the covered tickets) is recomputed by the build.

**Documentation.** The TypeSafe documentation pages, the Laya, AnyJev and SemIf READMEs, the Decision 1.0 and GLiNER release posts, the model card, the Archestra and LangChain articles, and the NIST excerpt were captured on September 26, 2026. Statements in the book about what they say were checked against those captures. Repository pages on a main branch and documentation for a current model change over time.

**Links.** Every URL in the book is checked by the build (`make verify`), which fails on a 4xx or 5xx response.

## Not checked

- **No live Jev call was made.** No API key was used and the Python SDK was not installed. The example in Chapter 5 was syntax-checked and compared against the documented API. It has not been run against the service.
- **No benchmark was reproduced.** Every measurement in the book is reported by the person who ran it. That includes Banking77, the Archestra results, the vendor benchmarks, and the figures other evaluators are quoted as having found.
- **No local model was run,** and no model weights were downloaded.
- **Other pages of the supplied PDFs** were read through OCR text. Figures that do not appear in the book were not checked against images.
- **Vendor claims about latency, price and speed** are reported as documented at capture time. I did not measure them. That includes the LangChain speed figures and TypeSafe's price comparison in Chapter 9.
- **The "my reading" section of Chapter 9** is my inference from the reported facts, and it is labeled that way. No source says it.
- **The proposals in Chapters 11 and 12** are proposals. I found no source showing them working, and I did not build them.
- **Sources with no web address** (two Medium articles, a LinkedIn post, and one independently compiled PDF) could not be re-fetched.

## Where a source says more than it should

Several statements in the supplied material were not repeated in the book, or were corrected. They are listed so that you can recognize them elsewhere.

- **"No validation, parsing or retry is needed."** A schema guarantees the shape of the answer. It says nothing about whether the answer is right, and transient failures still need handling (Chapters 1 and 5).
- **"Jev's 0 percent malformed rate."** By TypeSafe's own account this is guaranteed by schema matching and is not an empirical measurement (Chapter 1).
- **Temperature scaling is impossible on a hosted API.** Too strong: with unrounded positive probabilities it can be expressed directly, though rounding to two decimals limits it (Chapter 4).
- **A ten-level, 0 to 9 Score.** The documented contract is two to ten ordered levels (Chapter 3).
- **A 79 percent saving from the cascade.** An arithmetic sketch that leaves out the cost of one branch of its own diagram, presented with a traffic split its author calls illustrative (Chapter 7).
- **Benchmark percentages as accuracy.** TypeSafe's workflow benchmark scores agreement with a reference built from other models' answers. It has no independent ground truth, and the launch-week guide notes that no independent reproduction exists yet. Decision 1.0's 54-task suite and GLiNER's 17-dataset benchmark are also their publishers' own selections. None of these can be merged with another (Chapter 8).
- **"GLiNER beat Jev."** The release compares against JevK5, which it describes as an open reproduction and not TypeSafe's Jev (Chapter 8).
- **"Zero latency, zero hallucinations."** The author of the LinkedIn overview wrote this in a reply to a comment. The vendor's own latency claim is 70 to 500 milliseconds, and valid but wrong answers still happen (Chapters 1, 5 and 6).

## Limits of the record

This book describes a field that was less than two weeks old when its sources were written. Model versions, prices, limits and repository contents will change. The measurements are small, mostly single-run, and mostly on one task each. What lasts is the shape of the questions: is the answer valid, is it right, is the number calibrated on your population, and who is entitled to act on it.
