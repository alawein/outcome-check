# Outcome check

Strict, offline supplied-evidence outcome checker. Read README.md and docs/contract.md
before behavior changes. Python 3.11+, stdlib runtime; uv manages the dev lock.

- Work on a feature branch; preserve unrelated changes.
- Write meaningful contract and negative tests before changing behavior.
- Use `just check` for product lint, tests and build. No workspace audit required.
- Runtime never calls a network, model, subprocess or agent executor.
- Unsigned supplied observations are not authenticated; signatures bind bytes only; action and outcome stay separate.
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

The owner selected chat option (b) on October 8, 2026: complete the reviewed
v0.3.0 release delivery for alawein/claim-review, alawein/eval-audit and
alawein/outcome-check, targeting main. This explicitly authorizes merging the
existing hardening PRs, registry trusted-publisher configuration, v0.3.0 tags,
npm/PyPI publication and GitHub Releases. It is the plain-language equivalent
of profile execution mode (c) for this named scope, not profile mode (b).

Pages deployment, GitHub repository/security/Dependabot settings, operational
secret creation or rotation, branch deletion, force pushes and unrelated remote
changes remain unauthorized. Publishing requires verified existing registry
access; missing authentication blocks registry-dependent actions, not the merge.
Preserve the feature branches. No new repositories or kohyr copies.
