"""Remote-only, fail-open UTC aggregates. No request fields or identifiers."""
import asyncio
from contextvars import ContextVar
import os
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

TOOLS = frozenset(('get_coverage', 'plan_verification', 'create_sandbox_verification', 'get_sandbox_verification', 'explain_result'))
RETENTION_DAYS = 90
CALL_SOURCE = ContextVar('gridzen_call_source', default='unknown')
SOURCES = frozenset(('internal_test', 'self_reported_test', 'unknown'))

def record(path, tool, day=None, source='unknown'):
    if tool not in TOOLS:
        return
    source = source if source in SOURCES else 'unknown'
    day = day or datetime.now(timezone.utc).date()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path, timeout=5) as db:
        db.execute('CREATE TABLE IF NOT EXISTS calls (day TEXT NOT NULL, tool TEXT NOT NULL, count INTEGER NOT NULL, PRIMARY KEY(day, tool))')
        db.execute('CREATE TABLE IF NOT EXISTS call_sources (day TEXT NOT NULL, tool TEXT NOT NULL, source TEXT NOT NULL, count INTEGER NOT NULL, PRIMARY KEY(day, tool, source))')
        db.execute('DELETE FROM call_sources WHERE day < ?', ((day - timedelta(days=RETENTION_DAYS - 1)).isoformat(),))
        db.execute('DELETE FROM calls WHERE day < ?', ((day - timedelta(days=RETENTION_DAYS - 1)).isoformat(),))
        db.execute('INSERT INTO calls VALUES (?, ?, 1) ON CONFLICT(day, tool) DO UPDATE SET count=count+1', (day.isoformat(), tool))
        db.execute('INSERT INTO call_sources VALUES (?, ?, ?, 1) ON CONFLICT(day, tool, source) DO UPDATE SET count=count+1', (day.isoformat(), tool, source))

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
    from .product_feedback import record_safe
    path=os.environ.get('GRIDZEN_MCP_EVENTS_DB')
    params=ctx.params if isinstance(ctx.params,dict) else {}
    arguments=params.get('arguments') if isinstance(params.get('arguments'),dict) else {}
    name=params.get('name')
    observe=ctx.method=='tools/call'
    dimensions={'operation':name,'task':arguments.get('task'),'capability':arguments.get('capability'),'country':arguments.get('country'),'stage':arguments.get('stage','prototype'),'source':CALL_SOURCE.get(),'mode':'research' if name in ('get_coverage','plan_verification') else 'synthetic_fixture'}
    try:
        result=await call_next(ctx)
    except Exception as error:
        if observe:
            await asyncio.to_thread(record_safe,path,{**dimensions,'outcome':'integration_error','reason':'schema_error' if getattr(getattr(error,'error',None),'code',None)==-32602 else 'tool_error'})
        raise
    if observe:
        failed=getattr(result,'is_error',False)
        structured=getattr(result,'structured_content',None)
        if isinstance(structured,dict):
            dimensions['capability']=structured.get('capability',dimensions['capability'])
        blocked=isinstance(structured,dict) and (structured.get('task_match_status') in ('unsupported','needs_clarification') or structured.get('requested_stage')=='production')
        reason='tool_error' if failed else 'production_disabled' if blocked and structured.get('requested_stage')=='production' else 'unavailable_route' if blocked else 'none'
        await asyncio.to_thread(record_safe,path,{**dimensions,'outcome':'integration_error' if failed else 'capability_unavailable' if blocked else 'technical_success','reason':reason})
        if path and isinstance(name,str) and name in TOOLS and not failed:
            try:await asyncio.to_thread(record,path,name,source=CALL_SOURCE.get())
            except (OSError,sqlite3.Error):pass
    return result
