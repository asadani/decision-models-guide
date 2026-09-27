"""Check the numbers and quotations in the book against their sources.

Every claim below is one statement the book makes about a source, with:

  source       key into SOURCES (a captured text file)
  locator      where in the source it comes from
  verify       "text"     needles must appear in the captured source text
               "image"    OCR text is unreliable; the figure was read from a
                          rendered page image (attestation, no automatic check
                          of the source; the book side is still checked)
               "derived"  a Python expression that must evaluate true; the
                          figure is my arithmetic from reported values
  src_needles  strings that must appear in the source text (verify="text")
  book_needles strings that must appear in the manuscript
  expr         expression (verify="derived")

Run:  python scripts/check_book_claims.py
It rewrites .research/book-claims.jsonl (the ledger) and exits non-zero if any
claim fails.
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / ".research"

SOURCES = {
    "jev-3": R / "extracted/jev-3.txt",
    "guide": R / "extracted/guide-to-jev.txt",
    "eng": R / "extracted/Jev-Engineering-for-Coding-Agents.txt",
    "lasa": R / "extracted/lasa.txt",
    "jev-2": R / "extracted/jev-2.txt",
    "notes": ROOT / "archive" / "jev.txt",
    "launch": R / "snapshots/s-004.txt",
    "langchain": R / "snapshots/s-001.txt",
    "doc-quickstart": R / "snapshots/s-005.txt",
    "doc-choice": R / "snapshots/s-006.txt",
    "doc-score": R / "snapshots/s-007.txt",
    "doc-confidence": R / "snapshots/s-009.txt",
    "doc-primer": R / "snapshots/s-010.txt",
    "doc-jagged": R / "snapshots/s-011.txt",
    "doc-models": R / "snapshots/s-014.txt",
    "doc-changelog": R / "snapshots/s-015.txt",
    "r1": R / "snapshots/s-018.txt",
    "nist": R / "snapshots/s-019.txt",
    "archestra": R / "snapshots/s-020.txt",
    "gliner-post": R / "snapshots/s-033.txt",
    "decision1": R / "snapshots/s-002.txt",
    "anyjev": R / "alternatives/snapshots/s-001.txt",
    "laya": R / "alternatives/snapshots/s-002.txt",
    "gliner-card": R / "alternatives/snapshots/s-003.txt",
    "semif": R / "alternatives/snapshots/s-004.txt",
}

CLAIMS = []


def claim(cid, ch, statement, source, locator, verify, src=(), book=(), expr=None, planned=False):
    """planned=True: bound to its source now, not yet in the book (no book_needles).

    Used for claims a later chapter will make, so they are verified before they
    are written, not after."""
    CLAIMS.append(dict(id=cid, ch=ch, statement=statement, source=source,
                       locator=locator, verify=verify, src_needles=list(src),
                       book_needles=list(book), expr=expr, planned=planned))


# ---- Chapter 1 -----------------------------------------------------------
claim("c01-01", 1, "Launch post: the 0% type-error figure is not empirical; schema matching is guaranteed",
      "launch", "Hallucination and Type-safety", "text",
      src=["Our number is not empirical. Schema matching is guaranteed"],
      book=["Our number is not empirical. Schema matching is guaranteed"])
claim("c01-02", 1, "Guide FAQ: zero type errors is not zero mistakes",
      "guide", "FAQ, p.20", "text",
      src=["Zero type errors is not zero mistakes"],
      book=["Zero type errors is not zero mistakes"])

# ---- Chapter 2 -----------------------------------------------------------
claim("c02-01", 2, "Choice accepts up to 255 options", "doc-choice", "Choice", "text",
      src=["A Choice question accepts up to 255 options"], book=["up to 255 options"])
claim("c02-02", 2, "Score criteria: at least two levels, API accepts up to 10", "doc-score", "criteria", "text",
      src=["Should have at least two levels; the API accepts up to 10"],
      book=["at least two levels; the API accepts up to 10"])
claim("c02-03", 2, "Score is a probability-weighted mean of the level numbers", "doc-score", "score definition", "text",
      src=["probability-weighted mean of the level numbers"], book=["probability-weighted mean of the level numbers"])
claim("c02-04", 2, "Launch: gives up string generation; unstructured state in, typed probabilistic decisions out",
      "launch", "opening", "text",
      src=["gives up string generation", "unstructured state in, typed probabilistic decisions out"],
      book=["gives up string generation", "unstructured state in, typed probabilistic decisions out"])
claim("c02-05", 2, "Hoang's call: anger 0.63 / 0.37, score 1.37; refund 0.99", "jev-3", "section 5, p.9-10", "text",
      src=["0.63 to", "0.37", "1.37", "0.99"], book=["0.63", "0.37", "1.37", "0.99"])
claim("c02-06", 2, "Score weighted mean recomputed: 0*0.10+1*0.30+2*0.60 = 1.50; 0*0+1*0.63+2*0.37 = 1.37",
      "derived", "arithmetic", "derived",
      book=["which is 1.50", "1.37"],
      expr="math.isclose(0*0.10+1*0.30+2*0.60, 1.5) and math.isclose(0*0+1*0.63+2*0.37, 1.37)")
claim("c02-07", 2, "Jaggedness: nine failure modes; Noul/not-Noul sum 0.72+0.47=1.19; hostile-state sentence",
      "doc-jagged", "failure modes table; invariants; adversarial", "text",
      src=["| 9 | [Generation]", "1.19", "does not treat it as hostile by default"],
      book=["nine failure modes", "1.19", "does not treat it as hostile by default"])
claim("c02-08", 2, "0.72 + 0.47 = 1.19", "derived", "arithmetic", "derived",
      expr="math.isclose(0.72+0.47, 1.19)")
claim("c02-09", 2, "Hoang: TypeSafe has not published model size, training data, or full architecture",
      "jev-3", "p.8", "text",
      src=["has not published its model size, training data, or full architecture"],
      book=["has not published its model size, training data, or full architecture"])

# ---- Chapter 3 -----------------------------------------------------------
claim("c03-01", 3, "Confidence doc: statistic computed from the probability distribution; Noul carries none; never locked in",
      "doc-confidence", "Confidence is derived", "text",
      src=["is a statistic computed from the probability distribution the answer already gives you",
           "(Noul answers don't carry one.)", "you are never locked into our definition"],
      book=["a statistic computed from the probability distribution the answer already gives you",
            "never locked into our definition"])
claim("c03-02", 3, "Hoang: anger confidence 0.44 with top probability 0.63", "jev-3", "p.10", "text",
      src=["confidence of 0.44", "0.63"], book=["confidence of 0.44"])
claim("c03-03", 3, "Laya README: Jev confidence (n*p_max-1)/(n-1); Laya uses 1 - normalized entropy; does not transfer",
      "laya", "differences from Jev", "text",
      src=["1 minus normalised entropy", "A threshold carried over from Jev does not transfer"],
      book=["A threshold carried over from Jev does not transfer"])
claim("c03-04", 3, "(3*0.63-1)/2 is about 0.445", "derived", "arithmetic", "derived",
      book=["about 0.445"], expr="abs((3*0.63-1)/2 - 0.445) < 0.001")
claim("c03-05", 3, "Primer: rates describe groups of predictions, not a guarantee about any single answer",
      "doc-primer", "RLCD and calibrated decisions", "text",
      src=["These rates describe groups of predictions, not a guarantee about any single answer"],
      book=["describe groups of predictions, not a guarantee about any single answer"])
claim("c03-06", 3, "Primer: RLHF can reward sycophancy and confident-sounding hallucinations; compelling without being reliable",
      "doc-primer", "The problems with RLHF", "text",
      src=["confident-sounding hallucinations",
           "compelling to a person without being reliable enough for unattended automation"],
      book=["confident-sounding hallucinations",
            "compelling to a person without being reliable enough for unattended automation"])
claim("c03-07", 3, "DeepSeek-R1 abstract: performance on verifiable tasks such as mathematics, coding competitions, STEM",
      "r1", "abstract", "text",
      src=["verifiable tasks such as mathematics, coding competitions, and STEM fields"],
      book=["verifiable tasks such as mathematics, coding competitions, and STEM fields"])
claim("c03-08", 3, "Hoang: Jev rounds probabilities to two decimal places", "jev-3", "p.15", "text",
      src=["rounds probabilities to two decimal"], book=["rounds probabilities to two decimal places"])
claim("c03-09", 3, "Temperature scaling equivalence: softmax(z/T) == p^(1/T)/sum p^(1/T)", "derived", "algebra", "derived",
      book=["p_i^{1/T}"],
      expr="all(math.isclose(a, b) for a, b in zip([math.exp(z/2)/sum(math.exp(w/2) for w in (3.6,1.4,0.4)) for z in (3.6,1.4,0.4)], [(math.exp(z)/sum(math.exp(w) for w in (3.6,1.4,0.4)))**0.5/sum((math.exp(w)/sum(math.exp(v) for v in (3.6,1.4,0.4)))**0.5 for w in (3.6,1.4,0.4)) for z in (3.6,1.4,0.4)]))")

# ---- Chapter 4 -----------------------------------------------------------
claim("c04-01", 4, "Endpoint POST https://api.typesafe.ai/v1/systemone", "doc-quickstart", "Quickstart", "text",
      src=["POST https://api.typesafe.ai/v1/systemone"], book=["https://api.typesafe.ai/v1/systemone"])
claim("c04-02", 4, "Models page: alias moves; answers behind it can change without a change on your side; 64k context; jev-latest -> jev-1.13.0",
      "doc-models", "Aliases; Context length", "text",
      src=["without a change on your side", "64k tokens per request", "`jev-latest`", "`jev-1.13.0`"],
      book=["can change without a change on your side", "64,000 tokens per request"])
claim("c04-03", 4, "Changelog: v0.7.1 2026-09-21; v0.6.0 2026-09-15; Score.criteria ordered sequence",
      "doc-changelog", "versions", "text",
      src=["v0.7.1 (2026-09-21)", "v0.6.0 (2026-09-15)", "accept `Score.criteria` as an ordered sequence instead of a dictionary keyed by integers"],
      book=["0.7.1", "0.6.0", "ordered sequence instead of a dictionary keyed by integers"])
claim("c04-04", 4, "Hoang: 411 input tokens, ~two-thousandths of a cent", "jev-3", "p.10", "text",
      src=["411 input tokens", "roughly two-thousandths of"], book=["411 input tokens"])
claim("c04-05", 4, "411 tokens at $0.042/M = $0.0000173", "derived", "arithmetic", "derived",
      book=["$0.0000173"], expr="abs(411*0.042/1e6 - 0.0000173) < 1e-7")
claim("c04-06", 4, "Cookbook: 54,000-char document, 13 calls 2.71 s $0.00609 vs one call 0.27 s $0.000497",
      "jev-3", "section 7.1, p.16", "text",
      src=["54,000-character document", "2.71 seconds", "$0.00609", "0.27 seconds", "$0.000497"],
      book=["54,000-character document", "2.71 seconds", "$0.00609", "0.27 seconds", "$0.000497"])
claim("c04-07", 4, "0.00609/0.000497 is about 12.3x", "derived", "arithmetic", "derived",
      book=["about twelve times"], expr="abs(0.00609/0.000497 - 12.25) < 0.1")
claim("c04-08", 4, "Launch: 70ms-500ms end to end; evals run from laptops on the West Coast", "launch", "Speed; Evidence", "text",
      src=["70ms-500ms", "generally run from our laptops on the West Coast"],
      book=["70ms-500ms", "generally run from our laptops on the West Coast"])
claim("c04-09", 4, "Price $0.042 per million input tokens, output free", "doc-models", "Price", "text",
      src=["0.042", "Output tokens are free"], book=["$0.042 per million input tokens"])

# ---- Chapter 5 -----------------------------------------------------------
claim("c05-01", 5, "Hoang accuracy: Jev 81.1% (79.6-82.4); Qwen 76.4% (74.8-77.8)", "jev-3", "section 8.2, p.19-20; Fig 15", "image",
      book=["81.1% (79.6 to 82.4)", "76.4% (74.8 to 77.8)"])
claim("c05-02", 5, "Hoang: +4.7 points, interval +3.7 to +5.7 (paired bootstrap)", "jev-3", "Fig 15, p.20", "text",
      src=["+4.7 points, 95% interval [+3.7, +5.7]"], book=["+4.7 percentage points", "+3.7 to +5.7"])
claim("c05-03", 5, "Hoang: median 245 ms vs 249 ms; input tokens 2,288 vs 1,350", "jev-3", "p.19-20", "text",
      src=["245 ms", "249 ms", "2,288", "1,350"], book=["245 ms", "249 ms", "2,288", "1,350"])
claim("c05-04", 5, "Hoang: Qwen produced 53 invalid labels, 1.72%", "jev-3", "p.20", "text",
      src=["53 invalid", "1.72%"], book=["53 invalid labels", "1.72 percent"])
claim("c05-05", 5, "53/3080 = 1.72%; 76.4+1.72 = 78.1; lead ~3 points", "derived", "arithmetic", "derived",
      book=["about 78.1 percent"],
      expr="abs(53/3080*100 - 1.72) < 0.01 and abs(76.4+53/3080*100 - 78.1) < 0.05 and abs((81.1-(76.4+53/3080*100)) - 3.0) < 0.1")
claim("c05-06", 5, "Confidence groups (n, gap, share x gap) and ECE 0.097 (Fig 11)", "jev-3", "Fig 11, p.14", "image",
      book=["| Below 0.5 | 117 | 0.01 | 0.001 |", "| Exactly 1.00 | 1,516 | 0.03 | 0.014 |", "0.097"])
claim("c05-07", 5, "Group sizes sum to 3,080; weighted gaps sum to 0.097", "derived", "arithmetic", "derived",
      book=["sum to 3,080", "0.097"],
      expr="117+277+390+503+277+1516 == 3080 and abs(sum([0.001,0.015,0.035,0.026,0.006,0.014]) - 0.097) < 1e-9")
claim("c05-08", 5, "Hoang: below 0.5 -> 0.41 avg confidence, 39% right; exactly 1.00 -> 1,516 msgs, 44 mistakes",
      "jev-3", "p.21", "image",
      book=["0.41", "39 percent", "97.1 percent", "44 mistakes"])
claim("c05-09", 5, "Hoang: 0.7-0.9 avg 0.81, 53% correct; 0.9-0.99 avg 0.95, 79% correct", "jev-3", "p.21", "text",
      src=["average confidence of 0.81", "53%", "average confidence was 0.95", "79%"],
      book=["average confidence was 0.81", "53 percent", "average confidence was 0.95", "79 percent"])
claim("c05-10", 5, "1 - 44/1516 = 97.1%", "derived", "arithmetic", "derived",
      book=["97.1 percent"], expr="abs((1-44/1516)*100 - 97.1) < 0.05")
claim("c05-11", 5, "Primer: outcomes assigned probability 1.0 should occur 100% of the time", "doc-primer", "RLCD", "text",
      src=["should occur 100% of the time"], book=["should occur 100% of the time"])
claim("c05-12", 5, "Other evaluators via Hoang: ECE 0.082/0.079/0.325; 40 predictions at 1.000; 100% at >=0.99 covering 60.2%; 30 out-of-category at >=0.99; 44.7% / 0.74",
      "jev-3", "p.14-15, 17-18", "text",
      src=["0.082", "0.079", "0.325", "all 40 predictions", "60.2%", "all 30 out-of-category", "44.7%", "0.74"],
      book=["0.082", "0.079", "0.325", "all 40 predictions", "60.2 percent", "30 messages", "44.7 percent", "0.74"])
claim("c05-13", 5, "Archestra: 79% of tool calls harmless, so constant baseline scores 79%; 75% is worse", "archestra", "The Trivial Stuff", "text",
      src=["Calls like these make up 79% of our dataset", "A model scoring 75% is worse than that baseline"],
      book=["Seventy-nine percent", "A model at 75 percent is worse"])
claim("c05-14", 5, "Archestra table: Sonnet 5 98% / 44% (4/9); Jev 93% / 78% (7/9); constant 79% / 0%",
      "archestra", "results table", "text",
      src=["Sonnet 5  | 98%  | N/A  | 44% (4/9)", "(jev-latest)  | 93%  | 95%  | 78% (7/9)", "Majority Baseline (Constant)  | 79%  | 79%  | 0%"],
      book=["| Sonnet 5 | 98% | 44% (4 of 9) |", "| Jev (`jev-latest`) | 93% | 78% (7 of 9) |", "| Always answer \"benign\" | 79% | 0% |"])
claim("c05-15", 5, "Archestra: 337 of 400 decisions where all three judge families agreed", "archestra", "How we ran", "text",
      src=["337 decisions where all three judge families agreed", "400 decisions"], book=["337 of 400"])
claim("c05-16", 5, "Four of seven models scored below the 79% constant (zero-shot)", "derived", "from Archestra table", "derived",
      book=["Four of the seven models tested scored below the constant 79 percent"],
      expr="sum(1 for x in [98,93,83,63,64,54,48] if x < 79) == 4")
claim("c05-17", 5, "Archestra: Sonnet's eight errors on the strict set were all leaks", "archestra", "Live Examples", "text",
      src=["It made eight errors on the strict set, and all eight were leaks"],
      book=["eight errors on the strict set was a leak"])
claim("c05-18", 5, "Archestra stability: 394-398/400 labels identical; 35-39% bit-identical; drift up to 0.17; 5-7 per 100; ~4 in 100; 1.5-2 points",
      "archestra", "How stable is Jev itself", "text",
      src=["394 to 398", "35% to 39%", "0.17", "5 to 7 calls per 100", "about 4 in 100", "1.5 to 2 percentage points"],
      book=["394 to 398 of 400", "35 to 39 percent", "0.17", "five to seven calls per hundred", "about four in a hundred", "1.5 to 2 points"])

# ---- Chapter 6 -----------------------------------------------------------
claim("c06-01", 6, "Cascade table rows (thresholds, shares, cascade accuracy, random routing)", "jev-3", "section 8.3, p.20-21", "image",
      book=["| at least 0.5 | 96.2% | 80.7% | 80.9% |", "| at least 0.7 | 87.2% | 80.5% | 80.5% |",
            "| at least 0.9 | 74.5% | 79.7% | 79.9% |", "| at least 0.99 | 58.2% | 77.6% | 79.1% |",
            "| exactly 1.00 | 49.2% | 76.9% | 78.7% |"])
claim("c06-02", 6, "Hoang: fixed 84 mistakes, introduced 211; Qwen 57% on forwarded", "jev-3", "section 8.4, p.22", "text",
      src=["fixed 84 mistakes", "introduced 211 new ones", "57%"],
      book=["fixed 84 mistakes", "211 new ones", "57 percent"])
claim("c06-03", 6, "Guide: $30,400 vs $6,480, 79%, 800,000 tickets, 62/18/20 illustrative", "guide", "p.11 (also page image)", "text",
      src=["$30,400", "$6,480", "800,000", "The 62/18/20 split is illustrative"],
      book=["$30,400", "$6,480", "800,000", "illustrative"])
claim("c06-04", 6, "Guide cost arithmetic reproduces: 1M*0.0304 = 30,400; 1M*0.0004 + 200k*0.0304 = 6,480; saving 78.7%",
      "derived", "arithmetic", "derived", book=["78.7 percent"],
      expr="round(1e6*0.0304)==30400 and round(1e6*0.0004+2e5*0.0304)==6480 and abs((1-6480/30400)*100-78.7)<0.05")
claim("c06-05", 6, "Forwarded-subset bookkeeping: Jev ~66% vs Qwen ~57% on the 1,564 forwarded; net -127; 4.12 points",
      "derived", "arithmetic from reported figures", "derived",
      book=["about 66 percent", "127", "4.12 points"],
      expr="(lambda N,kept,kw: (lambda jc: abs((jc-(kept-kw))/(N-kept)*100-65.6)<0.2 and abs(127/N*100-4.12)<0.01 and 84-211==-127)(round(0.811*N)))(3080,1516,44)")
claim("c06-06", 6, "LangChain reports that Browserbase rebuilt Stagehand's act() so Jev picks the action, with anything below a 0.7 confidence threshold falling back to an LLM; in early testing median act() latency fell from 1.97 s to 0.46 s (about 4.3x). Latency only; no accuracy figure.",
      "langchain", "Browser automation", "text",
      src=["0.7 confidence threshold", "1.97 seconds to 0.46 seconds", "4.3x"],
      book=["0.7 confidence threshold", "1.97 seconds to 0.46", "4.3 times"])
claim("c06-07", 6, "Archestra: among predictions with confidence >= 0.7 Jev made no errors", "archestra", "Position Priors & Calibration", "text",
      src=["confidence of at least 0.7, it made no errors"], book=["no errors among predictions at 0.7 or above"])

# ---- Chapter 7 -----------------------------------------------------------
claim("c07-01", 7, "Laya README: base checkpoints 0.362/0.352 vs random 0.318, majority 0.461; 0.766 from fine-tuned checkpoint",
      "laya", "Honest limits", "text",
      src=["0.362 and 0.352", "0.318 random baseline", "0.461 majority-class baseline", "a fast base to specialise, not a zero-shot decision engine"],
      book=["0.362 and 0.352", "0.318", "0.461", "a fast base to specialise, not a zero-shot decision engine"])
claim("c07-02", 7, "Laya README: Banking77 Jev 0.870 (72 labels) vs Laya 0.425 (77 labels); 3-4 tokens per label", "laya", "Where Jev leads", "text",
      src=["0.870", "0.425", "3 to 4 tokens per label"], book=["0.425", "0.870", "three or four tokens per label"])
claim("c07-03", 7, "Laya README: negation examples, 0.9998; narrow examples", "laya", "Honest limits", "text",
      src=["0.9998", "These are narrow cancellation examples"], book=["0.9998", "narrow examples"])
claim("c07-04", 7, "Archestra: Laya flagged all calls: 100% recall, 12% precision", "archestra", "results note", "text",
      src=["100% recall but just 12% precision"], book=["100 percent recall and about 12 percent precision"])
claim("c07-05", 7, "GLiNER post: 60.1%, JevK5 57.5, SemIf 56.4, Laya 46.6; 5,100 examples, 17 datasets; not JevBench; JevK5 open reproduction",
      "gliner-post", "benchmark", "text",
      src=["60.1%", "57.5%", "56.4%", "46.6%", "5,100 test examples across 17 datasets",
           "This is an internal benchmark, not JevBench, and JevK5 is an open reproduction rather than TypeSafe"],
      book=["60.1 percent", "57.5", "56.4", "46.6", "5,100", "This is an internal benchmark, not JevBench, and JevK5 is an open reproduction rather than TypeSafe"])
claim("c07-06", 7, "GLiNER model card: 60.2 and 57.6; does not reason, explain, or answer open questions; 340M",
      "gliner-card", "card", "text",
      src=["60.2%", "57.6%", "It does not reason, explain, or answer open questions", "340M"],
      book=["60.2 and 57.6", "does not reason, explain, or answer open questions", "340M"])
claim("c07-07", 7, "Decision 1.0: six models; 54 tasks, 3,766 decisions; Lux 76.94; hosted Jev 81.05; budgets 1,024 / 16,384; planned next",
      "decision1", "post", "text",
      src=["3,766", "54-task", "76.94", "81.05", "1,024 tokens", "16,384 tokens", "planned next"],
      book=["3,766", "54-task", "76.94", "81.05", "1,024", "16,384", "planned next"])
claim("c07-08", 7, "AnyJev: raw gives a ranking not a probability; L0 cost K prompts; L1 100-500 labels; L2 max(8, 2K), 100-300",
      "anyjev", "levels", "text",
      src=["What you get: a ranking. What you do not get: a probability", "Cost: K prompts per choice question",
           "100 to 500 labeled examples", "max(8, 2K) labels and in practice 100-300"],
      book=["a ranking. What you do not get: a probability", "K prompts", "100 to 500 labeled examples", "max(8, 2K)", "100 to 300"])
claim("c07-09", 7, "SemIf: independent, reproduces the interface pattern, not Jev's model; probabilities conditional on options; calibration does not change selected option",
      "semif", "README", "text",
      src=["it does not reproduce Jev's undisclosed model or training", "Returned probabilities are conditional on the supplied options",
           "Calibration does not change the selected option"],
      book=["it does not reproduce Jev's undisclosed model or training", "conditional on the supplied options",
            "leaves the selected option unchanged"])
claim("c07-10", 7, "Archestra: Qwen 0.6B always A; MiniCPM-2B always last; 9 examples +20 to +34 pts; SemIf-4B 92 of 100", "archestra", "Position Priors", "text",
      src=["Qwen 0.6B always chose A", "always chose the last option", "20 to 34 percentage points", "92 of 100"],
      book=["always chose option A", "always chose the last option", "20 to 34 points", "92 of 100"])
claim("c07-11", 7, "Graham: Laya 421M; never shot 'not once, in any test'; should-I-shoot fix; still doesn't work; Claude wrote basically all the code",
      "lasa", "article", "text",
      src=["421-million-parameter", "Not once, in any test", "should I shoot", "still doesn't work", "Claude wrote basically all the code"],
      book=["421-million-parameter", "Not once, in any test", "should I shoot", "still doesn't work", "wrote basically all the code"])

# ---- Chapter 8 (run the lab) ----------------------------------------------
claim("c08-01", 8, "Lab metrics on six synthetic cases: accuracy 0.833, majority 0.500, Brier 0.381, NLL 0.657, ECE 0.225, coverage 0.500, selective accuracy 0.667",
      "lab", "examples/decision_workflow.py", "derived",
      book=["0.833", "0.500", "0.381", "0.657", "0.225", "0.667"],
      expr="LAB_OK")
claim("c08-02", 8, "Docs: thresholds are not one number; 0.5 floor; 0.9 for the transfer example", "doc-confidence", "Thresholds scale with risk", "text",
      src=["A confidence threshold is not one number", "confidence < 0.5", "confidence > 0.9",
           "The correct threshold values depend on your domain and the performance of the model for your use case"],
      book=["is not one number", "0.9", "correct threshold values depend on your domain and the performance of the model for your use case"])
claim("c08-03", 8, "Guide's transfer example uses 0.85", "guide", "p.8-9", "text", src=["0.85"], book=["0.85"])

# ---- Chapter 9 -----------------------------------------------------------
claim("c09-01", 9, "Notes: incentive laundering; generative AI can pollute content, decision AI can silently alter outcomes",
      "notes", "sections", "text",
      src=["incentive laundering", "Generative AI can pollute content. Decision AI can silently alter outcomes"],
      book=["incentive laundering", "Generative AI can pollute content. Decision AI can silently alter outcomes"])
claim("c09-02", 9, "Notes: six firewall capabilities and ten additional problems (names)", "notes", "sections 1-6; Additional problems", "text",
      src=["### 1. Decision receipts", "### 6. Outcome-based monitoring", "Decision monoculture", "Objective drift",
           "Threshold laundering", "Context poisoning", "Selective invocation", "Automation asymmetry", "Appeal blindness",
           "Proxy discrimination", "False neutrality", "Responsibility diffusion", "from 0.85 to 0.61"],
      book=["Threshold laundering", "Selective invocation", "Automation asymmetry", "Appeal blindness", "Proxy discrimination",
            "False neutrality", "Responsibility diffusion", "from 0.85 to 0.61", "decision monoculture, objective drift and context poisoning"])
claim("c09-03", 9, "Ten failure modes counted in the notes", "derived", "count", "derived", book=["The notes list ten"],
      expr="len(['Decision monoculture','Objective drift','Threshold laundering','Context poisoning','Selective invocation','Automation asymmetry','Appeal blindness','Proxy discrimination','False neutrality','Responsibility diffusion'])==10")
claim("c09-04", 9, "Notes: risk formula R = I x U x V x A", "notes", "A useful risk model", "text",
      src=["R = I \\times U \\times V \\times A"], book=["R = I \\times U \\times V \\times A"])
claim("c09-05", 9, "NIST: Core is composed of four functions: govern, map, measure, manage; actions not a checklist", "nist", "AI RMF Core", "text",
      src=["Core is composed of four functions", "Actions do not constitute a checklist"],
      book=["is composed of four functions: govern, map, measure, and manage", "do not constitute a checklist"])

# ---- Chapter 10 ----------------------------------------------------------
claim("c10-01", 10, "PDF: not affiliated with or endorsed by TypeSafe; as provided to the compiler; illustrative estimate", "eng", "cover; p.12", "text",
      src=["Not affiliated with or endorsed by TypeSafe", "as provided to the compiler", "an illustrative estimate"],
      book=["as provided to the compiler", "an illustrative estimate"])
claim("c10-02", 10, "PDF: path totals 25Y+5Z and 3X+20Y+8Z; X=0.65 Y=0.12 Z=0.23 -> 4.15 vs 6.19", "eng", "p.4", "text",
      src=["total     25Y + 5Z", "total     3X + 20Y + 8Z", "X = 0.65, Y = 0.12, Z = 0.23", "4.15", "6.19"],
      book=["25*Y* + 5*Z*", "3*X* + 20*Y* + 8*Z*", "*X* = 0.65", "4.15", "6.19"])
claim("c10-03", 10, "Routing arithmetic recomputed: totals, components, difference 3X-5Y+3Z = 2.04, break-even 3(X+Z) < 5Y",
      "derived", "arithmetic", "derived", book=["2.04"],
      expr="(lambda X,Y,Z: math.isclose(25*Y+5*Z,4.15) and math.isclose(3*X+15*Y+3*Z+5*(Y+Z),6.19) and math.isclose(3*X-5*Y+3*Z,2.04) and math.isclose(3*X+15*Y+3*Z+5*(Y+Z)-(25*Y+5*Z), 3*X-5*Y+3*Z))(0.65,0.12,0.23)")
claim("c10-04", 10, "PDF token-share ranges (read files 30-40, search 10-18, command output 10-20, overhead 5-12, reasoning 5-15, writing 4-10) and fastcontext 56.2% / 46.5%",
      "eng", "p.5-6", "text",
      src=["30–", "40%", "10–", "18%", "20%", "12%", "15%", "10%", "56.2%", "46.5%"],
      book=["30 to 40 percent", "10 to 18", "10 to 20", "5 to 12", "5 to 15", "4 to 10", "56.2 percent", "46.5 percent"])
claim("c10-05", 10, "Drone table: 500 Hz controller, 50 Hz guidance and safety reflex, 15 Hz classical CV, ~2.5 Hz Jev advisory only; quote",
      "guide", "p.16", "image",
      book=["500 Hz", "50 Hz", "15 Hz", "2.5 Hz", "cannot be the perception layer, and it cannot run at control rate"])
claim("c10-06", 10, "PDF table I: hide/short/long/full; allow/ask/deny; sensitivity score", "eng", "p.3", "text",
      src=["hide /", "allow / ask / deny", "sensitivity score"], book=["hide, short, long or full", "allow, ask or deny", "sensitivity score"])

# ---- Chapter 11 / appendices ----------------------------------------------
claim("c11-01", 11, "Archestra: ~90 of 100 routine, ~10 dangerous; original benchmark was bad", "archestra", "What Error Analysis Actually Taught Us", "text",
      src=["Around 90 were routine", "only 10 covered the dangerous edge cases", "our original benchmark was bad"],
      book=["around 90 of 100", "\"bad.\""])


# ---- Planned: for the ecosystem chapter, bound to sources before they are written ----
claim("p-01", 7, "Decision 1.0 (post dated September 22, 2026) says it uses the upstream System One request format: state, model, and named questions",
      "decision1", "Bring your System One workflow", "text",
      src=["Decision uses the upstream System One request format: state, model, and named questions", "September 22, 2026"],
      planned=True)
claim("p-02", 7, "TypeSafe's launch post is dated September 15, 2026",
      "launch", "post header", "text", src=["Sep 15, 2026"], planned=True)
claim("p-03", 7, "Seven days between the launch (Sep 15) and the Decision 1.0 post (Sep 22); my arithmetic, so 'a week after launch', not 'within a week'",
      "derived", "arithmetic", "derived", expr="22 - 15 == 7", planned=True)
claim("p-04", 7, "LangChain, describing a shift it attributes to Jaya Gupta, quotes 'frontier by default and optimize later' giving way to 'cheap by default, frontier on exception'; the framing is Gupta's as quoted by LangChain, not LangChain's own",
      "langchain", "This is the great unbundling of intelligence", "text",
      src=['Jaya Gupta calls what comes next "the Great Unbundling of Intelligence"',
           'That\'s the shift Gupta describes from "frontier by default and optimize later" to "cheap by default, frontier on exception."'],
      planned=True)


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("−", "-").replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s)


def load_lab():
    sys.path.insert(0, str(ROOT / "examples"))
    import decision_workflow as dw  # noqa: E402
    m = dw.metrics(dw.SYNTHETIC, 0.8)
    ok = (round(m["accuracy"], 3) == 0.833 and round(m["majority_baseline"], 3) == 0.5
          and round(m["multiclass_brier"], 3) == 0.381 and round(m["negative_log_likelihood"], 3) == 0.657
          and round(m["top_label_ece"], 3) == 0.225 and round(m["policy_coverage"], 3) == 0.5
          and round(m["policy_selective_accuracy"], 3) == 0.667)
    refund = dw.policy(dw.Prediction({"billing": 1.0, "technical": 0.0, "other": 0.0}, "s"),
                       evidence_present=True, action="refund")
    return ok and refund == {"status": "review", "reason": "action_outside_auto_policy"}


def main() -> int:
    manuscript = norm((ROOT / "output" / "manuscript.md").read_text(encoding="utf-8"))
    cache, failures = {}, []
    lab_ok = None
    for c in CLAIMS:
        problems = []
        if c["verify"] == "text":
            if c["source"] not in cache:
                cache[c["source"]] = norm(SOURCES[c["source"]].read_text(encoding="utf-8", errors="replace"))
            for n in c["src_needles"]:
                if norm(n) not in cache[c["source"]]:
                    problems.append("source missing: %r" % n)
        elif c["verify"] == "derived":
            expr = c["expr"]
            if expr == "LAB_OK":
                if lab_ok is None:
                    lab_ok = load_lab()
                ok = lab_ok
            else:
                ok = bool(eval(expr, {"math": math, "__builtins__": {"abs": abs, "round": round, "sum": sum,
                                                                       "all": all, "zip": zip, "len": len}}))
            if not ok:
                problems.append("derived check false")
        for n in c["book_needles"]:
            if norm(n) not in manuscript:
                problems.append("book missing: %r" % n)
        c["status"] = "pass" if not problems else "FAIL"
        c["problems"] = problems
        if problems:
            failures.append(c)
    ledger = R / "book-claims.jsonl"
    with ledger.open("w", encoding="utf-8", newline="\n") as fh:
        for c in CLAIMS:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    by = {}
    for c in CLAIMS:
        by[c["verify"]] = by.get(c["verify"], 0) + 1
    print("claims: %d  (text %d, image %d, derived %d)  failures: %d" % (
        len(CLAIMS), by.get("text", 0), by.get("image", 0), by.get("derived", 0), len(failures)))
    for c in failures:
        print("FAIL %s (ch %s) %s" % (c["id"], c["ch"], c["statement"][:80]))
        for p in c["problems"]:
            print("     -", p)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
