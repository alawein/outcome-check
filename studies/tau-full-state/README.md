# Full-state supplied-snapshot protocol

No inspected public release supplied complete baseline, final and expected goal
states together with trial identity and reward. This directory ships the executable
protocol and an exact missing-input report, not a reconstructed benchmark result.

## Corpus inspection

- The pinned [tau-bench airline archive](https://github.com/sierra-research/tau-bench/blob/59a200c6d575d595120f1cb70fea53cef0632f6b/historical_trajectories/gpt-4o-airline.json)
  is MIT, commit `59a200c6d575d595120f1cb70fea53cef0632f6b`, SHA-256
  `e9e6c0297660c537f83d4fd9c476ce7a9a86ecd2784874b7bfc13be598e37bfa`.
  All 200 rows have task_id, trial, reward, info and traj. Their supplied records
  have no full pre-action, final or goal database. Tool arguments, tool-return
  projections and reward hashes are not substitute full snapshots.
- [tau2-bench evaluation documentation](https://github.com/sierra-research/tau2-bench/blob/4ce7c0397c1eb65c9bbe59aeacfe1ca44a1cd699/docs/evaluation.md)
  and its [simulation model](https://github.com/sierra-research/tau2-bench/blob/4ce7c0397c1eb65c9bbe59aeacfe1ca44a1cd699/src/tau2/data_model/simulation.py)
  were inspected at commit `4ce7c0397c1eb65c9bbe59aeacfe1ca44a1cd699` (MIT).
  Its benchmark derives a goal by replaying reference actions and checks database
  hashes. Those instructions are not supplied goal snapshots and were not executed.
- The [AgentSuite trajectory preview](https://huggingface.co/datasets/AgentSuite/tau-bench-trajectories)
  shows messages, reward details and db_match, not the needed full-state triple.
  No large download or reuse occurred; complete fields and reusable license were
  not established from this preview. This is a bounded search, not proof that no
  suitable public corpus exists anywhere.

`results.json` is generated from the pinned archive already used by the prior
study. Coverage is baseline 0/200, final 0/200, goal 0/200, complete 0/200.
All 200 full-state outcomes are unobserved, including all 84 upstream successes
and 116 nonsuccesses. Zero unconfirmed cases cannot establish absence of no-change
exploits when baselines are missing. The prior [reservation-field projection](../tau-airline/README.md)
remains exactly 13 confirmed, 9 contradicted, 62 unobserved among 84 successes.

```sh
uv run python studies/tau-full-state/run.py studies/data/gpt-4o-airline.json --pinned-tau-archive --output studies/tau-full-state/results.json
```

The command checks the source hash and shape. It never executes tools or calls a
model. Third-party state/messages remain outside committed files; only IDs,
coverage and classifications are retained.

## Executable input protocol

Supply a UTF-8 JSON object with source URL, immutable version, license,
`projection: "entire supplied database"`, and a records array. Every record has
unique task_id/trial_id strings, reported_success Boolean, and optionally:

- baseline: observed_at (RFC3339) and complete state object before the action.
- final: observed_at and complete final state object.
- goal: complete expected state object and mutation_paths, an array of object-key
  paths requiring changes. Use an empty list for legitimate unchanged/refusal goals.

The projection compares the entire supplied database with typed recursive equality.
It is not automatically equivalent to tau-bench's domain-specific hash projection.
A corpus with a different documented comparison rule needs a reviewed explicit
adapter; unsupported projection names fail. Extra, missing or contradictory state
can affect the full comparison. Each named mutation target also needs a changed
value, so unrelated-field changes cannot satisfy it. Baselines must strictly
precede final timestamps. Missing supplied inputs remain unobserved.

```sh
uv run python studies/tau-full-state/run.py supplied-corpus.json --output full-state-results.json
```

The output binds the input bytes by SHA-256, reports baseline/final/goal/complete
coverage, counts all four statuses, and cross-tabulates upstream successes. Fixed
`as_of` equals the supplied final timestamp for this study; it does not establish
real collection freshness. Fixture tests cover unchanged legitimate goals,
required changes, unrelated changes, absent snapshots, temporal conflicts and
contradictory final states. They prove protocol behavior, not public task success
or causal credit for an agent. New corpora need independently documented license,
collector provenance and complete snapshot coverage before stronger conclusions.
