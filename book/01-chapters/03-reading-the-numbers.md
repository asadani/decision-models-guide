# Chapter 3. Reading the Numbers

Two dashboards sit side by side. Both report 80 correct out of 100 on a held-out set, for predictions whose top probability was about 0.8. On the first, the twenty misses each sent a ticket to the wrong queue, where a person moved it an hour later. On the second, the twenty misses each issued a refund nobody had approved.

The accuracy is identical and the dashboards are equally well calibrated. Nobody would automate both the same way. Calibration is the property that makes a probability usable, and it is silent on what you should do with it.

## Three numbers that get confused

A Choice or Score answer carries three things: the option probabilities, a selected answer, and a `confidence` field. They are different.

The probabilities are a distribution over your options and sum to one. The selected answer is the option with the most weight. The `confidence` field, the documentation says, is "a statistic computed from the probability distribution the answer already gives you": a single number from 0 to 1 for how concentrated the distribution is. Noul answers carry no confidence field, because the probability of yes already is the belief.[^ch3-1]

The practitioner report we return to in Chapter 5 hit the difference in its first call. A three-level anger question came back with 0.63 on its top level and a confidence of 0.44. The confidence is lower than the top probability because the other 0.37 sits on a single second level, so the distribution is split between two answers, not peaked on one.[^ch3-2]

The formula behind the field is not spelled out on the documentation page, which offers an approximation for three options and says you are "never locked into our definition." Another project's README states it for Jev as $(n \cdot p_{\max} - 1) / (n - 1)$, where $n$ is the number of options.[^ch3-3] Applied to the anger example, $(3 \times 0.63 - 1) / 2$ is about 0.445, which is consistent with the 0.44 that was reported. That is my arithmetic, and it is a consistency check, not a statement of TypeSafe's implementation.

The practical point is that another model's `confidence` can be a different statistic. The Laya model computes it as one minus normalized entropy and warns that "a threshold carried over from Jev does not transfer."[^ch3-3b] A confidence threshold is a property of the model and its version, and you validate it there.

## Calibration is about groups

One vendor page states the idea plainly. Across many predictions from a well-calibrated model, outcomes assigned 0.2 should occur about 20 percent of the time and outcomes assigned 0.8 about 80 percent. "These rates describe groups of predictions, not a guarantee about any single answer."[^ch3-4]

The report in Chapter 5 uses a weather forecaster to make it concrete. Across all the days a forecaster said 90 percent, it should have rained on about nine in ten. A model that says "90 percent sure" and is right half the time is overconfident, and its numbers cannot be relied on.[^ch3-2b] The test is never whether one 90 percent prediction was right, since no single outcome can be 90 percent right. It is whether predictions that carried similar confidence were right at roughly that rate.

Finite groups are noisy. Of 100 predictions near 0.8, seeing 78 or 83 correct tells you little. Seeing 55 correct tells you a lot. A reliability table needs group sizes and intervals alongside its percentages, which is why the experiment in Chapter 5 reports both.

## Where the numbers come from

TypeSafe says Jev is trained with a method it calls RLCD, reinforcement learning for calibrated decisions, which trains the model to return decisions and calibrated probabilities instead of generated text.[^ch3-5] The company sets this beside two better-known approaches. RLHF trains a model to produce responses people prefer; InstructGPT is the standard research example.[^ch3-6] RLVR rewards outputs that can be checked automatically, such as the answer to a math problem. It is associated with reasoning-model work such as DeepSeek-R1, whose abstract reports strong performance "on verifiable tasks such as mathematics, coding competitions, and STEM fields."[^ch3-7]

TypeSafe's argument is that RLHF can reward sycophancy and confident-sounding hallucinations, and that an output can be compelling to a person without being reliable enough for unattended automation.[^ch3-5b] That is a claim about a training objective. The recipe for RLCD itself has not been published, and I did not find anything independent that reproduces it.

Keep the three labels apart. One of the supplied notes describes RLCD as building on RLVR. TypeSafe's own primer lists them as three separate paths, and that is the framing to use. A reward for reaching a correct answer and a reward for reporting honest uncertainty target different properties. A model trained for either could still be badly calibrated on a population it wasn't trained on. That is what Chapter 5 measures.

## Recalibrating after the fact

