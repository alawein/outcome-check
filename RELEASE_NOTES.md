# outcome-check v0.4.0 release record

This checkout document records delivery and dated preparation history. The workflow generates
the public GitHub Release body after verified registry publication from the actual
version, source commit, tag and distribution digests; it does not upload this file.

Schema v3 adds explicitly bound RFC 8785 signatures with finite binary64 numbers,
UTF-16 key ordering and unchanged legacy v2 signing bytes. Signed migration requires
authentic re-signing. Core remains offline and dependency-free.

The full-state study protocol accepts supplied snapshots and reports missing-input
coverage separately from benchmark rewards. The pinned public archive lacks all
three complete states; its 84 reported successes remain full-state unobserved.

Release automation retains one canonical build, verifies exact file inventory,
attests those bytes, reconciles registry retries, and uploads identical assets.
Shared output tests cover per-file atomicity and escaping. See CHANGELOG.md for
compatibility and DECISIONS.md for the signed profile and study projection.

## Current release state (October 8, 2026)

Version 0.3.0 is published: [merged PR 16](https://github.com/alawein/outcome-check/pull/16),
[immutable tag](https://github.com/alawein/outcome-check/tree/v0.3.0),
[GitHub Release](https://github.com/alawein/outcome-check/releases/tag/v0.3.0),
[successful publish run](https://github.com/alawein/outcome-check/actions/runs/37799710726),
and [PyPI](https://pypi.org/project/outcome-check/0.3.0/).
The source commit is `66fea09ab87352224d3e01b65709392c3259e0ca`.
Do not retry that successful publication or replace its tag/assets.

Version 0.4.0 is now public on [PyPI](https://pypi.org/project/outcome-check/0.4.0/)
from immutable source `6f026e2f59059c34dd53b496eb4ff973712d380d`.
Its retained distribution bytes and publisher/build provenance were verified.
The initial post-upload registry check observed an incomplete listing. Recovery
[run 37824835131](https://github.com/alawein/outcome-check/actions/runs/37824835131)
succeeded without reuploading verified files and created the public
[GitHub Release](https://github.com/alawein/outcome-check/releases/tag/v0.4.0).
Exact hashes and recovery evidence are in [release readiness](RELEASE_READY.md).
The entire Dependabot family remains excluded from this closeout.

## Dated v0.3.0 prepublication record

The following records the earlier preparation run, before the publication above.

Release candidate. Publication is gated.

0.3.0

- Opt-in version 2 checks: numeric ranges, typed array contains, bounded fixed-width
  regex and explicit baseline comparisons. Unchanged satisfied targets requiring a
  change return unconfirmed. Original version 1 packets/reports stay compatible.
- Optional Ed25519 signatures verified against local public keys, with unsigned and
  unverified labels, required signature enforcement and restricted canonical JSON.
  Signatures authenticate supplied bytes only; core remains dependency-free.
- Per-file atomic report output with hard-link alias and competing-creation guards.
- Versioned Draft 2020-12 schemas, negative/compatibility tests, Hypothesis freshness
  properties, local runtime boundary proof and source type checks.
- Python support floor lowered to 3.11 after local compatibility verification.

See [AUDIT_VERIFICATION.md](AUDIT_VERIFICATION.md) for executed checks and limitations,
and [RELEASE_READY.md](RELEASE_READY.md) for gated publication commands.
