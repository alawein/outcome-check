# Packet contract v1

Exact root fields: schema_version (integer 1), as_of (timezone-aware RFC3339),
requirements (nonempty array), actions (array), observations (array). Each array
<= 10,000, IDs unique per array. IDs, subjects and object keys are nonblank strings
<= 200 characters. Files UTF-8 without BOM, <= 5 MiB; duplicate JSON keys invalid.

Requirement exact fields: id, subject, path (1..32 object-key strings), expected
(JSON value, recursive depth <= 32), observation_id, max_age_seconds (nonnegative
integer, Boolean forbidden), action_id (ID or null). Observation exact fields:
id, subject, observed_at (RFC3339), state (JSON object). Action exact fields:
id, status (succeeded|failed|unknown). Unknown fields and nonfinite numbers fail.

Missing references are unobserved. Only the named observation is checked. Its
subject must match and age must be in [0,max_age_seconds] relative to as_of.
Missing object paths are unobserved. Equality is recursive and typed, except
integer/float numeric equivalence. No array indexing, expressions or collectors.

Action: succeeded=>confirmed, failed=>contradicted, unknown/missing=>unobserved,
null=>not_required. Overall contradicted if either required component contradicted;
confirmed if outcome confirmed and action confirmed/not_required; otherwise
unobserved. Reports show both components and an outcome reason. No clock lookup.
Output schema_version 1, counts, results, exit_code and exact input SHA-256.

Offset hours 00..23/minutes 00..59 are enforced. Fractional-second freshness uses
every supplied digit. Leap seconds and year 0000 are unsupported by the calendar
parser and rejected. Timestamp strings are limited to 64 characters.
