# Hosted MCP metrics rehearsal

The hosted HTTP server uses the normal `gridzen_developer.server:app` entrypoint. The isolated Compose overlay replaces the old metrics volume with a protected, read-only connection-file mount and sets the storage and environment explicitly. The hosted writer can modify public aggregate buckets and receipt hashes only. GridZen installs the schema and imports the reviewed historical archive before this writer can start recording aggregates. The existing hosted service and release tag are unchanged by this candidate.

UTC buckets, the two consented endpoints and the daily aggregate/summary ceilings retain the old behavior. Receipt hashes deduplicate across 30 retained UTC dates. The separate call-source table retains trusted loopback test attribution and keeps publicly labelled tests self-reported. A metrics outage leaves synthetic tools available and denies receipt acceptance instead of using the old file. The separate stdio entrypoint keeps its existing local opt-in semantics and cannot write hosted metrics.

Use `deploy/compose.metrics-postgres.yml` only in a disposable environment with an isolated image and a read-only connection file readable by the image's non-root UID. The paired GridZen draft includes roles, matching frozen-source adoption, GEO reader and a two-repository acceptance fixture.