If reported probabilities do not match outcomes on your data, you can adjust them. Temperature scaling, studied by Guo and colleagues in 2017, divides a model's raw scores by a single number *T* before they become probabilities.[^ch3-8] It softens an overconfident model without changing which answer ranks first.

A hosted API returns probabilities, not raw scores, and one practitioner concludes that temperature scaling is therefore unavailable.[^ch3-2c] The conclusion is too strong. If the returned probabilities are positive, they are the softmax of some raw scores, and dividing those scores by *T* gives the same result as raising each probability to the power 1/*T* and renormalizing:

$$
q_i = \frac{p_i^{1/T}}{\sum_j p_j^{1/T}}, \qquad T > 0.
$$

Fit *T* on a labeled calibration set that is separate from anything you tuned prompts on. For any *T* above zero, the ranking of options is preserved, so the winner does not change. Only the sharpness does. The catch is precision: Jev rounds probabilities to two decimal places, so an answer of 1.00 and 0.00 carries almost no information to rescale.[^ch3-2d] Isotonic regression, which learns a correction curve from labeled examples, works from the returned probabilities alone and is the safer choice for API users.[^ch3-2e]

Neither method recovers evidence that was never in the state, and neither repairs a wrong ranking.

## In practice

- Decide which signal you will threshold on, the `confidence` field or the largest option probability, and measure both. The report in Chapter 5 found them nearly identical on one dataset; another evaluation it cites found the largest probability tracked accuracy better.
- Do not carry a threshold across models, model versions, or question types.
- Report calibration with group sizes and intervals. A percentage without an *n* is a rumor.
- Set the automation policy by what an error costs, not by the calibration curve alone.
- If you recalibrate, fit on a separate split and record the split.

[^ch3-1]: TypeSafe AI, "Confidence," documentation, <https://docs.typesafe.ai/confidence.md>. It states that Noul answers "don't carry one" and that confidence "is derived from the probabilities."

[^ch3-2]: Nhu Hoang, "Jev vs. LLMs: When AI Moves from Generation to Decision-Making," Towards Data Science, September 25, 2026, <https://towardsdatascience.com/jev-vs-llms-when-ai-moves-from-generation-to-decision-making/>. Reported: the anger call (section 5, page 10); the forecaster analogy (section 6, page 11); isotonic regression working from returned probabilities and temperature scaling needing raw scores (page 12); rounding to two decimal places (page 15). Supplied copy.

[^ch3-3]: Laya project (GitHub: NandhaKishorM/laya), repository README, <https://github.com/NandhaKishorM/laya>. In its section on differences from Jev, the README says Laya's confidence "is 1 minus normalised entropy … not Jev's `(n*p_max - 1)/(n - 1)`. A threshold carried over from Jev does not transfer." (The README writes the middle dot and minus signs as typographic characters; I have used plain ASCII in the code span.) The TypeSafe confidence page cited above gives "(3 x largest probability - 1) / 2" as an approximation for three options.

[^ch3-4]: TypeSafe AI, "AI primer," documentation, <https://docs.typesafe.ai/introduction/machine-learning-primer.md>.

[^ch3-5]: TypeSafe AI, "AI primer," as cited above. The sycophancy and mode-dropping argument, and the statement that an output "can be compelling to a person without being reliable enough for unattended automation," are from this page.

[^ch3-6]: Long Ouyang et al., "Training language models to follow instructions with human feedback," 2022, <https://arxiv.org/abs/2203.02155>.

[^ch3-7]: DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning," 2025, <https://arxiv.org/abs/2501.12948>. The TypeSafe primer cited above describes RLVR as having "created reasoning models that are strong at tasks such as mathematics, but slower and more expensive."

[^ch3-8]: Chuan Guo, Geoff Pleiss, Yu Sun and Kilian Q. Weinberger, "On Calibration of Modern Neural Networks," *Proceedings of the 34th International Conference on Machine Learning*, 2017, <https://proceedings.mlr.press/v70/guo17a.html>.

[^ch3-3b]: Laya README, as cited above.

[^ch3-2b]: Hoang, "Jev vs. LLMs," section 6 (supplied copy, page 11).

[^ch3-5b]: TypeSafe AI, "AI primer," as cited above.

[^ch3-2c]: Hoang, "Jev vs. LLMs," section 6 (page 12).

[^ch3-2d]: Hoang, "Jev vs. LLMs," section 6 (page 15).

[^ch3-2e]: Hoang, "Jev vs. LLMs," section 6 (page 12).
