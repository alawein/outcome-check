# Offline tau-bench airline pilot

The source has 200 public recorded trajectories, including 84 with upstream
reward 1.0. The study rechecks only explicit supplied final reservation fields.
It does not run agents, tools, the environment, or a model.

Source: [Sierra's recorded GPT-4o airline trajectories](https://github.com/sierra-research/tau-bench/blob/59a200c6d575d595120f1cb70fea53cef0632f6b/historical_trajectories/gpt-4o-airline.json),
commit `59a200c6d575d595120f1cb70fea53cef0632f6b`, MIT repository, downloaded
October 8, 2026. The archive's complete end-of-run database and expected goal
snapshots are absent; a goal-state hash cannot recover them. Third-party
messages and data are excluded from Git. Committed results contain task IDs,
counts, and classifications, not transcripts or reservation records.

```powershell
New-Item -ItemType Directory studies/data -Force
curl.exe -L --fail https://raw.githubusercontent.com/sierra-research/tau-bench/59a200c6d575d595120f1cb70fea53cef0632f6b/historical_trajectories/gpt-4o-airline.json -o studies/data/gpt-4o-airline.json
Get-FileHash studies/data/gpt-4o-airline.json -Algorithm SHA256
uv run python studies/tau-airline/run.py studies/data/gpt-4o-airline.json --output studies/tau-airline/results.json
```

SHA-256: `e9e6c0297660c537f83d4fd9c476ce7a9a86ecd2784874b7bfc13be598e37bfa`.
The script refuses different bytes and reproduces its classifications twice.

## Mapping and actual results

For each annotated reservation mutation, named target fields in its supplied
kwargs become requirements. Cancellation maps to `status=cancelled`, as specified
by the upstream [cancellation tool](https://github.com/sierra-research/tau-bench/blob/59a200c6d575d595120f1cb70fea53cef0632f6b/tau_bench/envs/airline/tools/cancel_reservation.py).
Flights are projected to `flight_number` and `date`, excluding price and derived
route data. Control arguments such as payment ID are dropped rather than treated
as final state. Later annotated mutations override earlier expected fields for
the same reservation. The last explicit JSON tool response for that reservation
supplies the observed fields. A hash, reward, tool-call argument, or assistant
claim never supplies an observation. Missing goal/state remains unobserved.

Of the 84 reported successes, the **reservation-field projections** are:
13 confirmed, 9 contradicted, and 62 unobserved. These classify the declared
projection, not the full task. They do not establish nine incorrect benchmark
scores: projection omissions and domain-specific reward rules remain outside
this comparison. See [results.json](results.json) for every task ID and zero-based source index;
task IDs repeat across trials, so the index identifies each archived trajectory.

For **full database and full goal verification**, all 84 are unobserved because
the archive does not supply those snapshots. No full success is confirmed.

The separate no-change sensitivity check requires distinct first and last
snapshots of the same reservation and a pre-mutation lookup. It flags zero of
these 84 successes. A single lookup cannot serve as both baseline and final
observation. Missing baseline coverage is not proof that an agent changed state.
Legitimate refusal tasks can require unchanged state; this diagnostic is not a
general requirement that every task must cause a mutation.

Study timestamps are fixed encodings of observed log order, not evidence of
wall-clock collection freshness. Freshness itself is tested separately.

## Full-state follow-up protocol

The requested full-state recheck could not be performed on this archive. To run
it, obtain a legally reusable release that includes all four explicit inputs:
pre-action database, post-action database, expected goal database, and reported
reward with task/trial IDs. Record the source version, license, checksum, and
observation collector. Do not reconstruct state by executing historical tools.

Create typed equality requirements for the benchmark's documented comparison
projection. Supply each complete final state as an observation and its earlier
state as a baseline. Set `requires_change` only for task goals that require a
mutation. Count confirmed, contradicted, unobserved, and unconfirmed separately;
cross-tabulate against reported successes and document exclusions. Never infer
truth from a matching hash, a signature, or the upstream success bit.
