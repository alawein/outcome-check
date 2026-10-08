# Functional evidence

The v0.2.0 source baseline has 49 passing local pytest cases. PR 4's stated 45
was stale: PR head 9c96f81 and squash 939b9a5 have identical tests, and an isolated
run of the PR head yields 49, matching the release notes. See
[related work and historical checks](related-work.md). The independently
specified twelve-case matrix covers clean, wrong-state, failed/missing/unknown/null
action, missing/stale/future/wrong-subject observation, missing path and Boolean
versus number. Other tests cover explicit retries, row ordering, recursive equality,
duplicate IDs/keys, unknown fields, timezones, limits, nesting, UTF-8/BOM, nonfinite
numbers, hard-link output preservation, escaping and the 10,000-entry boundary.

No remaining mismatch against the declared matrix. These tests validate decisions
over supplied evidence, not authentic execution or collector accuracy. Isolated
artifact and hosted results are reported in release notes after actual execution.

Fresh review found invalid offset normalization and submicrosecond truncation.
Regressions failed first, then passed with offset range checks and exact rational
fractional-second freshness. No remaining precision mismatch in those cases.

Version 0.3.0 adds meaningful negative and boundary cases for rich checks, explicit
baselines, the unchanged required-change regression, local signature verification,
canonicalization limits, per-file atomic output failure and creation races, version 1
snapshot compatibility, and a guarded complete CLI run. The guard denies socket,
subprocess and os.system calls and disallows writes outside declared exports and
their same-directory staging files. It also checks signed and unsigned version 2
runs. It verifies this path over fixtures, not all possible custom verifier code.

Hypothesis checks exact fractional freshness, timezone-equivalent instants,
inclusive max-age boundaries and submicrosecond future/stale comparisons. Schema
validation checks every committed contract example and each versioned schema.
Runtime validation remains authoritative for cross-record and complexity limits.

The public study's scoped data, transform, counts and limitations live in
[studies/tau-airline/README.md](../studies/tau-airline/README.md). Existing synthetic examples remain
AI-assisted, non-client CC0 data. Public traces have their own upstream license and
are not relabeled synthetic or CC0.

Local product verification: 114 tests pass on Python 3.11.13, 3.12.10 and 3.13.9.
Ruff lint/format, mypy (including untyped function bodies), all 12 schemas and all
six committed JSON examples pass. The frozen lock has 69 entries (development,
build and optional dependencies); the default wheel has zero runtime dependencies.
