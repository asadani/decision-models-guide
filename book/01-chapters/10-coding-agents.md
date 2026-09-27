# Chapter 10. Extending the Pattern to Coding Agents

One of the supplied documents opens with a question meant to be uncomfortable: how would you design a coding agent if language models had no KV cache?[^ch10-1]

The cache is why agents are built as append-only transcripts. Reusing a cached prefix is cheap. Changing anything early in the context invalidates it and forces the model to reprocess everything after. That single economic fact, the document argues, shapes most of what current agents do, usually without anyone saying so. Imagine it away and ideas that feel obviously right, such as sending easy work to a cheap model, start to look wrong.

Before going further, a note on what this document is. It calls itself an independent synthesis, "not affiliated with or endorsed by TypeSafe," compiled in September 2026 from design notes it attributes to TypeSafe's founder, "as provided to the compiler."[^ch10-1b] I could not verify that attribution, and the compiler is not named. Everything in it is a proposal. Nothing in this chapter is a Jev feature, and I have not seen any of it working.

## Where Jev would sit

In the proposal Jev is not the model that writes code. It is a decision layer beside it. The harness hands Jev the current state, the goal, the context, the rules and the previous actions, together with a predefined question, and gets back a typed answer with a probability. Frontier models, sub-agents, tools and deterministic code do the work. The document's list of questions is a fair summary of the whole idea:

| Decision point | Question to the decision model | Typed answer |
|---|---|---|
| Context | How visible should this chunk be for this query? | hide, short, long or full |
| Cache | Reuse the cached prefix, or rebuild? | yes-or-no probability |
| Routing | Can this subtask leave the frontier model? | choice, plus a cost estimate |
| Tools | Which tool fits this intent? | ranked choice |
| Permissions | Should this command run? | allow, ask or deny |
| Security | Which files will this task touch? | sensitivity score |

*From the supplied document. Every row is a proposal.*

Asked thousands of times per session, the document says, those small decisions are where the leverage is.

![A proposed decision loop for a coding agent. Code assembles a bounded context from repository facts, a decision component judges relevance and routing, a generator proposes an action, and deterministic validation and permissions gate anything that executes.](../../assets/diagrams/generated/fig4-agent-loop.png){alt="Flow diagram. Versioned task state and repository facts feed retrieval of candidate context. Relevance and task-routing judgments follow. Code assembles a bounded context. A generator proposes a patch or tool action. Permissions and deterministic validation gate it before tool execution. The result returns to task state, and read-only evaluation and review read from the state."}

## The routing arithmetic

The most concrete part of the document is a cost model. Let *X* be the tokens of context, *Y* the tokens the model generates, and *Z* the additional tokens it reads while working, such as command output and file reads. Using the list prices the notes cite, $5 input and $25 output per million tokens for Opus and $3 and $15 for Sonnet, the document compares two paths.

| Path | Cost |
|---|---|
| Stay on the frontier model throughout | 25*Y* + 5*Z* |
| Frontier plans, cheaper model executes, frontier reviews | 3*X* + 20*Y* + 8*Z* |

The second path pays the cheaper model to load the context (3*X*), generate (15*Y*) and read (3*Z*), then pays the frontier model to reload whatever changed (5*Y* + 5*Z*). For a plausible session, *X* = 0.65, *Y* = 0.12 and *Z* = 0.23, the totals are 4.15 for the frontier path and 6.19 for the routed one. Staying on the frontier costs about two thirds as much as the route meant to save money.[^ch10-1c]

The document's own numbers check out. The difference between the paths is $3X - 5Y + 3Z$, which is 2.04 here; that simplification is mine. Routing is cheaper only when $3(X + Z)$ is less than $5Y$: a short context, little reading, and a lot of output. The units are normalized tokens under stated prices, not invoices. Cache pricing, summary size, routing overhead, quality differences and repeated handoffs can each change the answer, and the prices are the notes' own and may have changed.

The lesson the document draws is that routing priced per token, rather than per context rebuild, is wrong. Routing pays off only when the harness can hand the cheaper model a small, purpose-built context and does not force the frontier model to reread everything the helper produced.

## Where the tokens go

