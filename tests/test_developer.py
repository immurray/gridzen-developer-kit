import json
import pytest
from fastapi.testclient import TestClient
from gridzen_developer import core
from gridzen_developer.server import app
client=TestClient(app)

def test_catalog_counts_and_no_implied_commercial_access():
 data=core.catalog()
 assert len(data['countries'])==198
 assert sum(len(c['services']) for c in data['countries'])==230
 for c in data['countries']:
  assert c['live_available'] is False
  for s in c['services']:
   assert not s['live_available']
   assert s['source_urls']
 assert core.coverage('AF')['countries'][0]['evidence_status']=='UNCONFIRMED'
 assert core.coverage('AZ')['countries'][0]['evidence_status']=='RESEARCH_EVIDENCE'

@pytest.mark.parametrize('scenario',core.SCENARIOS)
def test_synthetic_results_never_verify_a_person(scenario):
 r=client.post('/api/sandbox/verifications',json={'country':'ID','capability':'bank_account_match','scenario':scenario})
 assert r.status_code==200
 data=r.json();assert data['simulated'] and not data['verified'] and data['provider_calls']==0
 assert data['evidence']==[]
 assert client.get('/api/sandbox/verifications/'+data['id']).json()==data
 if scenario in ('not_found','timeout','unsupported'):assert data['status']=='inconclusive'
 assert client.get('/api/explain/'+data['reason_code']).json()['verified'] is False

@pytest.mark.parametrize('extra', [{'name':'Example'},{'account_number':'synthetic'},{'mode':'live'},{'provider':'fake'},{'consent':True}])
def test_no_live_or_personal_fields_accepted(extra):
 r=client.post('/api/sandbox/verifications',json={'country':'ID','capability':'bank_account_match','scenario':'match',**extra})
 assert r.status_code==422
 assert r.json()['error']=='INVALID_INPUT'

@pytest.mark.parametrize('body',[{'country':'ZZ','capability':'bank_account_match'}, {'country':'ID','capability':'invented'},{'country':'ID','capability':'bank_account_match','scenario':'verified'}])
def test_unknown_input_does_not_fabricate_success(body):
 assert client.post('/api/sandbox/verifications',json=body).status_code in (400,422)

def test_schema_and_bounded_request():
 assert client.post('/api/plan',json={'country':'ID','event':'payout'}).json()['execution']=={'sandbox_available':True,'live_available':False,'reason':'NO_LIVE_ROUTE_ENABLED'}
 assert client.post('/api/plan',content='x'*4097).status_code==413
 assert client.get('/api/sandbox/verifications/not-a-fixture').status_code==400
 assert client.get('/api/openapi.json').json()['servers'][0]['url']=='/developers'
 assert client.get('/api/coverage').headers['cache-control']=='no-store'

def test_snapshot_known_limits_survive_projection():
 az=core.coverage('AZ','commercial_identity')['countries'][0]
 assert any('生物识别' in s['user_participation'] for s in az['services'])
 assert any(s['limitations'] for s in az['services'])
 assert core.plan('ID','payout')['capability']=='bank_account_match'


def test_distribution_has_no_private_or_recursive_files():
 from pathlib import Path
 import zipfile
 root=Path(__file__).resolve().parents[1]
 with zipfile.ZipFile(root/'src/gridzen_developer/web/downloads/gridzen-developer-kit.zip') as z:
  names=z.namelist()
  assert all(not x.endswith('.zip') and '.env' not in x and 'secrets/' not in x for x in names)
  assert 'gridzen-developer-kit/src/gridzen_developer/data/catalog.json' in names
  assert len([n for n in names if n.endswith('SKILL.md')])==3
