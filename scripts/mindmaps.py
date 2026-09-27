"""Mindmaps: one per chapter, plus one for the whole book.

MAPS is the single source for each map's content. This script turns it into
TikZ sources (assets/diagrams/src/map-*.tex), which scripts/render_diagrams.py
renders to PNG. scripts/make_narration.py reads the same data for the spoken
recap, so the picture and the audio cannot drift apart.

Run:  python scripts/mindmaps.py
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "diagrams" / "src"

# key -> (center, takeaway, [(label, detail), ...])
MAPS = {
    "book": (
        "A typed answer and a probability",
        "Three gaps to close: is it right, does the number mean what you think, and may anyone act on it.",
        [("What it is", "Plain-language idea, the contract, one real call"),
         ("Is it right?", "Measure on your own cases, not the launch numbers"),
         ("Does the number mean it?", "Calibration, checked on your population"),
         ("May anyone act?", "A written policy and a record between prediction and action"),
         ("What it changes", "The layer it adds, and the alternatives around it"),
         ("What to build", "One reversible decision first, then widen")],
    ),
    "ch01": (
        "The ticket",
        "One message hides three questions, and only the first two are for the model.",
        [("Which queue?", "A classification"),
         ("What does it ask?", "A reading of intent"),
         ("May anyone act?", "Not in the text: records and policy"),
         ("Sort the work", "Code, then model, then policy"),
         ("Valid is not correct", "A rate to measure, not a defect to fix"),
         ("Keep baselines", "A rules answer and a constrained LLM")],
    ),
    "ch02": (
        "The idea in plain language",
        "The model does not write an answer. It scores your options, and you decide what to do with the scores.",
        [("Decide, don't write", "One pass over your options"),
         ("A spread of odds", "Every option gets a probability"),
         ("Confidence", "How peaked the spread is"),
         ("Calibration", "Right as often as it says, over groups"),
         ("Accuracy and coverage", "A threshold trades one for the other"),
         ("How it is trained", "Claimed, and not published")],
    ),
    "ch03": (
        "What a decision model is",
        "A contract of state, question and permitted answers. It guarantees the shape, not the truth.",
        [("State", "The evidence you send"),
         ("Question", "Typed, literal, one thing"),
         ("Three primitives", "Choice, Noul and Score"),
         ("The schema buys", "No parsing, no stray text"),
         ("Jagged edges", "Literal, no arithmetic, no hostile-input defense"),
         ("Not known", "Size, data and architecture")],
    ),
    "ch04": (
        "Reading the numbers",
        "A probability is not a promise about one answer. It is a claim about a group of answers.",
        [("Probability", "Weight on each option"),
         ("Confidence", "One number, defined differently by each system"),
         ("Calibration", "Judged over groups, never one answer"),
         ("Training labels", "RLHF, RLVR and RLCD are different goals"),
         ("Rescaling", "Possible from probabilities alone"),
         ("Thresholds", "Do not carry over between systems")],
    ),
    "ch05": (
        "One real call",
        "You cannot reproduce a decision unless you wrote down what made it.",
        [("Pin the model", "Aliases move under you"),
         ("Literal questions", "Boundary cases in the criteria"),
         ("Facts in the state", "Account status is data, not a guess"),
         ("Ask together", "Related questions in one call"),
         ("Record it all", "Versions, schema, full distributions"),
         ("Fail closed", "A timeout executes nothing")],
    ),
    "ch06": (
        "A measured case",
        "Good on average and overconfident in the middle. A high number is not knowledge.",
        [("Accuracy", "Ahead of Qwen on this task, one setup"),
         ("Confidence bins", "The middle of the range is the worst"),
         ("Exactly 1.00", "Still wrong 44 times in 1,516"),
         ("No option fits", "It answers anyway, confidently"),
         ("The constant baseline", "Always saying benign scored 79 percent"),
         ("Labels and odds", "Labels stable, probabilities float")],
    ),
    "ch07": (
        "The cascade",
        "Knowing a case is hard for one model does not tell you another model can solve it.",
        [("The case for it", "Cheap model first, big model for the rest"),
         ("The test", "Measure on the forwarded subset"),
         ("The result", "Fixed 84 mistakes, broke 211"),
         ("Random routing", "Did at least as well as the gate"),
         ("Cost and latency", "The forwarded case pays for both calls"),
         ("Other fallbacks", "A lookup, a question, a person")],
    ),
    "ch08": (
        "The alternatives",
        "The request shape is shared. The behavior, limits and numbers are not.",
        [("Laya", "Open encoder, honest about its limits"),
         ("GLiNER", "Small, schema-driven, its own benchmark"),
         ("Decision 1.0", "Six open models, one request format"),
         ("AnyJev", "Reads and debiases an existing model"),
         ("SemIf", "Open reproduction of the interface"),
         ("Numbers", "Not interchangeable between setups")],
    ),
    "ch09": (
        "What changes around it",
        "A cheap decision layer changes how work is routed, and the shared interface may outlast any one model.",
        [("A new layer", "Between plain code and the large model"),
         ("Routing", "Cheap by default, large on exception"),
         ("A shared interface", "Open projects reuse the request shape"),
         ("Cost and speed", "Vendor claims, not yet independent"),
         ("Tooling", "Evaluation and tracing catch up"),
         ("New risks", "Correlated errors, and re-measuring on a swap")],
    ),
    "ch10": (
        "Between prediction and action",
        "A probability is evidence. Permission comes from policy, written and versioned.",
        [("Validate", "Is the prediction well formed"),
         ("Evidence", "Does the record exist"),
         ("Authority", "May this run without a person"),
         ("Confidence", "Only then, and never alone"),
         ("Beyond the score", "Prohibitions and failure paths"),
         ("A receipt", "A fingerprint is not an audit log")],
    ),
    "ch11": (
        "The accountability argument",
        "A neutral-looking probability can carry an objective nobody declared.",
        [("Incentive laundering", "A preference turned into a probability"),
         ("Calibrated for whom?", "Which objective, outcome and population"),
         ("Six controls", "Receipts, provenance, tests, judges, audits"),
         ("Failure modes", "Threshold drift, appeal blindness"),
         ("Outcomes", "Watch consequences, not just outputs"),
         ("A proposal", "No source shows it working yet")],
    ),
    "ch12": (
        "Coding agents",
        "Keep the loop, the safety and the arithmetic in code. Use the model for the narrow judgment.",
        [("A layer beside", "Not the model that writes code"),
         ("Routing costs", "Price by context rebuild, not per token"),
         ("Where tokens go", "Reading and searching dominate"),
         ("Advice, not authority", "A score never authorizes"),
         ("Tool choice", "Choosing a tool is not choosing its arguments"),
         ("Test it", "On your own sessions")],
    ),
    "ch13": (
        "What to build first",
        "The deliverable is a measured operating boundary, including what people keep.",
        [("One reversible decision", "Routing before refunds"),
         ("An evaluation set", "Ordinary, ambiguous, costly, stress"),
         ("Baselines", "A rules answer plus two candidates"),
         ("Tune and freeze", "On a separate split, then test once"),
         ("Shadow mode", "Compare, do not execute"),
         ("Widen slowly", "Limited routing, receipts, review")],
    ),
}


def esc(s: str) -> str:
    return (s.replace("\\", " ").replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
             .replace("_", r"\_").replace("$", r"\$"))


def spoken(key: str) -> str:
    """The recap read aloud in place of the picture."""
    center, takeaway, branches = MAPS[key]
    assert len(branches) == 6
    parts = ["%s, %s" % (label, detail[0].lower() + detail[1:]) for label, detail in branches]
    return "The map has %s at the center, with six branches. %s." % (center, ". ".join(parts))


def alt(key: str) -> str:
    center, takeaway, branches = MAPS[key]
    return "Mindmap. Center: %s. Branches: %s." % (
        center, "; ".join("%s (%s)" % (l, d) for l, d in branches))


def tikz(key: str) -> str:
    """A hub with three rows of two branches, left and right: a plain grid, not a

    circle, so the boxes line up and the sheet reads top to bottom like a page."""
    center, takeaway, branches = MAPS[key]
    assert len(branches) == 6
    col_x, row_y = 4.35, 1.9
    pts = [(-col_x, row_y), (col_x, row_y), (-col_x, 0), (col_x, 0), (-col_x, -row_y), (col_x, -row_y)]
    lines = [
        r"\documentclass[border=6pt]{standalone}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{tikz}",
        r"\usetikzlibrary{arrows.meta,positioning,shapes.geometric,calc,fit}",
        r"\begin{document}",
        r"\hyphenpenalty=10000 \exhyphenpenalty=10000",
        r"\begin{tikzpicture}[",
        r"  font=\footnotesize\sffamily,",
        r"  hub/.style={draw=red!55!black, line width=1pt, rounded corners=7pt, fill=red!8, align=center,",
        r"              text width=3cm, inner sep=7pt, font=\bfseries\small\sffamily},",
        r"  br/.style={draw=black!60, rounded corners=3pt, fill=black!3, align=center,",
        r"             text width=3.05cm, inner sep=4pt, minimum height=1.05cm},",
        r"  edge/.style={draw=black!45, line width=0.8pt}",
        r"]",
    ]
    lines.append(r"\node[hub] (hub) at (0,0) {%s};" % esc(center))
    for i, ((x, y), (label, detail)) in enumerate(zip(pts, branches)):
        name = "b%d" % i
        lines.append(r"\node[br] (%s) at (%.2f,%.2f) {\textbf{%s}\\[1pt]{\scriptsize %s}};"
                     % (name, x, y, esc(label), esc(detail)))
        lines.append(r"\draw[edge] (hub) -- (%s);" % name)   # TikZ clips to each node's border
    lines += [r"\end{tikzpicture}", r"\end{document}", ""]
    return "\n".join(lines)


def main() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    for key in MAPS:
        (SRC / ("map-%s.tex" % key)).write_text(tikz(key), encoding="utf-8", newline="\n")
    print("wrote %d mindmap sources to %s" % (len(MAPS), SRC))


if __name__ == "__main__":
    main()
