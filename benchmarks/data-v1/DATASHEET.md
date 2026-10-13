# Datasheet

## Motivation

Test whether a deterministic verifier distinguishes supplied correct state,
contradictions, ineligible observations, and satisfied goals with no required
change. This is a diagnostic software test set, not a population benchmark.

## Composition

Pinned public tau-bench GPT-4o airline archive: 200 trajectories. Select the last
JSON tool response containing a reservation ID and no error in each eligible
trajectory: 173 anchors, 27 excluded for no such snapshot. Six controlled variants
produce 1,038 packets. Original transcripts are not committed or included in the
archive. Selected reservation states are source derivatives, not real client data
collected by this project; the upstream benchmark is simulated.

## Collection and labeling

Fetched October 13, 2026 from the pinned upstream source URL in provenance.json.
SHA-256 must match before parsing. The selected state is its own declared goal
for a synthetic clean condition. The baseline is deliberately different except
for the no-op intervention. Fixed clocks encode the intervention, not original
collection freshness. Success receipts in every case are synthetic.

The gold labels follow explicit interventions: clean confirms, no-op is
unconfirmed, stale/wrong-subject/timezone-skew are unobserved, wrong-state
contradicts. No humans or models supplied labels. No native full-task labels are
asserted. Examples therefore combine real public state content and synthetic
fault construction; they are not an independently annotated external gold set.

## Processing and splits

Task IDs, including repeated trials, are SHA-256 grouped into dev (hash mod 5=0)
and test (all others). Source indices identify each recorded trajectory. Answer
keys live separately from case JSON. Both splits are public diagnostic material,
not sealed held-out scientific evaluation. A developer can see their labels.

## Uses

Recommended: regression tests for freshness, subjects, no-op checks and typed
comparison, with per-state precision/recall and exact denominators. Unsuitable:
claiming full-task success, comparing agent competence, authenticating state,
training a semantic judge, or inferring a general-world precision of 100%.

## Distribution

Code and source repository are MIT; the source copyright/license notice is
retained in SOURCE_LICENSE.txt. Original source bytes are fetched, checksum-bound,
and ignored locally. Generated local ZIP includes derived packets, separate
keys, checksums, schemas, datasheet/card/provenance and metadata. No Hugging Face
upload or GitHub release asset publication occurs automatically.

## Maintenance and risks

Version 1 is frozen to its source checksum and deterministic interventions.
Change source or intervention semantics only under a new dataset version.
Source task goals, complete databases, real collection timestamps, and causal
provenance are missing. Correlated variants preclude simple independent-sample
confidence intervals. No new agent trajectories, human study, or LLM baseline
were run. Native tau reward replay requires absent full databases and executes
tools, outside this read-only diagnostic. Compare a naive equality baseline on
the same actual packets, and retain the prior public projection study separately.