The document also gives a table of how a typical session's processed tokens divide: reading file contents roughly 30 to 40 percent, searching the codebase 10 to 18, command output 10 to 20, fixed overhead such as the system prompt and tool schemas 5 to 12, reasoning and planning 5 to 15, and writing and editing code only 4 to 10. It labels these midpoint estimates and "an illustrative estimate," not telemetry.[^ch10-1d] It cites a separate figure from Microsoft's fastcontext project, which I did not verify: that in GPT-5.4 trajectories, reading and searching account for 56.2 percent of tool-use turns and 46.5 percent of the main agent's tokens.

If those numbers generalize, the largest saving in a coding agent is not a better model or diff format. It is smarter retrieval, and that is where a cheap decision component could earn its keep. That is a hypothesis, and one to test on your own sessions.

## Three cautions

The proposal has a good idea at its center: context is not static, it can be assembled per query instead of accumulated. Three cautions apply before you build on it.

**Relevance filtering is lossy.** The proposal scores each chunk of context for relevance to the current question. Binding instructions and unresolved user constraints must stay outside that discretionary pruning, or the harness will silently discard the rules it was meant to follow.

**A learned permission score is not authorization.** The document suggests programmable permissions and routing by data sensitivity, with secrets restricted to first-party frontier models and public documentation open to any model. Good. But a model's prediction that a file is harmless cannot itself authorize disclosure, and a low price or open weights does not establish a provider's privacy practices. Hard enforcement belongs in deterministic policy, as in Chapter 8, with the model advising inside it.

**Choosing a tool is not choosing its arguments.** The document proposes that typed calls select a tool and construct its arguments. Selection is a natural fit for a decision model. Building arbitrary valid arguments is extraction or generation, which still needs validation.

## The pattern in a drone

A launch-week example from the supplied guide shows the shape of a well-bounded design. A simulated quadrotor flies a five-station obstacle course using only its onboard camera, in layers. A geometric flight controller runs at 500 Hz and guidance with a safety reflex at 50 Hz, both ordinary code, and code always owns safety. Classical computer vision turns the camera image into a symbolic scene at 15 Hz. Jev sits at the top, at about 2.5 Hz, for tactical judgment: it answers three questions in one call, a Choice over maneuvers, a Score for risk, and a Noul on whether the target is lost or briefly occluded, and it is advisory only. As the project's README puts it, Jev "cannot be the perception layer, and it cannot run at control rate."[^ch10-2] The guide's summary of its examples is the one to keep: keep the loop, the safety and the arithmetic in ordinary code, and use Jev for the narrow judgment in the middle that code finds hard to phrase.

The same pattern appeared in the Doom story of Chapter 7. State representation, question design and deterministic rules did most of the work.

## In practice

- Price routing by context rebuild, not per token. Use your own session numbers for *X*, *Y* and *Z*.
- Measure where your agent's tokens go before you optimize anything.
- Keep binding instructions and open constraints out of relevance pruning.
- Let a decision model advise permissions and routing inside a deterministic policy. Never let it replace one.
- Validate everything a tool call is built from. A correct choice of tool does not make its arguments correct.

[^ch10-1]: "Jev Engineering for Coding Agents: The TypeSafe Founder's Blueprint for Building with Jev," an independently compiled working note, September 2026 (supplied PDF; no author named and no web address). Its final page states that it is an independent synthesis for study, that its diagrams are original to it, that its cost figures are "illustrative and based on list prices cited in the source notes," and that the token-share table is "an illustrative estimate." The routing arithmetic is on page 4, the token table on page 5, and the fastcontext figures on pages 5 and 6. I checked the arithmetic and the chart values in Figure 2 of the document against my own calculation.

[^ch10-2]: unicodeveloper, "The Ultimate Guide to Jev: The new Frontier AI for faster decisions," Medium, September 17, 2026 (supplied copy, pages 16 and 18; the original web address was not preserved). The drone table is on page 16; I read its rates from the page image. The drone example is described there as a launch-week artifact whose figures are self-reported by the project's author; the quotation is from that project's README as reproduced in the guide.

[^ch10-1b]: Independent compiler, working note (see above), page 12.

[^ch10-1c]: Independent compiler, working note (see above), page 4.

[^ch10-1d]: Independent compiler, working note (see above), pages 5 and 6.
