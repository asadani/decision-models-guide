"""Spoken versions of the elements that cannot be read aloud as written.

Keyed by (chapter file prefix, kind, ordinal). Kinds: table, code, figure, math.
Ordinals count each kind in document order within the file, starting at 1.
scripts/make_narration.py fails if an element has no entry here, so a new table
or figure cannot silently drop out of the audio.
"""

SAY = {
    # ---- Chapter 1 ---------------------------------------------------------
    ("01", "code", 1): (
        "In code, that contract has three fields. The state, which is the customer's message. "
        "The question: which team should handle this? And the options: billing, technical, or other."),
    ("01", "figure", 1): (
        "Figure one shows the contract. Code prepares the evidence from the ticket text. The question and "
        "the allowed answers join it, and both go into the decision component, which returns a typed "
        "prediction. That prediction passes through validation and application policy, both written by "
        "the application, which either routes the ticket or requests evidence or review."),
    ("01", "table", 1): (
        "Here is how to sort the work. Does the invoice total equal the sum of its line items? Start with "
        "exact arithmetic in code. Does this message ask for a refund? A semantic classifier, or a decision "
        "model. Which of our permitted queues fits best? A rules baseline first, then a decision model. "
        "What should a helpful reply say? A template, or a generative model. And may this account receive "
        "money? Verified business facts and an authorization policy, with any learned judgment kept explicit."),
    # ---- Chapter 2 ---------------------------------------------------------
    ("02", "table", 1): (
        "Ten invented tickets. Ticket one: billing, zero point nine seven, right. Ticket two: billing, zero "
        "point nine five, right. Ticket three: technical, zero point nine three, right. Ticket four: technical, "
        "zero point nine two, right. Ticket five: billing, zero point nine zero, wrong. Ticket six: technical, "
        "zero point seven five, right. Ticket seven: other, zero point seven zero, right. Ticket eight: "
        "billing, zero point six five, wrong. Ticket nine: technical, zero point six zero, right. Ticket "
        "ten: other, zero point five five, wrong."),
    # ---- Chapter 3 ---------------------------------------------------------
    ("03", "table", 1): (
        "There are three primitives. Choice takes up to two hundred fifty-five options, each with a "
        "description, and returns the selected option and a probability for every option. Noul takes a "
        "yes-or-no statement and returns the probability that it is true. Score takes two to ten ordered "
        "levels, described in words, and returns a probability for each level and their "
        "probability-weighted mean."),
    # ---- Chapter 5 ---------------------------------------------------------
    ("05", "code", 1): (
        "The code defines three named questions. A Choice called team, with billing, technical, and other "
        "as its criteria. A Noul called refund requested, which asks whether the message explicitly "
        "requests a refund, rather than only describing a charge. And a Score called urgency, with three "
        "ordered levels: no time pressure stated, time-sensitive without a stated outage, and a current "
        "service outage. It then opens a client pinned to model version jev one point thirteen point zero, "
        "with a twenty-second timeout, and sends the message together with one extra fact in the state: "
        "the account has not been verified."),
    # ---- Chapter 6 ---------------------------------------------------------
    ("06", "figure", 1): (
        "Figure two charts the gap between the confidence Jev reported and how often it was right, in six "
        "confidence groups. The gaps are about zero point zero one below zero point five, zero point one "
        "seven from zero point five to zero point seven, zero point two seven from zero point seven to zero "
        "point nine, zero point one six from zero point nine to zero point nine nine, zero point zero seven "
        "from zero point nine nine to just below one, and zero point zero three at exactly one. The largest "
        "gap is the middle group, from zero point seven to zero point nine. The full table is in Appendix D."),
    # ---- Chapter 7 ---------------------------------------------------------
    ("07", "figure", 1): (
        "Figure three charts accuracy against the share of cases Jev keeps. Jev alone scores eighty-one "
        "point one percent, and Qwen alone seventy-six point four. With the confidence gate, accuracy climbs "
        "from seventy-six point four to eighty-one point one as Jev keeps more. But at every point in "
        "between, random routing at the same share does as well or better. The full table is in Appendix D."),
    ("07", "figure", 2): (
        "Figure four shows the cascade. A primary prediction meets a frozen gate. Accepted cases become the "
        "primary decision. Forwarded cases go to a fallback, whose output is validated against the same "
        "schema and policy. The outcomes are joined, and both the whole cascade and the forwarded subset "
        "are measured."),
    ("07", "math", 1): (
        "In symbols: the accuracy of the fallback on the forwarded subset S must be greater than the "
        "accuracy of the primary on that same subset."),
    ("07", "math", 2): (
        "In symbols: the cost per case is the primary cost, plus q times the fallback cost, plus the costs "
        "of retrieval, policy, and handoff, where q is the fraction of cases forwarded."),
    # ---- Chapter 8 ---------------------------------------------------------
    ("08", "table", 1): (
        "Six candidates. Jev, from TypeSafe: hosted, closed weights, a typed-decision API. Test whether its "
        "uncertainty separates automation from review on your cases. Laya: open encoder checkpoints, with a "
        "Jev-compatible request shape. Test which checkpoint you need, and whether your options fit its "
        "option budget. Decision one point zero: six open-weight models, from six-tenths of a billion to "
        "nine billion parameters, in encoder and adapted-decoder branches. Test which release and runtime "
        "fit your evidence length and latency. GLiNER two point five Decide: a three hundred forty million "
        "parameter open English encoder, with labels supplied at call time. Test whether your task is "
        "classification, and whether its benchmark resembles yours. AnyJev: a toolkit that reads and "
        "debiases an existing language model's option probabilities. Test what each level needs, and what "
        "it does not fix. And SemIf: an independent open-model reproduction of the interface. Test how "
        "option wording and order change the result."),
    # ---- Chapter 10 ---------------------------------------------------------
    ("10", "code", 1): (
        "The policy function does five things, in order. It validates the prediction, and a malformed one "
        "goes to review as an invalid prediction. It checks that the needed evidence is present, and if "
        "not, sends it to review for missing evidence. It checks that the requested action is one the "
        "policy allows automatically, and anything other than routing goes to review as an action outside "
        "automatic policy. It sends a tie for the top probability to review. And it sends the answer other, "
        "or any top probability below the threshold, to review as uncertain. Only then does it return a "
        "route to the winning label."),
    ("10", "table", 1): (
        "Accuracy: zero point eight three three, which is five of six. The majority-class baseline: zero "
        "point five. The multiclass Brier score: zero point three eight one. Negative log likelihood: zero "
        "point six five seven. Top-label expected calibration error: zero point two two five. Policy "
        "coverage: zero point five, meaning three of six were routed. And selective accuracy: zero point "
        "six six seven, meaning two of the three routed cases were right."),
    # ---- Chapter 11 ---------------------------------------------------------
    ("11", "code", 1): (
        "In code, that is a single line: if the approval probability is greater than zero point eight, "
        "approve the application."),
    ("11", "figure", 1): (
        "Figure five shows the control service. Evidence with provenance feeds the model's judgment. That "
        "judgment, the declared objective and conflicts, and the versioned policy and authority all feed "
        "the decision control service. The service either requests review or more evidence, or permits an "
        "action. Both paths write a decision and review record. That record feeds outcome and appeal "
        "monitoring, which feeds evaluation of policy or model changes, which in turn refines the service."),
    # ---- Chapter 12 --------------------------------------------------------
    ("12", "table", 1): (
        "Six decision points. Context: how visible should this chunk be for this query? The answer is hide, "
        "short, long, or full. Cache: reuse the cached prefix, or rebuild? A yes-or-no probability. "
        "Routing: can this subtask leave the frontier model? A choice, plus a cost estimate. Tools: which "
        "tool fits this intent? A ranked choice. Permissions: should this command run? Allow, ask, or deny. "
        "And security: which files will this task touch? A sensitivity score. Every row is a proposal from "
        "the supplied document."),
    ("12", "figure", 1): (
        "Figure six shows the proposed loop. Versioned task state and repository facts feed retrieval of "
        "candidate context. Relevance and routing judgments follow, and then code assembles a bounded "
        "context. A generator proposes a patch or a tool action. Permissions and deterministic validation "
        "gate it before the tool executes, and the result returns to the task state. Read-only evaluation "
        "and review read from that state."),
    ("12", "table", 2): (
        "Staying on the frontier model throughout costs twenty-five Y plus five Z. Having the frontier "
        "model plan, a cheaper model execute, and the frontier model review costs three X plus twenty Y "
        "plus eight Z."),
    # ---- Chapter 13 --------------------------------------------------------
    ("13", "figure", 1): (
        "Figure seven shows the protocol. Labeled cases with provenance are split before tuning, keeping "
        "related cases together. Development data shapes wording and taxonomy. Calibration data sets "
        "thresholds and transforms. The test set stays frozen. Development and calibration feed a frozen "
        "candidate configuration, which is evaluated once on the test set. The report covers quality, "
        "coverage, and failure costs."),
    ("13", "table", 1): (
        "There are seven things to measure. Accuracy and the majority baseline, so you know whether the "
        "model beats a trivial answer. The common mistake is ignoring class imbalance. Per-class precision "
        "and recall and the confusion matrix, to see which mistakes it makes. The mistake is reporting "
        "only an average. Brier score or negative log likelihood, to judge the distributions and not only "
        "the winner. Reliability bins and calibration error, to check whether the probability matches "
        "outcomes. The mistake is calling any confidence field a probability. Coverage and selective risk: "
        "how much is automated, and how often that is wrong. The mistake is quoting high accepted accuracy "
        "without the accepted volume. Latency and cost over the whole workflow, not only warm model time. "
        "And repeated and permuted inputs, because a typed schema does not make answers repeatable near "
        "the threshold."),
}

# Inline math and other exact strings, replaced before any other processing.
INLINE = {
    "$(p_{ik} - y_{ik})^2$": "the squared difference between each predicted probability and the true outcome",
    "$B_b$": "the bin",
    "$\\sum_b \\frac{|B_b|}{N}\\,\\bigl|\\operatorname{accuracy}(B_b) - \\overline{p}_{\\text{top}}(B_b)\\bigr|$":
        "the size-weighted sum, over bins, of the gap between each bin's accuracy and its mean top probability",
    "$y$": "y",
    "$R = I \\times U \\times V \\times A$": "R equals I times U times V times A",
    "$3(X + Z)$": "three times X plus Z",
    "$3X - 5Y + 3Z$": "three X minus five Y plus three Z",
    "$5Y$": "five Y",
}
