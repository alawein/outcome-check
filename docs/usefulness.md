# Bounded usefulness exercise

Actor: Codex, AI-assisted, original synthetic non-client alarm packet. No external
users, client result, measured time saving, adoption or independent labeler.

Baseline: read three requirements and two observations. Direct state assertions
confirm enabled=true and fail time07:00 against07:30. A separate freshness check
is needed before using old volume5; its age900 exceeds120 seconds. A plain equality
assertion would pass that stale value. Both referenced actions report succeeded.

Actual core/CLI reports one confirmed, one contradicted, one unobserved, exit1.
Time retains actionconfirmed alongside outcomecontradicted. Volume is unobserved
with stale observation reason and actionnot_required. Input hash and actual output
are in examples/report.json. No false alarm against these declared expectations;
no general error-rate or authenticity claim. Expectations preceded implementation.

Preparation requires explicit paths, references, timestamps and trusted collection
outside this tool. Small pytest assertions are easier for one simple trusted snapshot;
the packet adds portable explanations and distinguishes missing evidence. Existing
[tau-bench](https://github.com/sierra-research/tau-bench) evaluates final-state outcomes
in a controlled environment, a methodological baseline rather than demand evidence.

The workflow is usable. Broad demand, comparative speed, real-world completion,
production suitability and superiority remain unproven.
