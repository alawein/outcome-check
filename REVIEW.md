# Review scope

Review the exact PR head and changed lines. Report concrete regressions or security
issues with file/line evidence and a reproducible trigger. Prefer a short findings-
first summary; say when no actionable defect was found. Do not invent executed
tests, speculate about adoption, or repeat settled design choices as defects.

Preserve these invariants:

- v1/v2 behavior and exact legacy signature bytes remain compatible.
- v3 RFC 8785 binds canonicalization, algorithm and key ID; invalid Unicode,
  nonfinite values, unsupported profiles and lossy integers fail closed.
- Signed migration requires authentic re-signing; signatures prove bytes, not truth.
- Baselines are explicit, subject-bound and strictly earlier than final evidence.
  Required changes apply to the addressed value; legitimate unchanged goals remain valid.
- Supplied timestamps control freshness. Missing state is never reconstructed from
  tools, hashes, rewards, model judgments or an agent's self-report.
- Runtime is offline with no subprocess/model/network calls and zero default
  dependencies. Cryptography remains an optional extra.
- Input aliases and hard links are protected. Exports are atomic per file, not
  a multi-file transaction. Escape imported HTML text and reject nonfinite JSON.
- One canonical release build supplies attested, retained, verified publication
  bytes. Never replace an existing tag or mismatching registry/GitHub asset.
- Leave Dependabot-family configuration unchanged.

This file applies to hosted reviewers that load it from their supported base
revision. Its presence does not establish that a hosted review actually ran.
