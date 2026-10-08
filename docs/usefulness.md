# Bounded usefulness exercise

Actor: Codex, AI-assisted, original synthetic non-client alarm packet. No external
users, client result, measured time saving, adoption or independent labeler.

Baseline: read three requirements and two observations. Direct state assertions
confirm enabled=true and fail time 07:00 against 07:30. A separate freshness check
is needed before using old volume 5; its age 900 exceeds 120 seconds. A plain equality
assertion would pass that stale value. Both referenced actions report succeeded.

Actual core/CLI reports one confirmed, one contradicted, one unobserved, exit 1.
Time retains action confirmed alongside outcome contradicted. Volume is unobserved
with stale observation reason and action not_required. Input hash and actual output
are in examples/report.json. No false alarm against these declared expectations;
no general error-rate or authenticity claim. Expectations preceded implementation.

Preparation requires explicit paths, references, timestamps and trusted collection
outside this tool. Small pytest assertions are easier for one simple trusted snapshot;
the packet adds portable explanations and distinguishes missing evidence. Existing
[tau-bench](https://github.com/sierra-research/tau-bench) evaluates final-state outcomes
in a controlled environment, a methodological baseline rather than demand evidence.

The workflow is usable. Broad demand, comparative speed, real-world completion,
production suitability and superiority remain unproven.


Version 0.3.0 also includes a [bounded public trajectory recheck](../studies/tau-airline/README.md).
Its classifications apply to supplied reservation-field projections. The archive
lacks full final/goal snapshots, so the study cannot confirm full tasks or establish
incorrect original rewards. Baseline sensitivity is limited by observed coverage.
This expands inspectable evidence beyond synthetic fixtures without an adoption,
production, general error-rate or benchmark superiority claim.
