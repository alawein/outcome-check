# Related work and evidence scope

[tau-bench](https://arxiv.org/abs/2406.12045v1) (June 17, 2024) evaluates agent
trajectories by comparing resulting database state to an annotated goal state.
Outcome Check adopts the general supplied-state comparison pattern, with explicit
action/outcome separation and freshness checks; it does not claim that pattern is
new or reimplement tau-bench's original reward function.

[Zhu et al., Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/html/2507.02825v5)
(August 7, 2025, Kang is the last author) describes intentionally impossible tasks,
such as changing a non-refundable ticket, for which unchanged state may earn a
success despite a trivial empty-response agent. This motivates explicit baseline
and requires_change checks. It does not establish that every task needs a state
change: a refusal with correct reasoning or an intentionally unchanged state can
be the right behavior. Our synthetic regression shows only that a caller-designated
required change cannot confirm from unchanged supplied state.

The public trajectory study is a bounded recheck of tool-observed reservation
projections from a historical official trace set. A final tool response is supplied
evidence at that point, not a full final database snapshot. Missing matching state
is unobserved; action arguments and original benchmark rewards do not fill that gap.
The adapter does not collect live state, execute an agent, authenticate a benchmark
trace or prove the corresponding real-world task occurred. See the study's source
commit, exact transformation and limitations in studies/tau-airline/README.md.

[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) specifies canonical JSON,
including UTF-16 property sorting and ECMAScript-compatible number serialization.
The signature module intentionally supports a restricted safe-integer subset;
it rejects floats and cannot claim full RFC 8785 number interoperability.

Historical repository checks: [PR 1](https://github.com/alawein/outcome-check/pull/1/checks)
had 15 successful Actions checks and a pending CodeRabbit status. The aggregate
15/16 display is not evidence of a failed test. [PR 4](https://github.com/alawein/outcome-check/pull/4)
reported 45 tests, but its head 9c96f81 and squash 939b9a5 have identical tests and
an isolated run of that head yields 49. [v0.2.0 release](https://github.com/alawein/outcome-check/releases/tag/v0.2.0)
reported 49. The 45 was a stale author report, not four later post-PR additions.
