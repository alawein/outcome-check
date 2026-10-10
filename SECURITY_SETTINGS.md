# Security controls

The October 8, 2026 closeout authorizes supported security configuration while
excluding the entire Dependabot family: alerts, security updates, version-update
configuration and its PR automation remain unchanged. There is no instruction to
enable those features.

Existing CI runs `pip-audit --local` as a report-only check. It reports known
vulnerabilities in installed development dependencies; it is not a clean-security
certificate. The product has zero default runtime dependencies. Optional signing
uses cryptography. Lock review, full-SHA action pins, protected main, least-privilege
job permissions, OIDC, provenance checks and immutable release hashes provide
separate controls. Root verifies any authorized hosted settings after applying them.

Current root readback confirmed secret scanning and push protection enabled;
Dependabot alerts and security updates remain disabled. No control change was
needed. These are hosted observations, not claims from local preparation.

The read-only prepublication check on October 8 found vulnerability alerts and
automated security fixes disabled. That is a dated observation, not a new request
to change them. The exact maintainer page is
<https://github.com/alawein/outcome-check/settings/security_analysis>.
Its narrow anonymous-link-check exception remains because GitHub returns 404 to
anonymous readers; public citations and release links remain checked.

[Release readiness](RELEASE_READY.md) records the successful v0.3.0 trusted
publication and the new workflow. Never rotate or expose a token to work around
registry authentication.
