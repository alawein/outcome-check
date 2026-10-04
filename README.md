# Outcome check

An action can succeed while its requested outcome is wrong. Compare each explicit
requirement with supplied state evidence. Outcome check keeps the action receipt,
observed outcome and overall decision separate: confirmed, contradicted or unobserved.

## Run

Python3.13+, no runtime dependencies. Install the wheel from this repository's
Releases using `python -m pip install path/to/outcome_check-0.1.0-py3-none-any.whl`.
Or from a clone:

```sh
uv sync --frozen
uv run outcome-check examples/packet.json --html report.html
```

The synthetic alarm example exits1: enabled is confirmed, requested time07:00
is contradicted by observed07:30 despite a succeeded action, and volume is
unobserved because its receipt is stale. Exit0 all confirmed; exit2 invalid/I/O.

## Capabilities and limits

Explicit observation IDs prevent accidental retry or row-order matching. Supplied
as_of fixes the comparison time. Object-key paths use recursive typed JSON equality;
Boolean true differs from number1. Missing/wrong-subject/future/stale evidence
remains unobserved. A required failed action is contradicted even with correct state.

This read-only tool authenticates nothing, collects no external state and executes
no agent actions, code, shell or network. Hashes bind bytes, not truth. It cannot
prove a real-world task was completed from a self-reported packet.

[Contract](docs/contract.md), [functional evidence](docs/evaluation.md),
[usefulness](docs/usefulness.md), [provenance](docs/provenance.md).

`just check`: lint, tests, wheel/sdist. `uv run python scripts/build_demo.py`:
static executed Pages report. JSON stdout by default; --json PATH and --html PATH
export files, --force permits overwrite. Input aliases/hard links are rejected.
Writes are not a multi-file transaction; a write failure may leave partial output.

MIT code, original CC0 synthetic AI-assisted non-client examples. Independent
project; no production ownership, client delivery or adoption claim.
