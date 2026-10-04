# Functional evidence

30 local pytest cases passed after initial missing-module failure. The independently
specified twelve-case matrix covers clean, wrong-state, failed/missing/unknown/null
action, missing/stale/future/wrong-subject observation, missing path and Boolean
versus number. Other tests cover explicit retries, row ordering, recursive equality,
duplicate IDs/keys, unknown fields, timezones, limits, nesting, UTF-8/BOM, nonfinite
numbers, hard-link output preservation, escaping and the 10,000-entry boundary.

No remaining mismatch against the declared matrix. These tests validate decisions
over supplied evidence, not authentic execution or collector accuracy. Isolated
artifact and hosted results are reported in release notes after actual execution.
