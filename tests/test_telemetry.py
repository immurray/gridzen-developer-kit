import json
import sqlite3
from uuid import uuid4
import pytest
from gridzen_developer import telemetry
from gridzen_developer.product_feedback import accept_usage, safe_dimensions

@pytest.fixture(autouse=True)
def local(monkeypatch,tmp_path):
 monkeypatch.setenv('GRIDZEN_TELEMETRY_DIR',str(tmp_path/'local'))

def test_default_off_and_disable_purge(monkeypatch):
 monkeypatch.setattr(telemetry,'urlopen',lambda *a,**k:pytest.fail('Unexpected upload'))
 telemetry.observe({'task':'signup_phone'})
 assert not telemetry.directory().exists()
 telemetry.configure(True)
 telemetry.enqueue({'task':'PRIVATE_SENTINEL','country':'PRIVATE_SENTINEL','extra':'PRIVATE_SENTINEL'})
 assert 'PRIVATE_SENTINEL' not in (telemetry.directory()/'queue.sqlite3').read_bytes().decode(errors='ignore')
 assert telemetry.status()['queued']==1
 telemetry.configure(False)
 assert telemetry.status()['queued']==0 and not telemetry.enabled()

def test_offline_queue_and_receipt_retry(monkeypatch,tmp_path):
 telemetry.configure(True)
 def unavailable(*a,**kw):raise OSError('no network')
 monkeypatch.setattr(telemetry,'urlopen',unavailable)
 telemetry.observe({'operation':'plan_verification','task':'signup_phone','outcome':'technical_success'})
 assert telemetry.status()['queued']==1
 path=tmp_path/'server.sqlite3'
 class Response:
  status=200
  def __enter__(self):return self
  def __exit__(self,*a):pass
  def read(self,*a):return b'{"accepted":true}'
 def send(request,**kw):
  value=json.loads(request.data)
  assert accept_usage(path,value) and accept_usage(path,value)
  return Response()
 monkeypatch.setattr(telemetry,'urlopen',send)
 assert telemetry.flush()['sent']==1 and telemetry.status()['queued']==0
 with sqlite3.connect(path) as db:assert db.execute('SELECT SUM(count) FROM product_events').fetchone()[0]==1

def test_usage_contract_cannot_claim_authenticated_customer(tmp_path):
 value={'schema_version':1,'event_id':str(uuid4()),'consent_to_share':True,'dimensions':safe_dimensions({'source':'self_reported_local_usage'})}
 assert accept_usage(tmp_path/'db',value)
 for mutation in ({'consent_to_share':False},{'extra':'PRIVATE_SENTINEL'},{'dimensions':{**value['dimensions'],'source':'authenticated_merchant_sandbox'}},{'dimensions':{**value['dimensions'],'phone':'PRIVATE_SENTINEL'}}):
  with pytest.raises(ValueError):accept_usage(tmp_path/'db',{**value,**mutation})

def test_cli_automatic_after_consent_only(monkeypatch,capsys):
 from gridzen_developer import cli
 events=[]
 monkeypatch.setattr(telemetry,'flush',lambda:events.append('upload'))
 monkeypatch.setattr('sys.argv',['gridzen','plan','--country','US','--event','onboarding','--task','signup_phone'])
 cli.main();capsys.readouterr();assert events==[]
 telemetry.configure(True);cli.main();capsys.readouterr()
 assert events==['upload'] and telemetry.status()['queued']==1

def test_actual_stdio_opt_in_records_one_call_without_raw_fields():
 import asyncio
 import sys
 from mcp import Client,StdioServerParameters
 telemetry.configure(True)
 script="from gridzen_developer import telemetry; telemetry.urlopen=lambda *a,**k:(_ for _ in ()).throw(OSError('offline')); from gridzen_developer.mcp import main; main()"
 async def run():
  async with Client(StdioServerParameters(command=sys.executable,args=['-c',script],env={'GRIDZEN_TELEMETRY_DIR':str(telemetry.directory())})) as client:
   result=await client.call_tool('plan_verification',{'country':'US','event':'onboarding','task':'signup_phone'})
   assert not result.is_error and result.structured_content['execution']['live_available'] is False
 asyncio.run(run())
 with sqlite3.connect(telemetry.directory()/'queue.sqlite3') as db:
  payloads=[json.loads(row[0]) for row in db.execute('SELECT payload FROM queue')]
 assert len(payloads)==1
 assert payloads[0]['dimensions']['task']=='signup_phone'
 assert payloads[0]['dimensions']['source']=='self_reported_local_usage'
