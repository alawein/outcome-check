# Release readiness

## Verified v0.3.0 publication

[PR 16](https://github.com/alawein/outcome-check/pull/16) merged on October 8, 2026
at commit `66fea09ab87352224d3e01b65709392c3259e0ca`.
The [immutable tag](https://github.com/alawein/outcome-check/tree/v0.3.0),
[GitHub Release](https://github.com/alawein/outcome-check/releases/tag/v0.3.0),
[PyPI release](https://pypi.org/project/outcome-check/0.3.0/), and
[publish run 37799710726](https://github.com/alawein/outcome-check/actions/runs/37799710726)
are published successfully. Do not retry or replace that version.
Historical preparation evidence remains in [audit verification](AUDIT_VERIFICATION.md).

## v0.4.0 delivery

The owner authorized this closeout, including publication and necessary registry
setup, excluding the entire Dependabot family. v0.4.0 publication has **not yet
been attempted**. No credential or hosted setting is inferred from a local test.
Root coordinates the reviewed PR, merge, new tag, publication and release readback.
Preserve prior feature branches, tags and release assets.

`release.yml` starts only on a new `v*` tag whose commit is the current main tip
and whose version equals pyproject.toml. Build once with the frozen development
lock and Hatchling 1.32.4. Default runtime dependencies remain empty.
The build job checks tests, types, schemas, metadata and a fresh wheel install,
creates an exact two-file inventory, attests those files and retains them in the
`canonical-distributions` Actions artifact before registry authentication.
SHA256SUMS and inventory.json live in release-assets, outside dist.

The publish job downloads and verifies those retained files, reconciles PyPI, and
verifies each existing upload's digest, downloaded bytes and exact publisher
provenance. A matching partial upload resumes only its missing files through OIDC;
extra files, conflicting bytes or missing/foreign provenance fail closed. A fresh
`publish-dist` directory holds copies of only missing files. PyPA's generated
`.publish.attestation` sidecars stay there; retained dist and its inventory are
never modified or loosened. Already verified existing files are never uploaded again.
After publication the complete exact registry inventory is required. Downloaded
registry bytes must match, with build provenance constrained to the
repository, release workflow, source commit, tag and hosted runner. PyPI publish
attestations are cryptographically checked and their certificate claims bind the
repository, workflow, signer/source commit, tag and hosted runner. Only the final GitHub upload job
has contents:write. It uploads the same files and checksums and rejects conflicting
existing assets. Its public release body is generated only after complete registry
byte and publisher-provenance verification, and includes the actual version, source,
tag and digests. It does not copy this checkout's preparation notes. Version-specific
historical notes and existing tags/assets remain unchanged. This is prepared
automation until a new run actually succeeds.

Publication states must remain distinct:

- **Published successfully:** verify destination files and hashes, then stop.
- **Failed with a verified cause:** retain the build artifact and record that cause.
  Repair access/configuration as needed; rerun failed jobs using retained bytes.
  Reconcile the destination first because a timeout may have had an effect.
- **Not attempted:** no successful or failed external publication is claimed.

The existing PyPI trusted publisher uses repository `alawein/outcome-check`,
workflow `release.yml`, environment `pypi`. Owner-entered interactive authentication
is an access requirement when needed, not a renewed authorization request.
Never expose a token or invent an alternative secret flow.

## Pages and security

Pages remains manual-only. The v0.3.0 [deployment run](https://github.com/alawein/outcome-check/actions/runs/37818145477)
succeeded. Root handles the next authorized deployment and actual readback. [Security settings](SECURITY_SETTINGS.md) describe supported controls
and report-only audits. Local checks do not prove those remote controls changed.
