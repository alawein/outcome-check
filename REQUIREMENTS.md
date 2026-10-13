# Requirement coverage

This matrix covers the original outcome-check brief and shared requirements.
Done means implemented and exercised within the stated finite scope. Partial
means a real limitation remains. Gated means no remote effect was performed.
The other two tools' implementation belongs to their own repositories.

| Requirement | Status | Evidence or precise limit |
| --- | --- | --- |
| Current MAIOS policy/style/load order | Done | MAIOS_CONTEXT.md records verified source paths/revision, read-only policy scope, and repository authority. |
| Recent commits/PRs/releases/settings | Partial | docs/repo-history.json and shared-history files inventory accessible branch/PR/release history and current settings; inaccessible/deleted settings history cannot be reconstructed. |
| Verify baseline and prechange counts | Done | AUDIT_VERIFICATION.md: 240 tests at starting SHA; historical findings distinguished from current implementation. |
| Dated primary-source research through cutoff | Done | RESEARCH.md includes September 2026 work, foundational benchmarks, official docs, dates or unknowns, and evaluation methods. |
| Positioning/usefulness | Done | BRAND.md and README define user, supplied-evidence task, and integration boundaries. No demand/adoption claim. |
| Family/product name and collision checks | Done | Siftgrain State, name-checks.json exact GitHub/npm/PyPI/HF queries and limited web search; Spanward rejected. No legal-clearance claim. |
| Original SVG logo/wordmark/palette/type/voice | Done | brand assets and BRAND.md; shared canonical tokens, system/Georgia/monospace fonts. |
| Shared token package | Done | Identical vendored private 1.0.0 package, frozen canonical owner in claim-review; runtime embed equality is enforced. No published package. |
| Four runtime themes and guarded persistence | Done | Cartoon/Calm/Pixel/Lab, dark/light controls; every storage access guarded; denied-storage tests. |
| GPU motion/offline fallbacks | Done | Finite WebGL2 worker sweep on explicit interaction; Chromium handshake verifies actual renderer. Static fallback where unavailable; no CDN. |
| Meaningful verdict motion | Done | Confirmed settles, contradiction shakes, missing evidence uses dashed/ghosted outline; no-op has explicit fourth label. Motion does not alter results. |
| Reduced motion/pause/hidden lifecycle | Done | CSS/WAAPI/GPU guards, explicit active-animation cancellation and offscreen observer; hidden work stopped, pagehide worker terminated, controls and browser runs. |
| WCAG2.2AA/focus/keyboard/labels | Partial | All four themes/both appearances/three engines passed automated WCAG-tag axe with no violations; full manual assistive-technology conformance is not established. Motion text opacity defect was corrected. |
| 60 fps, INP<200 ms, file LCP<2.5s | Partial | Measured active replay rAF cadence, event timing and file LCP in PERF.md; CI enforces explicit budgets. Field INP and midrange-laptop certification are unavailable. |
| Lighthouse CI/axe/gzip budget | Done | npm run perf invokes Lighthouse and npm run lhci uses native collect/assert in CI; npm test invokes axe and three engines; 32,768-byte gzip cap enforced. Lighthouse score/TBT are reported candidly. |
| Real MP4 per vibe | Done | assets/demos: actual Playwright viewer recordings converted with ffmpeg, no fabricated product footage. |
| Explicit deterministic offline stdlib core | Done | Existing core retained; adapters/MCP never collect or execute. Guarded boundary tests. Default runtime dependencies zero. |
| Hashes bind bytes, not truth | Done | README/contracts/UI preserve trust boundary; signatures remain optional. |
| Versioned Draft2020-12 schemas and v0.2.x migrations | Done | Existing v1/v2/v3 schemas and explicit unsigned migration retained; 19 schemas/10 examples validated. Dataset schema adds versioned case shape. |
| Range/contains/anchored bounded regex | Done | Already present and preserved; current audit refs and negative tests. |
| Unchanged/changed-from-baseline/requires_change | Done | Explicit prior subject/path baseline; no-op returns unconfirmed; fault and contract tests. |
| Optional RFC8785 signatures | Done | Existing restricted and v3 canonical profiles retained, signing extra optional, no key handling added. |
| Read-only proof and freshness properties | Done | Existing runtime proof/Hypothesis plus new MCP socket/subprocess/file-open denial. |
| tau/SWE-bench/Inspect adapters | Partial | Explicit snapshot/native per-instance/collector-store JSON conversions work. No absent tau databases inferred; no native .eval zip decoding or independent state collection. |
| GitHub Action | Done | Composite local action checks packet with stdlib/Python 3.11 and unchanged exit contract; input/output aliases remain protected. |
| Read-only MCP check server | Done | Finite 2025-06-18 stdio handshake/list/check/ping, protocol negative tests, object-only inputs, no path/network/executor capability. |
| Four-state animated timeline | Done | Action/receipt/observation stages, engine reason, explicit fourth label; new four-state CC0 showcase. |
| Duplicated safety behavior identical | Done | output.py and shared safety vectors retained identically; atomic/no-clobber/input-hardlink safeguards reused by conversion. |
| Full-SHA Actions/report-only audits/Dependabot off | Done | Existing pins retained; new workflow actions full-SHA pinned; npm/pip audits report-only; SECURITY_SETTINGS.md keeps owner exclusion and optional restoration paths. |
| Real trajectory fault injection | Done | Pinned public tau archive,173 eligible trajectories,1038 controlled variants with known fault labels. This is public-state diagnostic data plus synthetic interventions. |
| Independent external full-task gold | Partial | Archive omits complete final/goal databases and real collection clocks. No full-task or human truth labels invented; original84-success projection study remains separate. |
| Per-state precision/recall and naive baseline | Done | RESULTS.md/results.json report actual denominators and four-state metrics; deterministic order check and regression failure invariant. |
| Native benchmark checker baseline | Partial | Native reward replay needs absent full databases/goals and executes tools. Unavailable, explicitly recorded; no reconstructed baseline labeled native. |
| LLM-as-judge baseline | Partial | Omitted: no model calls or new judgments; explicit in results and dataset card. |
| Throughput/memory/confidence intervals | Done | Actual timed run and tracemalloc peak, hardware/runtime recorded; intervals intentionally unavailable for correlated nonrandom fault cases. |
| License/version/download/checksum/date | Done | data-v1/provenance.json, pinned SHA, source MIT notice, date fields/unknowns, checksum-enforced fetch. |
| Datasheet/Croissant/HF card/splits/schema/checksums | Done | data-v1 metadata and generated local archive; task-ID grouped dev/test and separate keys. Native mlcroissant 1.1.1 parser reports two RecordSets; no hosted dataset claim. |
| One-command benchmark/local ZIP | Done | make bench fetches, validates, runs, checks invariants and packages build/siftgrain-state-data-v1.zip. No public upload. |
| Human-study protocol/no fabricated labels | Done | data-v1/HUMAN_PROTOCOL.md is protocol-only; no study participants or results claimed. |
| README/changelog/migration/limits | Done | Current brand/quickstart/integrations/results/limits, unreleased changes, stable distributions and schema migration. |
| Clean clone/fresh environment checks | Done for verified product source | Fresh temporary clone of 1bed622 passed the complete software/viewer/benchmark chain; fast-forward to 974e64e passed all 262 Python 3.11.13 tests, lint/types, 19 schemas/10 examples and wheel/sdist after the identity follow-up. The unchanged viewer passed 27 browser observations, two motion regressions and Lighthouse CI. docs/final-verification.json binds results. Prior Python 3.13.9 and installed-wheel checks remain dated evidence. |
| Independent review and delivery record | Done for reviewed product source | Coordinator reviewed runtime d5a0817 and interpreter-only a2e423e with no blocking finding. Final head/check/landing evidence belongs to live PR21, not this static matrix; no self-approval. |
| Repo rename/transfer/new shared package/HF upload | Gated | Unapplied; MIGRATION.md and publishing commands below require applicable named authority. |
| Preserve releases/tags/branches/secrets/people | Done | No tag/history replacement, permanent source deletion, secret work, or messages to people. Installer cache cleanup was observed and reported; subsequent browser installs disable GC. |

## Gated publication commands

Repository rename, after explicit identity approval:
`gh repo rename siftgrain-state --repo alawein/outcome-check`.
Transfer, after separate approval and organization access verification:
GitHub repository Settings -> General -> Danger Zone -> Transfer ownership ->
enter outcome-check and kohyr, then verify the resulting repository and redirects.
No transfer API command is proposed with guessed organization/team IDs.

Dataset upload, after explicit approval to create that public dataset:
`hf upload alawein/siftgrain-state-data-v1 build/benchmark-v1 --repo-type dataset`.
This may create a dataset repository; do not run on existing authorization.
Public release upload, after a separately approved release/tag exists:
`gh release upload <approved-tag> build/siftgrain-state-data-v1.zip --repo alawein/outcome-check`.
Do not use --clobber. New Python publication requires an approved stable version,
reviewed source/tag, existing trusted publisher and release checks; never publish
this development build as an existing 0.4.0 registry file.
