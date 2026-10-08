# Outcome Check

Check whether supplied evidence confirms an agent's requested outcome.

![Agent evaluation](assets/label-purpose.svg)
![Python](assets/label-stack.svg)
![Offline CLI](assets/label-runtime.svg)

An action can succeed while its outcome is wrong. Outcome Check compares explicit
requirements with supplied observations and reports each as confirmed,
contradicted, unobserved, or (for required changes) unconfirmed. Action receipts stay separate from outcome evidence.

## Run

Python 3.11+, no core runtime dependencies. [Version 0.4.0 is published](https://pypi.org/project/outcome-check/0.4.0/).
Run the repository examples from a clone:

```sh
uv sync --frozen
uv run outcome-check examples/packet.json --html report.html
```

Minimal authoring path: copy `examples/packet.json`, keep one requirement with its
subject, single-key path, expected value, observation reference, small max age, and
action reference (or null when no action applies), then add the matching observation
with the same subject, a fresh `observed_at`, and a state object holding the path key.
Run the command above and read the HTML results table before the JSON blob.

The synthetic alarm example exits 1: enabled is confirmed, requested time 07:00
is contradicted by observed 07:30 despite a succeeded action, and volume is
unobserved because its receipt is stale. Exit 0 all confirmed; exit 2 invalid/I/O.

## Related work and how this differs

[tau-bench](https://arxiv.org/abs/2406.12045v1) compares final database state with
an annotated goal. Outcome Check is a generic offline supplied-data checker: it
keeps action receipts separate, names evidence explicitly and checks freshness.
It neither executes that benchmark nor substitutes a model judgment for evidence.
[Zhu et al.](https://arxiv.org/html/2507.02825v5) found that empty-response agents
can exploit some impossible tasks' unchanged-state success rules; explicit baselines
and requires_change address that specified condition. A correct refusal can still
legitimately require no state change. See [related work](docs/related-work.md) and
the [scoped public trajectory study](studies/tau-airline/README.md).

## Capabilities and limits

Explicit observation IDs prevent accidental retry or row-order matching. Supplied
as_of fixes the comparison time. Object-key paths use recursive typed JSON equality;
Boolean true differs from number 1. Missing/wrong-subject/future/stale evidence
remains unobserved. A required failed action is contradicted even with correct state.

Version 2 adds numeric ranges, typed array membership, restricted fixed-width regex,
and explicit baseline comparisons. See [examples/checks-v2.packet.json](examples/checks-v2.packet.json).
Set requires_change=true with a baseline_id when the request needs a change; a
matching state that already held returns unconfirmed with reason "no observed change".
Correct refusals and deliberately unchanged targets can leave requires_change=false.
Version 1 inputs and report bytes remain compatible. Published
[JSON Schemas](schemas) make the versioned shapes inspectable.

Optional Ed25519 verification uses only supplied local public keys:

```sh
uv sync --extra signing
uv run outcome-check examples/signed-v2.packet.json --public-keys examples/public-keys.json
```

The synthetic public-keys.json fixture maps key IDs to base64 raw public keys. Set packet require_signatures=true
to require verified signatures on selected observations and baselines. The
[contract](docs/contract.md) specifies the legacy restricted profile and the new v3 RFC 8785 profile.

Troubleshooting: validation errors name the array row (for example
`requirements row 2`); check that entry's fields before editing the rest of the file.
Rejected inputs keep prior outputs: the CLI exits 2 and leaves an existing output file
untouched. Reruns need `--force` when the output path already exists, and outputs
cannot alias the input path. See [contract](docs/contract.md) for field limits.

This checker collects no external state and executes no agent actions, supplied
code, shell or network. Its only writes are requested local reports. Unsigned
observations authenticate nothing; optional signatures verify bytes against local
public keys. Hashes and signatures bind supplied bytes, not truth. It cannot
prove a real-world task was completed from a self-reported packet.

[Contract](docs/contract.md), [functional evidence](docs/evaluation.md),
[usefulness](docs/usefulness.md), [provenance](docs/provenance.md),
[related work](docs/related-work.md) and [public trajectory study](studies/tau-airline/README.md).

`just check`: lint, tests, type checks, schemas, wheel/sdist. `uv run python scripts/build_demo.py`:
local static synthetic report (does not deploy). JSON stdout by default; --json PATH and --html PATH
export files, --force permits overwrite. Input aliases/hard links are rejected.
Each report is written atomically. Multiple reports are not a transaction; a later
write failure may leave an earlier completed report.

For stack naming and structure, follow the
[shared repository conventions](https://github.com/alawein/.github/blob/main/docs/system/repos.md#stack-conventions)
alongside this project's local instructions and contract.

[Release readiness](RELEASE_READY.md) and [security settings](SECURITY_SETTINGS.md)
record published versions, v0.4.0 delivery evidence, and verified settings separately.

MIT code, original CC0 synthetic AI-assisted non-client examples. Independent
project; no production ownership, client delivery or adoption claim.

Schema version 3 adds explicitly bound RFC 8785 signatures for finite binary64
numbers. Existing v1/v2 checks and v2 signature bytes remain unchanged. Signed
migration requires authentic re-signing; see [migration guidance](docs/contract.md#version-3-signatures-and-migration).
The [full-state protocol](studies/tau-full-state/README.md) reports supplied-state
coverage separately from the retained reservation-field study.
