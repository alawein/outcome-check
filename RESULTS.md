# Results

Measured October 13, 2026 on Windows-11-10.0.26300-SP0,
Python 3.11.13, AMD64 Family 25 Model 117 Stepping 2, AuthenticAMD.
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

Timed checker loop: 1.595578 s, 650.55 cases/s with tracemalloc enabled;
peak traced Python allocation 164256 bytes. This is not resident process memory,
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
pass. Fresh-clone source-bound results are recorded below and in the audit.
See [PERF.md](PERF.md) for actual three-engine accessibility/cadence/LCP results,
Lighthouse, byte budgets, and unavailable field-INP/hardware claims.

Human participants/labels: none. A future [protocol](benchmarks/data-v1/HUMAN_PROTOCOL.md)
is supplied without fabricated outcomes. Native `.eval` archive support,
independent collection, external full-task gold and population-level precision
remain outside demonstrated coverage. [Requirement coverage](REQUIREMENTS.md)
records these limits alongside implemented deliverables.

## Fresh-clone verification

A no-hardlink clone started at d5a0817 and fast-forwarded to a2e423e (CI-only
interpreter-selection fix; core source unchanged). Fresh Python 3.11.13,
explicitly selected through UV_PYTHON, passed all 260 tests in 20.50 s, lint/format,
mypy, pyright, 19 schemas/10 examples, and the wheel/sdist build. A separate
Python 3.13.9 clean-clone gate passed 260 tests. An isolated installed-wheel
Python 3.11 environment had no cryptography dependency and rendered all four
states successfully. New benchmark split bytes matched between both interpreters.

Native mlcroissant 1.1.1 parsed two RecordSets and extracted 168 dev/870 test rows
with only an explicit FileObject-to-local-path mapping. Optional newer context
keys produce a warning, not a parse error. The package release date was verified
as October 5, 2026. No hosted dataset upload occurred.

Final browser harness uses fresh navigation through about:blank to exercise saved
preferences. Windows Firefox file reload intermittently timed out even with GPU
disabled; no application assertion is skipped. The unchanged startup/persistence
assertions and all 27 browser observations pass in the final local matrix.
A prior concurrent WebKit p95 of 33 ms correctly failed the unchanged 25 ms cap.
A controlled same-context comparison under reduced host contention measured
blank p95 17 ms and app replay p95 17 ms. These runs do not certify every laptop.
