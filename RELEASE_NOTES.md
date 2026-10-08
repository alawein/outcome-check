# outcome-check v0.3.0

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
