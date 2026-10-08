# v0.3.0 implementation decisions

Scope: local autonomous hardening on feat/v0.3.0-hardening. Root alone publishes a draft PR; no merge, main push, tags, releases, settings, secrets or Pages changes.

- Preserve schema_version 1 packets and report bytes. Version 2 adds baselines, optional checks, signatures and the unconfirmed status. Unconfirmed is review-needed exit 1, not a success.
- Equality defaults to recursive typed JSON equality; integers and floats are numerically equivalent, booleans differ from numbers. Range only compares finite numbers; contains checks array members using the same equality.
- Regex accepts anchored fixed-width patterns only, with a small whitelist and bounds. Reject ambiguous or unbounded complexity rather than claiming timeout guarantees.
- Baselines are explicit IDs in a separate array. Their timestamp must strictly precede the chosen final observation. The tool does not establish when an action actually ran; the caller owns that provenance.
- requires_change checks the addressed value, not unrelated state. A satisfied unchanged state returns unconfirmed / no observed change. Missing or incompatible baseline evidence returns unobserved.
- Optional local signature verification establishes the supplied bytes and named key, not the truth of state. Core remains dependency-free; Ed25519 support is an optional cryptography extra. Canonicalization supports an explicitly restricted RFC 8785 subset, with floats rejected for signing.
- Outputs use same-directory temporary files and per-file atomic replacement. Nonforce publication uses a hard link so a competing creation is never overwritten. Multiple outputs are not a transaction; filesystem failures can leave an earlier completed output.
- Lower the supported Python floor to 3.11 only after running its suite. Property tests, schema validation and type checks are dev dependencies.

- Existing release automation remains tag-only and uses OIDC with artifact attestations.
  Pages workflow is manual-only so merging the draft cannot deploy. No publication
  is authorized in this task. Hosted settings verification is root-owned.

## Release coordination decisions

Hosted link checks returned 404 only for the repository's maintainer-only security
settings URL. Keep its exact click path, exclude only that anchored URL from
anonymous lychee probes, and continue checking all public research/document links.
Read-only API checks separately established the disabled alerts/update settings.
No setting or credential was changed to make the check pass.

Pages deployment is manual-only so approving a merge does not also approve
hosting. A release tag starts trusted package publication, so the tag requires
both tag and registry publication authorization. npm first-publication bootstrap,
if needed, is a separate owner-approved publication using existing access; this
run does not create secrets or bypass registry setup.
