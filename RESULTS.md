# Results

Measured October 13, 2026 on Windows-11-10.0.26300-SP0,
Python 3.13.9, AMD64 Family 25 Model 117 Stepping 2, AuthenticAMD.
Numbers below are real software runs, not agent competence or human-study scores.

## Controlled trajectory faults

200 source trajectories; 173 with an explicit reservation
snapshot; 1038 cases across six controlled variants. All fault labels are
programmatic interventions on supplied snapshots, not independent task-success
gold. The selected state becomes the declared goal only for this diagnostic.

| Verdict | Gold cases | Predicted | Precision | Recall |
| --- | --- | --- | --- | --- |
| confirmed | 173 | 173 | 1.0 | 1.0 |
| contradicted | 173 | 173 | 1.0 | 1.0 |
| unconfirmed | 173 | 173 | 1.0 | 1.0 |
| unobserved | 519 | 519 | 1.0 | 1.0 |

Overall diagnostic accuracy: 1.000. Naive typed equality accuracy:
0.333; confirmed precision:
0.200. Its failure to distinguish
no-op, wrong subject, and timestamp ineligibility is deliberate baseline scope.
Every individual fault family has accuracy 1.0 on its173 constructed cases.

Timed checker loop: 2.353882s, 440.97cases/s with tracemalloc enabled;
peak traced Python allocation 167096bytes. This is not resident process memory,
a production SLA, or an instrument-free speed estimate. Reversed input ordering
reproduced identical ID-bound verdicts. Timing is machine/load-sensitive.
Exact environment, splits, metrics and source checksum: [results.json](benchmarks/results.json).

Native tau reward baseline: unavailable because the archive omits full final/goal
databases and its native checker reconstructs goals by executing tools. We did
not replay tools or relabel a naive comparison as native. LLM-as-judge omitted:
no model calls or new judgments. Confidence intervals are not appropriate for
these correlated deterministic variants of a nonrandom source inventory.

## Existing external projection study

The retained prior study of84 native-reported successes has13 confirmed,
9 contradicted,62 unobserved reservation-field projections. These are not
full-task success judgments or proof of nine wrong native scores. All84 full
database/goal comparisons are unobserved because required snapshots are absent.
See [tau study](studies/tau-airline/README.md). No missing state is recovered from
reward bits, signatures, or hashes.

## Software and viewer

Prechange:240 tests at7c49ae4. Current product run:260 tests pass; lint/format,
mypy, pyright,19 versioned schemas/10 examples, wheel/sdist build and actionlint
pass. Fresh-clone candidate-bound results are recorded separately in the audit.
See [PERF.md](PERF.md) for actual three-engine accessibility/cadence/LCP results,
Lighthouse, byte budgets, and unavailable field-INP/hardware claims.

Human participants/labels: none. A future [protocol](benchmarks/data-v1/HUMAN_PROTOCOL.md)
is supplied without fabricated outcomes. Native `.eval` archive support,
independent collection, external full-task gold and population-level precision
remain outside demonstrated coverage. [Requirement coverage](REQUIREMENTS.md)
records these limits alongside implemented deliverables.
