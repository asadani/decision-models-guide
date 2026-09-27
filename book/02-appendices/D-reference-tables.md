# Appendix D. Reference Tables {.unnumbered}

The tables behind Chapters 6 and 7, moved here so the chapters can carry the argument. Every figure is reported by the person who ran the test, and each table names its source. Nothing here is reproduced.

## Banking77: accuracy, time and tokens

| | Jev | Qwen3-Coder-Next-80B-A3B |
|---|---|---|
| Accuracy (95% interval) | 81.1% (79.6 to 82.4) | 76.4% (74.8 to 77.8) |
| Median time per call | 245 ms | 249 ms |
| Input tokens per call | 2,288 | 1,350 |

*Reported by Hoang. Jev minus Qwen on the same messages: +4.7 percentage points, 95% interval +3.7 to +5.7 (paired bootstrap).*


## Banking77: the confidence groups

| Confidence group | Answers | Gap (reported minus actual) | Share of answers × gap |
|---|---|---|---|
| Below 0.5 | 117 | 0.01 | 0.001 |
| 0.5 to 0.7 | 277 | 0.17 | 0.015 |
| 0.7 to 0.9 | 390 | 0.27 | 0.035 |
| 0.9 to 0.99 | 503 | 0.16 | 0.026 |
| 0.99 to below 1.00 | 277 | 0.07 | 0.006 |
| Exactly 1.00 | 1,516 | 0.03 | 0.014 |

*Reported by Hoang, Figure 11, checked against the page image. Weighted sum, the expected calibration error: 0.097.*

The group sizes sum to 3,080, and the last column sums to 0.097, which is the article's stated expected calibration error. Both checks are mine.

## Banking77: the cascade

| Threshold on Jev's confidence | Share handled by Jev | Cascade accuracy | Random routing at the same share |
|---|---|---|---|
| Jev only | 100% | 81.1% | |
| at least 0.5 | 96.2% | 80.7% | 80.9% |
| at least 0.7 | 87.2% | 80.5% | 80.5% |
| at least 0.9 | 74.5% | 79.7% | 79.9% |
| at least 0.99 | 58.2% | 77.6% | 79.1% |
| exactly 1.00 | 49.2% | 76.9% | 78.7% |
| Qwen only | 0% | 76.4% | |

*Reported by Hoang; column headings checked against the page images.*


## Archestra: dangerous calls

| Model | Accuracy, zero-shot | Recall on the nine dangerous calls |
|---|---|---|
| Sonnet 5 | 98% | 44% (4 of 9) |
| Jev (`jev-latest`) | 93% | 78% (7 of 9) |
| Always answer "benign" | 79% | 0% |

*Reported by Archestra. Other models tested scored between 48 and 83 percent zero-shot.*
