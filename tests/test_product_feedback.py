import json
import sqlite3
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from gridzen_developer import core
from gridzen_developer.product_feedback import accept_summary, record_safe
from gridzen_developer.server import app
from test_remote import rpc


def summary():
 return dict(schema_version=1,summary_id=str(uuid4()),task='signup_phone',country='US',requested_capability='phone_intelligence',stage='prototype',outcome='blocked',blocker='missing_workflow_step',skill='gridzen-integrate-sandbox',consent_to_share=True)


def test_task_routing_and_production_boundary():
 assert core.plan('US','onboarding','signup_phone')['capability']=='phone_intelligence'
 assert core.plan('US','onboarding','identity_onboarding')['capability']=='identity_verification'
 assert not core.plan('US','onboarding','identity_onboarding','production')['execution']['ready_for_requested_stage']
 assert core.plan('US','onboarding','phone_possession')['task_match_status']=='unsupported'
 with pytest.raises(ValueError):core.plan('US','payout','signup_phone')
 for cap in ('phone_intelligence','identity_verification'):
  for outcome in core.SCENARIOS:
   value=core.simulate('US',cap,outcome)
   assert value['provider_calls']==0 and value['verified'] is False
   assert core.get_simulation(value['id'])==value


def test_consent_dedup_and_no_personal_data(tmp_path):
 path=tmp_path/'counts.db';value=summary()
 assert accept_summary(path,value)
 assert accept_summary(path,value)
 with sqlite3.connect(path) as db:assert db.execute('SELECT SUM(count) FROM product_events').fetchone()[0]==1
 for mutation in ({'email':'PRIVATE_SENTINEL'},{'source':'authenticated_feedback'},{'consent_to_share':False}):
  with pytest.raises(ValueError):accept_summary(path,{**value,**mutation})
 record_safe(path,dict(task='PRIVATE_SENTINEL',country='PRIVATE_SENTINEL',reason='PRIVATE_SENTINEL'))
 assert b'PRIVATE_SENTINEL' not in path.read_bytes()
 assert value['summary_id'].encode() not in path.read_bytes()


def test_feedback_cli_is_local_without_share(monkeypatch,capsys):
 from gridzen_developer import cli
 from gridzen_developer.client import Gridzen
 monkeypatch.setattr(Gridzen,'_call',lambda *a,**k:pytest.fail('Unexpected network'))
 monkeypatch.setattr('sys.argv',['gridzen','feedback','--task','signup_phone','--country','US'])
 cli.main();value=json.loads(capsys.readouterr().out)
 assert value['consent_to_share'] is False and value['task']=='signup_phone'


def test_sdk_classifies_http_failure_without_returning_body(monkeypatch):
 from urllib.error import HTTPError
 from gridzen_developer.client import Gridzen,GridzenError
 def fail(*a,**kw):raise HTTPError('https://gridzen.ai',429,'PRIVATE_SENTINEL',{},None)
 monkeypatch.setattr('gridzen_developer.client.urlopen',fail)
 with pytest.raises(GridzenError) as error:Gridzen().plan('US')
 assert error.value.reason=='rate_limit' and error.value.retryable
 assert 'PRIVATE_SENTINEL' not in str(error.value)


def test_real_integration_errors_are_not_identity_outcomes():
 for code in ('HTTP_401','HTTP_403','HTTP_422','HTTP_429','HTTP_503','TRANSPORT_ERROR'):
  result=core.explain(code)
  assert result['simulated'] is False and result['business_outcome']=='unknown' and result['verified'] is False
