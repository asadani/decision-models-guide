# Appendix B. Glossary

**Brier score.** The mean, over cases, of the squared difference between each predicted probability and the true outcome, summed over classes. Lower is better. Some libraries normalize it differently.

**Calibration.** How closely reported probabilities match how often answers are right, measured over groups of predictions, never over a single one.

**Cascade.** A workflow in which a first model handles the cases it is confident about and passes the rest to another model, a person, or another step.

**Choice.** A Jev question type that selects one option from up to 255, returning a probability for each.

**Confidence.** A single number derived from the concentration of a probability distribution. It is not the probability of being right, and its definition differs between systems.

**Coverage.** The share of cases a policy handles automatically.

**Decision model.** A component that takes evidence and a defined question and evaluates a permitted list of answers. A functional definition, not a claim about architecture.

**Expected calibration error (ECE).** The average gap between reported confidence and observed accuracy across groups of predictions, weighted by group size. Depends on how you form the groups.

**Isotonic regression.** A calibration method that learns a never-decreasing correction curve from labeled examples. It works from returned probabilities alone.

**Jaggedness.** TypeSafe's word for the documented edge cases where the current model fails or underperforms.

**Noul.** A Jev question type that returns the probability that a yes-or-no statement is true.

**Policy.** The written, versioned rules, owned by the application, that decide what a prediction may cause to happen.

**Receipt.** A record of a decision: what was asked, the evidence, the model and version, the distribution, the threshold and policy applied, and the outcome. A hash of the input is a fingerprint, not a receipt, and not an immutable log.

**RLCD.** Reinforcement learning for calibrated decisions, TypeSafe's name for the training it describes for Jev. Its recipe has not been published.

**RLHF.** Reinforcement learning from human feedback: training a model to produce responses people prefer.

**RLVR.** Reinforcement learning with verifiable rewards: rewarding outputs that can be checked automatically.

**Score.** A Jev question type that rates a state against two to ten ordered levels and returns a probability for each level and their probability-weighted mean.

**Selective accuracy.** The accuracy of the cases a policy handled automatically, reported together with coverage.

**Shadow mode.** Running a system in parallel with real handling, comparing what it would have done, without letting it act.

**State.** The evidence sent to a decision model: a message, a proposed action, a JSON object.

**System One model.** TypeSafe's term for a model that returns typed decisions and probabilities instead of generated text. The name comes from Daniel Kahneman's fast, intuitive System 1 and describes what the model is for, not how it works.

**Temperature scaling.** A calibration method that divides a model's raw scores by one number before they become probabilities. It changes sharpness, not which answer ranks first.
