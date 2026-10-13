# Migration

Siftgrain State is the display brand. Package `outcome-check`, import
`outcome_check`, CLI `outcome-check`, and repository URL retain their identities.
No existing tag, registry file, packet, or JSON result field is renamed.

v0.2.x schema v1 packets load directly. Their three-state semantics remain intact;
no required change or baseline is silently added. Schema v2/v3 adds `unconfirmed`.
The viewer labels that state `unconfirmed-no-change` without changing JSON bytes.

Use `outcome_check.contract.migrate_to_v3(packet)` for validated deep-copy migration
of unsigned packets. Signed input requires authentic re-signing by the supplier;
the migrator refuses to discard or relabel signatures. See the versioned contract
for RFC8785 and legacy canonicalization differences.

New entrypoints `outcome-convert` and `outcome-check-mcp` are additive. Conversion
requires explicit subject, clocks, and goals. Outputs use the same no-clobber,
input-alias, and atomic-write policy as the checker.

Remote renames/transfers remain unapplied. If separately authorized, exact
repository rename is `gh repo rename siftgrain-state --repo alawein/outcome-check`.
GitHub redirects do not rename Python imports or preserve every external badge;
update verified consumers and release metadata before any package-name migration.
A kohyr transfer additionally needs confirmed organization permissions and its
own explicit repository transfer approval. No blanket transfer or registry-name
availability is inferred from the limited name search.
