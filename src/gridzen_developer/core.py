from functools import lru_cache
from importlib.resources import files
import json

SCENARIOS = ('match', 'mismatch', 'not_found', 'timeout', 'unsupported')
EVENTS = {'onboarding': 'commercial_identity', 'payout': 'bank_account_match', 'account_change': 'phone_identity'}
REASONS = {
 'SIMULATED_MATCH': ('The synthetic fixture matches.', 'Continue testing; this does not authorize a real action.'),
 'SIMULATED_MISMATCH': ('The synthetic fixture does not match.', 'Request correction or review; mismatch alone does not establish fraud.'),
 'SIMULATED_NOT_FOUND': ('The fixture has no matching record.', 'Treat as inconclusive; check inputs or use an authorized alternative.'),
 'SIMULATED_PROVIDER_TIMEOUT': ('The fixture simulates a provider timeout.', 'Treat as inconclusive; retry with a limit, never turn timeout into mismatch.'),
 'SIMULATED_UNSUPPORTED': ('The fixture simulates an unsupported route.', 'Choose a supported, authorized route or manual review.'),
}
@lru_cache(maxsize=1)
def catalog():
 return json.loads(files('gridzen_developer').joinpath('data/catalog.json').read_text())

def country(code):
 code=code.upper()
 result=next((x for x in catalog()['countries'] if x['code']==code),None)
 if result is None:raise ValueError('UNKNOWN_COUNTRY: use a code returned by coverage()')
 return result

def capability(value):
 if value not in catalog()['capabilities']:raise ValueError('UNKNOWN_CAPABILITY')
 return value

def coverage(country_code=None, capability_id=None):
 if capability_id:capability(capability_id)
 rows=[country(country_code)] if country_code else catalog()['countries']
 result=[]
 for row in rows:
  services=[s for s in row['services'] if not capability_id or s['capability']==capability_id]
  result.append({**row,'services':services,'capability_evidence':{k:v for k,v in row['capability_evidence'].items() if not capability_id or k==capability_id},'evidence_status':'RESEARCH_EVIDENCE' if services else 'UNCONFIRMED'})
 if not country_code:result=[{k:r[k] for k in ('code','name','region','research_class','live_available','evidence_status')}|{'service_count':len(r['services'])} for r in result]
 return {'mode':'research','research_date':catalog()['research_date'],'live_routes':0,'capabilities':catalog()['capabilities'],'countries':result,'notice':'Research evidence is not Gridzen commercial access, provider authorization, or a current availability guarantee.'}

def plan(country_code, event='payout'):
 c=country(country_code)
 if event not in EVENTS:raise ValueError('UNKNOWN_EVENT')
 cap=EVENTS[event];research=coverage(c['code'],cap)
 return {'mode':'planning','country':c['code'],'event':event,'capability':cap,'evidence_status':research['countries'][0]['evidence_status'],'research_date':catalog()['research_date'],'services':research['countries'][0]['services'],'execution':{'sandbox_available':True,'live_available':False,'reason':'NO_LIVE_ROUTE_ENABLED'},'next_steps':['Run synthetic match, mismatch, not_found, timeout and unsupported fixtures.','Preserve inconclusive outcomes; never infer identity or fraud from missing data.','For a real pilot, confirm provider access and required inputs before enabling a route.'],'sandbox_request':{'country':c['code'],'capability':cap,'scenario':'match'}}

def explain(reason_code):
 if reason_code not in REASONS:raise ValueError('UNKNOWN_REASON_CODE')
 meaning,next_step=REASONS[reason_code]
 return {'reason_code':reason_code,'meaning':meaning,'next_step':next_step,'simulated':True,'verified':False}

def simulate(country_code, capability_id, scenario='match'):
 c=country(country_code);capability(capability_id)
 if scenario not in SCENARIOS:raise ValueError('UNKNOWN_SCENARIO')
 code={'match':'SIMULATED_MATCH','mismatch':'SIMULATED_MISMATCH','not_found':'SIMULATED_NOT_FOUND','timeout':'SIMULATED_PROVIDER_TIMEOUT','unsupported':'SIMULATED_UNSUPPORTED'}[scenario]
 return {'id':f"sim_v1:{c['code']}:{capability_id}:{scenario}",'mode':'sandbox','simulated':True,'verified':False,'live_available':False,'provider_calls':0,'country':c['code'],'capability':capability_id,'fixture_outcome':scenario,'status':'inconclusive' if scenario in ('not_found','timeout','unsupported') else 'completed','evidence':[],'reason_code':code,'explanation':explain(code),'notice':'Deterministic synthetic fixture, not a unique transaction or an identity verification. Do not use to approve real people or payments.'}

def get_simulation(identifier):
 parts=identifier.split(':')
 if len(parts)!=4 or parts[0]!='sim_v1':raise ValueError('UNKNOWN_SANDBOX_ID')
 return simulate(*parts[1:])
