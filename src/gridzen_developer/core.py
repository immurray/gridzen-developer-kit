from functools import lru_cache
from importlib.resources import files
import json

SCENARIOS = ('match', 'mismatch', 'not_found', 'timeout', 'unsupported')
TASK_ROUTES = {
 'signup_phone': ('onboarding','phone_intelligence','number_line_type'),
 'identity_onboarding': ('onboarding','identity_verification','document_and_liveness'),
 'payout_account': ('payout','bank_account_match','account_holder_match'),
 'phone_possession': (None,'otp','phone_possession'),
 'business_onboarding': ('onboarding','business_kyb','business_and_owners'),
 'account_change': ('account_change',None,'clarify_changed_attribute'),
}
ALIASES = {'identity_verification':'commercial_identity'}
SYNTHETIC_CAPABILITIES = {'phone_intelligence','identity_verification'}
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
 if value not in catalog()['capabilities'] and value not in SYNTHETIC_CAPABILITIES:raise ValueError('UNKNOWN_CAPABILITY')
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

def plan(country_code, event='payout', task=None, stage='prototype'):
 c=country(country_code)
 if event not in EVENTS:raise ValueError('UNKNOWN_EVENT')
 if stage not in ('research','prototype','production'):raise ValueError('UNKNOWN_STAGE')
 if task is not None:
  if task not in TASK_ROUTES:raise ValueError('UNKNOWN_TASK')
  required_event,cap,proof=TASK_ROUTES[task]
  if required_event is not None and required_event!=event:raise ValueError('TASK_EVENT_MISMATCH')
  supported=cap is not None and cap not in ('otp','business_kyb')
  reference=coverage(c['code'],ALIASES.get(cap,cap)) if cap and cap not in ('phone_intelligence','otp','business_kyb') else None
  reasons=['NO_LIVE_ROUTE_ENABLED'] if stage=='production' else ['CLARIFY_REQUIRED_PROOF'] if cap is None else ['CAPABILITY_NOT_IMPLEMENTED'] if not supported else []
  return {'mode':'planning','task':task,'country':c['code'],'event':event,'requested_stage':stage,'capability':cap,'required_proof':proof,
          'task_match_status':'needs_clarification' if cap is None else 'matched' if supported else 'unsupported',
          'research_date':catalog()['research_date'],'research_reference':reference,
          'execution':{'sandbox_available':supported,'live_available':False,'ready_for_requested_stage':supported and stage!='production','blockers':reasons},
          'merchant_surface':{'capabilities_url':'https://gridzen.ai/console/api/capabilities','authentication':'GridZen merchant credential','availability_must_be_checked':True,'phone_intelligence':'adapter_mock','identity_verification':'conditional_provider_sandbox','bank_account_match':'not_available'},
          'skill_path':['gridzen-select-verification','gridzen-integrate-sandbox','gridzen-explain-verification'] if supported else ['gridzen-select-verification'],
          'workflow_requirements':['server_side_call','bounded_timeout','no_automatic_real_approval']+(['session_creation','user_handoff','signed_webhook','deduplication','pending_review','expired_or_abandoned_recovery'] if cap=='identity_verification' else ['number_type_is_not_ownership','OTP_is_separate'] if cap=='phone_intelligence' else []),
          'sandbox_request':{'country':c['code'],'capability':cap,'scenario':'match'} if supported else None,
          'notice':'Research, generic fixtures and conditional merchant sandbox are separate. Task-specific identity fixtures are not hosted user sessions. No production routes or prices are enabled.'}
 cap=EVENTS[event];research=coverage(c['code'],cap)
 return {'mode':'planning','country':c['code'],'event':event,'capability':cap,'evidence_status':research['countries'][0]['evidence_status'],'research_date':catalog()['research_date'],'services':research['countries'][0]['services'],'execution':{'sandbox_available':True,'live_available':False,'reason':'NO_LIVE_ROUTE_ENABLED'},'next_steps':['Run synthetic match, mismatch, not_found, timeout and unsupported fixtures.','Preserve inconclusive outcomes; never infer identity or fraud from missing data.','For a real pilot, confirm provider access and required inputs before enabling a route.'],'sandbox_request':{'country':c['code'],'capability':cap,'scenario':'match'}}

def explain(reason_code):
 integration={'HTTP_401':('Authentication failed.','Check the selected service surface and credential; public fixtures need no key.'),'HTTP_403':('Access was rejected.','Check origin, permissions and allowed surface; do not retry unchanged.'),'HTTP_422':('The input schema was rejected.','Use documented task/country/capability fields and remove personal fields.'),'HTTP_429':('The request rate was exceeded.','Honor Retry-After and retry with a limit.'),'TRANSPORT_ERROR':('The network request failed.','Keep the outcome inconclusive; retry with a limit and inspect service health.'),'HTTP_503':('The service or route is unavailable.','Check capability availability; keep the caller workflow pending or review.')}
 if reason_code in integration:
  meaning,next_step=integration[reason_code]
  return {'reason_code':reason_code,'meaning':meaning,'next_step':next_step,'simulated':False,'verified':False,'business_outcome':'unknown'}
 if reason_code not in REASONS:raise ValueError('UNKNOWN_REASON_CODE')
 meaning,next_step=REASONS[reason_code]
 return {'reason_code':reason_code,'meaning':meaning,'next_step':next_step,'simulated':True,'verified':False}

def simulate(country_code, capability_id, scenario='match'):
 c=country(country_code);capability(capability_id)
 if scenario not in SCENARIOS:raise ValueError('UNKNOWN_SCENARIO')
 code={'match':'SIMULATED_MATCH','mismatch':'SIMULATED_MISMATCH','not_found':'SIMULATED_NOT_FOUND','timeout':'SIMULATED_PROVIDER_TIMEOUT','unsupported':'SIMULATED_UNSUPPORTED'}[scenario]
 result={'id':f"sim_v1:{c['code']}:{capability_id}:{scenario}",'mode':'sandbox','simulated':True,'verified':False,'live_available':False,'provider_calls':0,'country':c['code'],'capability':capability_id,'fixture_outcome':scenario,'status':'inconclusive' if scenario in ('not_found','timeout','unsupported') else 'completed','evidence':[],'reason_code':code,'explanation':explain(code),'notice':'Deterministic synthetic fixture, not a unique transaction or an identity verification. Do not use to approve real people or payments.'}

 if capability_id=='phone_intelligence':
  result['phone']={'valid':True if scenario in ('match','mismatch') else None,'line_type':'mobile' if scenario=='match' else 'voip' if scenario=='mismatch' else None,'ownership_verified':False,'otp_delivered':False,'source':'synthetic_fixture'}
 if capability_id=='identity_verification':
  result['identity']={'source':'synthetic_fixture','user_session_created':False,'document_collected':False,'liveness_executed':False}
 return result

def get_simulation(identifier):
 parts=identifier.split(':')
 if len(parts)!=4 or parts[0]!='sim_v1':raise ValueError('UNKNOWN_SANDBOX_ID')
 return simulate(*parts[1:])
