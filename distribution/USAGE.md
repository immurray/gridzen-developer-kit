# Remote MCP operational counts

Only successful MCP tool dispatches are aggregated by UTC date and one of the five
public tool names. The counter has no request payload, caller ID, IP address or
request ID columns. It does not measure unique users; acceptance calls count too.
Local stdio does not attach the remote middleware. HTTP research/sandbox endpoints,
discovery and rejected arguments are not MCP tool invocations and are not counted.

Set `GRIDZEN_MCP_EVENTS_DB` in the remote service to enable counting. Use the
independent `gridzen-mcp-metrics` Docker volume in `deploy/compose.yml`.
Never commit the database or publish it as a package artifact. Writes discard rows
aged 90 days; an inactive database is cleaned at its next write. Counter failures
are fail-open and do not change the five tools' protocol or results.

Read-only weekly summary (seven UTC dates including today):

```sh
PYTHONPATH=src python scripts/mcp_usage_report.py --db /path/to/counters.sqlite3
```

Missing or unreadable counters return `status=unavailable, calls=null`, not zero.
An existing, readable database without calls in the selected dates returns zero.
Infrastructure access logs are separate from this database and may contain normal
network connection metadata. Optional website measurement has its own consent.


## Rebuild from a clean source snapshot

Generate the downloadable website archives before building the remote-service
image (they are intentionally not tracked or included in wheel package data):

```sh
python scripts/build_downloads.py
docker build -f deploy/Dockerfile -t gridzen-developer:0.5.0 .
docker compose -f deploy/compose.yml up -d --no-build developer
```

Keep the previous image and compose for rollback. Do not use `down -v`; the
independent metrics volume survives service replacement and restart.
