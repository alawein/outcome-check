# Changelog

## 0.2.0

- Structured HTML viewer: per-requirement table with action receipt, outcome, status,
  reason, expected path/value, observed value, and observed age versus max age.
- How-to-read legend separating action receipts from outcomes and confirmed, unobserved,
  and contradicted meanings. Comparison math, core reasons, and report.json bytes unchanged.
- Row-index context in contract validation messages; CLI --help with packet shape, example
  command, exit codes, and doc pointers. HTML evidence is escaped and large states truncate
  with an explicit marker.

## 0.1.2

- Regenerate committed example report hashes from the canonical LF input files.
- Add a regression comparing the full committed JSON snapshot with actual CLI output.
- Runtime behavior and original immutable v0.1.0 release are unchanged.

## 0.1.1 (tag only, no release)

- A release command continued after a blocked PR merge and created this immutable
  tag on the unchanged v0.1.0 commit. No v0.1.1 package was published.
- Use v0.1.2 for the corrected example snapshot. The tag is retained unchanged.

## 0.1.0

- Read-only explicit action/outcome checks over supplied evidence.
- Exact fractional freshness, typed JSON equality and safe reports.
- Synthetic examples, independently specified tests and GitHub-only distribution.
