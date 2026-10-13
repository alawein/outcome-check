# Performance and accessibility

Targets: local-file LCP below 2500  ms, interaction response below 200  ms,
approximately 60 fps main interactions, and a 32,768-byte gzip report budget.
These are measured in automated local runs, not certified for all hardware.

`npm test` blocks HTTP(S) and opens the actual file URL in Chromium, Firefox,
and WebKit. It runs axe 4.10.3 WCAG2/2.1/2.2AA tags for all four themes in both
appearances, rejects every reported violation, checks mobile width, labels,
keyboard-capable native controls, storage denial, reduced motion, and GPU fallback.
No automated tool alone establishes full WCAG conformance.

## Observed browser samples

| Engine | Local-file LCP ms | Event duration maximum ms | Active rAF median/p95 ms | GPU path |
| --- | --- | --- | --- | --- |
| chromium | 76 | 32 | 16.70/16.70 | webgl2 |
| firefox | 92 | 24 | 6.06/6.08 | webgl2 |
| webkit | 65 | 56 | 16.00/18.00 | static |

Each cadence sample contains60 rAF deltas while replaying timeline state motion.
These are main-thread presentation cadence, not GPU profiler frame times or a
midrange-laptop certification. CI enforces median<=18 ms and p95<25 ms for this
finite smoke interaction, plus every observed event duration<200 ms. Event Timing
samples are not field INP; if no qualifying interaction entry appears, it is
unavailable. Engines may differ in LCP/Event Timing support. Exact raw local
results are in [docs/browser-results.json](docs/browser-results.json).

## Lighthouse and bytes

`npm run perf` runs Lighthouse 12.8.2 on the same report through an ephemeral
localhost server because Lighthouse navigation requires HTTP. No external assets
or network-enabled product path is introduced. Last observed performance score
0.68, accessibility 1, LCP 1049.50 ms,
total blocking time 768.00ms. Field INP is unavailable in a navigation audit.
Local-file LCP comes from Playwright above, not the localhost Lighthouse run.

CI enforces Lighthouse LCP<2500 ms and accessibility 1.0, full axe checks,
active-cadence/event limits, and emitted report gzip<=32,768 bytes. The exact bytes
are printed by `uv run python scripts/check_perf.py`, which also verifies the
runtime CSS/logo embeds against their canonical sources. All assets are local.

WebGL2 runs in an optional OffscreenCanvas worker only after viewer interaction.
Initial rendering uses a static surface; no startup GPU context or idle render
loop. Finite600 ms sweeps stop under reduced motion, pause, or hidden-page state.
Workers terminate on pagehide. Text remains full contrast during motion after an
observed opacity-fade contrast defect was fixed. No WebGPU layer is needed.

## Reproduce

```sh
uv run python scripts/build_demo.py
uv run python scripts/build_state_demo.py
uv run python scripts/check_perf.py
npm ci --ignore-scripts
PLAYWRIGHT_SKIP_BROWSER_GC=1 npx playwright install chromium firefox webkit
npm test
npm run perf
node scripts/record-demos.mjs
```

Browser tooling is development-only. Playwright 1.62.1 release July 30, 2026;
axe 4.10.3 March 5, 2025; Lighthouse 12.8.2 August 28, 2025 (npm time metadata read
October 13, 2026). npm/pip audits are report-only. No audit result is a security
certificate. Hardware identity is in RESULTS.md; remote CI timing is separate.
