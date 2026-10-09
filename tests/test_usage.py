from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
import sqlite3
from gridzen_developer.usage import record, summarize
import importlib
import gridzen_developer.server as server_module
from fastapi.testclient import TestClient
from test_remote import rpc


def test_concurrent_aggregates_retention_and_read_only(tmp_path):
    path = tmp_path / 'counter.sqlite3'
    day = date(2026, 10, 9)
    assert summarize(path, day)['calls'] is None
    assert not path.exists()
    record(path, 'get_coverage', day - timedelta(days=91))
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: record(path, 'get_coverage', day), range(40)))
    record(path, 'private-input-is-not-a-tool', day)
    assert summarize(path, day)['calls'] == 40
    with sqlite3.connect(path) as db:
        assert [row[1] for row in db.execute('PRAGMA table_info(calls)')] == ['day', 'tool', 'count']
        assert db.execute('SELECT COUNT(*) FROM calls').fetchone()[0] == 1


def test_remote_only_valid_tools_and_fail_open(tmp_path, monkeypatch):
    path = tmp_path / 'remote.sqlite3'
    monkeypatch.setenv('GRIDZEN_MCP_EVENTS_DB', str(path))
    with TestClient(importlib.reload(server_module).app) as client:
        rpc(client, 'tools/list')
        assert not path.exists()
        response = rpc(client, 'tools/call', {'name':'get_coverage','arguments':{'country':'MX'}})
        assert 'result' in response.json()
        assert summarize(path)['by_tool'] == {'get_coverage': 1}
        bad = rpc(client, 'tools/call', {'name':'get_coverage','arguments':{'name':'PRIVATE_SENTINEL'}})
        assert 'error' in bad.json()
        assert summarize(path)['calls'] == 1
        monkeypatch.setenv('GRIDZEN_MCP_EVENTS_DB', '/dev/null/impossible.sqlite3')
        assert 'result' in rpc(client, 'tools/call', {'name':'get_coverage','arguments':{'country':'MX'}}).json()
    assert b'PRIVATE_SENTINEL' not in path.read_bytes()
