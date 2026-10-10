# Outcome Check

Check whether supplied evidence confirms an agent's requested outcome.

![Agent evaluation](assets/label-purpose.svg)
![Python](assets/label-stack.svg)
![Offline CLI](assets/label-runtime.svg)

An action can succeed while its outcome is wrong. Outcome Check compares explicit
requirements with supplied observations and reports each as confirmed,
contradicted, or unobserved. Action receipts stay separate from outcome evidence.

## Run

Python 3.13+, no runtime dependencies. Install the wheel from this repository's
Releases using `python -m pip install path/to/outcome_check-0.2.0-py3-none-any.whl`.
Or from a clone:

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

## Local Agent Acceptance demo

Build the static reports locally, then open `site/acceptance.html`:

```sh
uv run python scripts/build_demo.py
```

The refund example uses original CC0 synthetic, AI-assisted, non-client data.
It compares four requirements with named supplied observations at a fixed
acceptance time. The report shows expected and observed values, explicit baseline
state, freshness, action receipts, and the resulting verdict beside each other.

| Requirement | Evidence | Verdict |
| --- | --- | --- |
| `refund-confirmed` | Enabled is true in a fresh observation; issue-refund succeeded. | Confirmed |
| `refund-contradicted` | USD 120 expected; USD 100 observed despite a success receipt. | Contradicted |
| `refund-stale` | Completion is true, but the observation is 900 seconds old; max 120. | Unobserved |
| `refund-baseline` | Enabled was already true; the enable-refund receipt is unknown. | Unobserved |

Action receipts alone confirm three requirements; the combined check confirms
one, contradicts one, and leaves two unobserved (exit 1). Baseline state is display
context supplied explicitly by the demo builder. The engine checks state and the
required action receipt; it does not infer that the agent caused a change.

The demo links the exact [packet](examples/acceptance.json),
[source narrative](examples/acceptance-source.txt), and generated JSON report.
Downloads retain the input bytes. The JSON report records the packet SHA-256 and
synthetic provenance; the HTML demo context shows the source narrative SHA-256
separately. Hashes support byte consistency; they authenticate no claims.
The original alarm report remains at `site/index.html` with its existing JSON output.

## Capabilities and limits

Explicit observation IDs prevent accidental retry or row-order matching. Supplied
as_of fixes the comparison time. Object-key paths use recursive typed JSON equality;
Boolean true differs from number 1. Missing/wrong-subject/future/stale evidence
remains unobserved. A required failed action is contradicted even with correct state.

Troubleshooting: validation errors name the array row (for example
`requirements row 2`); check that entry's fields before editing the rest of the file.
Rejected inputs keep prior outputs: the CLI exits 2 and leaves an existing output file
untouched. Reruns need `--force` when the output path already exists, and outputs
cannot alias the input path. See [contract](docs/contract.md) for field limits.

This read-only tool authenticates nothing, collects no external state and executes
no agent actions, code, shell or network. Hashes bind bytes, not truth. It cannot
prove a real-world task was completed from a self-reported packet.

[Contract](docs/contract.md), [functional evidence](docs/evaluation.md),
[usefulness](docs/usefulness.md), [provenance](docs/provenance.md).

`just check`: lint, tests, wheel/sdist. `uv run python scripts/build_demo.py`:
offline static alarm and acceptance reports. JSON stdout by default; --json PATH and --html PATH
export files, --force permits overwrite. Input aliases/hard links are rejected.
Writes are not a multi-file transaction; a write failure may leave partial output.

For stack naming and structure, follow the
[shared repository conventions](https://github.com/alawein/.github/blob/main/docs/system/repos.md#stack-conventions)
alongside this project's local instructions and contract.

MIT code, original CC0 synthetic AI-assisted non-client examples. Independent
project; no production ownership, client delivery or adoption claim.
