import asyncio
import sqlite3
from datetime import date
from gridzen_developer.remote import CallSourceMiddleware
from gridzen_developer.usage import CALL_SOURCE, record


def classify(headers,peer='127.0.0.1'):
    async def run():
        observed=[]
        async def app(scope,receive,send): observed.append(CALL_SOURCE.get())
        await CallSourceMiddleware(app)({'type':'http','path':'/mcp','client':(peer,123),'headers':headers},None,None)
        assert CALL_SOURCE.get()=='unknown'
        return observed[0]
    return asyncio.run(run())


def test_only_explicit_local_test_is_trusted():
    marker=[(b'x-gridzen-purpose',b'internal_test')]
    assert classify(marker)=='internal_test'
    assert classify([])=='unknown'
    assert classify(marker,'198.51.100.1')=='self_reported_test'
    assert classify(marker+[(b'x-real-ip',b'127.0.0.1')])=='self_reported_test'
    assert classify(marker+[(b'x-forwarded-for',b'127.0.0.1')])=='self_reported_test'


def test_sources_preserve_legacy_totals_without_reclassifying_history(tmp_path):
    path=tmp_path/'counter.sqlite3'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE calls(day TEXT,tool TEXT,count INTEGER,PRIMARY KEY(day,tool))')
        db.execute('INSERT INTO calls VALUES(?,?,?)',('2026-10-10','get_coverage',42))
    record(path,'get_coverage',date(2026,10,10),source='internal_test')
    record(path,'get_coverage',date(2026,10,10),source='private-identifier')
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT count FROM calls').fetchone()[0]==44
        assert dict(db.execute('SELECT source,count FROM call_sources'))=={'internal_test':1,'unknown':1}
    assert b'private-identifier' not in path.read_bytes()


def test_remote_source_context_reaches_counter_threads(tmp_path,monkeypatch):
    # SDK transport managers have one lifespan; isolate from other server tests.
    import subprocess,sys,os
    path=tmp_path/'rpc.sqlite3'
    code="""
import sqlite3,sys
from fastapi.testclient import TestClient
from gridzen_developer.server import app
headers={'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
body={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'get_coverage','arguments':{'country':'MX'}}}
with TestClient(app) as client:
 for extra in ({},{'X-Gridzen-Purpose':'internal_test'},{'X-Gridzen-Purpose':'internal_test','X-Real-IP':'127.0.0.1'}):
  assert 'result' in client.post('/mcp',headers={**headers,**extra},json=body).json()
with sqlite3.connect(sys.argv[1]) as db:
 assert dict(db.execute('SELECT source,count FROM call_sources'))=={'internal_test':1,'self_reported_test':1,'unknown':1}
"""
    subprocess.run([sys.executable,'-c',code,str(path)],check=True,timeout=30,env={**os.environ,'GRIDZEN_MCP_EVENTS_DB':str(path),'GRIDZEN_MCP_LOCAL_TEST_PEERS':'testclient'})
