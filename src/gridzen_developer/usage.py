"""Remote-only, fail-open UTC aggregates. No request fields or identifiers."""
import asyncio
import os
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

TOOLS = frozenset(('get_coverage', 'plan_verification', 'create_sandbox_verification', 'get_sandbox_verification', 'explain_result'))
RETENTION_DAYS = 90

def record(path, tool, day=None):
    if tool not in TOOLS:
        return
    day = day or datetime.now(timezone.utc).date()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path, timeout=5) as db:
        db.execute('CREATE TABLE IF NOT EXISTS calls (day TEXT NOT NULL, tool TEXT NOT NULL, count INTEGER NOT NULL, PRIMARY KEY(day, tool))')
        db.execute('DELETE FROM calls WHERE day < ?', ((day - timedelta(days=RETENTION_DAYS - 1)).isoformat(),))
        db.execute('INSERT INTO calls VALUES (?, ?, 1) ON CONFLICT(day, tool) DO UPDATE SET count=count+1', (day.isoformat(), tool))

def summarize(path, end=None):
    end = end or datetime.now(timezone.utc).date()
    start = end - timedelta(days=6)
    result = {'status': 'unavailable', 'start': start.isoformat(), 'end': end.isoformat(), 'timezone': 'UTC', 'calls': None, 'by_tool': {}}
    if not path or not Path(path).is_file():
        return result
    try:
        with sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True) as db:
            rows = db.execute('SELECT tool, SUM(count) FROM calls WHERE day BETWEEN ? AND ? GROUP BY tool', (start.isoformat(), end.isoformat())).fetchall()
        result.update(status='available', calls=sum(n for _, n in rows), by_tool=dict(rows))
    except sqlite3.Error:
        pass
    return result

async def aggregate_calls(ctx, call_next):
    result = await call_next(ctx)
    if ctx.method == 'tools/call' and isinstance(ctx.params, dict):
        tool = ctx.params.get('name')
        path = os.environ.get('GRIDZEN_MCP_EVENTS_DB')
        if path and isinstance(tool, str) and tool in TOOLS and not getattr(result, 'is_error', False):
            try:
                await asyncio.to_thread(record, path, tool)
            except (OSError, sqlite3.Error):
                # Aggregate availability must never change tool behavior.
                pass
    return result
