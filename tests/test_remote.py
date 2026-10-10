import pytest
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse
from starlette.applications import Starlette
from starlette.routing import Route
from gridzen_developer.server import app
from gridzen_developer.remote import MCPBounds

HEADERS={'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
def rpc(c,method,params=None):
 return c.post('/mcp',headers=HEADERS,json={'jsonrpc':'2.0','id':1,'method':method,'params':params or {}})

def test_remote_discovery_fixtures_and_rejected_personal_inputs(tmp_path,monkeypatch):
 import sqlite3
 from test_product_feedback import summary
 path=tmp_path/"calls.db"
 monkeypatch.setenv("GRIDZEN_MCP_EVENTS_DB",str(path))
 with TestClient(app) as c:
  init=rpc(c,'initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'gridzen-test','version':'1'}})
  assert init.status_code==200,init.text
  assert init.json()['result']['serverInfo']['version']=='0.5.0'
  tools=rpc(c,'tools/list').json()['result']['tools']
  assert len(tools)==5
  assert all(t['inputSchema']['additionalProperties'] is False for t in tools)
  for scenario in ('match','mismatch','not_found','timeout','unsupported'):
   r=rpc(c,'tools/call',{'name':'create_sandbox_verification','arguments':{'country':'ID','capability':'bank_account_match','scenario':scenario}})
   assert r.status_code==200,r.text
   value=r.json()['result']['structuredContent']
   assert value['verified'] is False and value['simulated'] is True and value['provider_calls']==0
   if scenario in ('timeout','not_found','unsupported'):assert value['status']=='inconclusive'
  planned=rpc(c,'tools/call',{'name':'plan_verification','arguments':{'country':'US','event':'onboarding','task':'signup_phone'}})
  assert planned.json()['result']['structuredContent']['capability']=='phone_intelligence'
  assert c.post('/api/feedback',json=summary()).status_code==200
  assert c.post('/api/feedback',json={**summary(),'source':'authenticated_feedback'}).status_code==422
  bad=rpc(c,'tools/call',{'name':'create_sandbox_verification','arguments':{'country':'ID','capability':'bank_account_match','account_number':'PRIVATE_TEST_SENTINEL'}})
  assert bad.json()['error']['code']==-32602
  assert 'PRIVATE_TEST_SENTINEL' not in bad.text
  oversized=rpc(c,'tools/call',{'name':'get_coverage','arguments':{'country':'X'*161}})
  assert oversized.json()['error']['code']==-32602
  assert c.post('/mcp',content='x'*4097).status_code==413
  hostile=c.post('/mcp',headers={**HEADERS,'Host':'evil.example'},json={'jsonrpc':'2.0','id':1,'method':'tools/list'})
  assert hostile.status_code==421
  origin=c.post('/mcp',headers={**HEADERS,'Origin':'https://evil.example'},json={'jsonrpc':'2.0','id':1,'method':'tools/list'})
  assert origin.status_code==403

 with sqlite3.connect(path) as db:
  assert db.execute("SELECT SUM(count) FROM product_events WHERE outcome='integration_error'").fetchone()[0]>=1
  assert db.execute("SELECT SUM(count) FROM product_events WHERE source='authenticated_feedback'").fetchone()[0] is None
 assert b'PRIVATE_TEST_SENTINEL' not in path.read_bytes()

def test_rate_limit_is_bounded_and_recovers_without_affecting_health():
 now=[0]
 async def ok(request):return JSONResponse({'ok':True})
 bounded=MCPBounds(Starlette(routes=[Route('/{path:path}',ok,methods=['GET','POST'])]),per_client=2,total=3,clock=lambda:now[0])
 with TestClient(bounded) as c:
  assert c.post('/mcp').status_code==200
  assert c.post('/mcp').status_code==200
  assert c.post('/mcp').status_code==429
  assert c.get('/health').status_code==200
  assert c.post('/mcp',headers={'X-Real-IP':'other'}).status_code==200
  assert c.post('/mcp',headers={'X-Real-IP':'third'}).status_code==429
  now[0]=61
  assert c.post('/mcp').status_code==200
