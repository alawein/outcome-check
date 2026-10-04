# Outcome check

Strict, offline supplied-evidence outcome checker. Read README.md and docs/contract.md
before behavior changes. Python 3.13+, stdlib runtime; uv manages the dev lock.

- Work on a feature branch; preserve unrelated changes.
- Write meaningful contract and negative tests before changing behavior.
- Use `just check` for product lint, tests and build. No workspace audit required.
- Runtime never calls a network, model, subprocess or agent executor.
- Supplied observations are not authenticated; action and outcome stay separate.
- Escape imported text in HTML; reject malformed input without dropping records.
- Preserve input/output identity checks, including existing hard links.
- Examples are synthetic, AI-assisted, non-client, CC0 data. No adoption claim.
- Do not edit the lock manually, expose secrets or spend money.

Owner authorized publication mode (c), October 4, 2026: bootstrap, first-release
feature and release PRs to main, public MIT repo, GitHub Release v0.1.0 and Pages
synthetic outcome report. Push, check, review and merge within that scope. This scoped
permission supersedes the starter's owner-only merge rule. GitHub-only package
distribution and Pages are approved tool-class exceptions. New scope requires
the owner's instructions. Never bypass a hook or weaken protection to merge.
