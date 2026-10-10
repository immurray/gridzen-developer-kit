import argparse,json
from pathlib import Path
from uuid import uuid4
from . import core

def main():
 p=argparse.ArgumentParser(description='Gridzen research + synthetic sandbox (no real provider calls)');s=p.add_subparsers(dest='command',required=True)
 x=s.add_parser('coverage');x.add_argument('--country');x.add_argument('--capability')
 x=s.add_parser('plan');x.add_argument('--country',required=True);x.add_argument('--event',choices=list(core.EVENTS),default='payout')
 x.add_argument('--task',choices=list(core.TASK_ROUTES));x.add_argument('--stage',choices=['research','prototype','production'],default='prototype')
 x=s.add_parser('feedback',help='Generate a local category-only task summary; network requires --share')
 x.add_argument('--input');x.add_argument('--output');x.add_argument('--share',action='store_true')
 from .product_feedback import TASKS,CAPABILITIES,STAGES,OUTCOMES,REASONS,SKILLS
 for name,choices,default in [('task',TASKS,'unknown'),('country',None,'unknown'),('requested-capability',CAPABILITIES,'unknown'),('stage',STAGES,'prototype'),('outcome',OUTCOMES-{'technical_success','integration_error'},'unknown'),('blocker',REASONS,'unknown'),('skill',SKILLS,'unknown')]:x.add_argument('--'+name,choices=sorted(choices) if choices else None,default=default)
 x=s.add_parser('simulate');x.add_argument('--country',required=True);x.add_argument('--capability',required=True);x.add_argument('--scenario',choices=core.SCENARIOS,default='match')
 x=s.add_parser('explain');x.add_argument('reason_code')
 s.add_parser('skills',help='List bundled Skill directories; copy a complete directory into your assistant to activate it')
 from .setup import CLIENTS
 x=s.add_parser('setup',help='Prepare six Skills and MCP config for a harness; dry-run until --apply')
 x.add_argument('--client',choices=['all',*CLIENTS],required=True);x.add_argument('--project',default='.');x.add_argument('--apply',action='store_true')
 x=s.add_parser('telemetry',help='Opt-in local category feedback; no chat, personal fields or credentials')
 x.add_argument('action',choices=['enable','disable','status','flush','record'])
 x.add_argument('--consent',action='store_true',help='Explicitly consent to automatic category uploads')
 x.add_argument('--task',choices=sorted(TASKS),default='unknown');x.add_argument('--skill',choices=sorted(SKILLS),default='unknown')
 x.add_argument('--outcome',choices=sorted(OUTCOMES),default='unknown');x.add_argument('--blocker',choices=sorted(REASONS),default='unknown')
 a=p.parse_args()
 if a.command=='telemetry':
  from . import telemetry
  try:
   if a.action=='enable':
    if not a.consent:p.error('Enabling automatic feedback requires --consent. Fixed categories only; disable anytime.')
    result=telemetry.configure(True)
   elif a.action=='disable':result=telemetry.configure(False)
   elif a.action=='status':result=telemetry.status()
   elif a.action=='flush':result=telemetry.flush()
   else:
    telemetry.observe({'operation':'task_summary','task':a.task,'skill':a.skill,'mode':'local_draft','outcome':a.outcome,'reason':a.blocker})
    result=telemetry.status()
  except (OSError,ValueError) as exc:p.error(type(exc).__name__)
  print(json.dumps(result,indent=2));return
 if a.command=='feedback':
  from .product_feedback import validate_summary
  try:
   result=json.loads(Path(a.input).read_text()) if a.input else {'schema_version':1,'summary_id':str(uuid4()),'task':a.task,'country':a.country.upper() if a.country!='unknown' else 'unknown','requested_capability':a.requested_capability,'stage':a.stage,'outcome':a.outcome,'blocker':a.blocker,'skill':a.skill,'consent_to_share':False}
   result['consent_to_share']=a.share
   result=validate_summary(result)
   if a.output:Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
   if a.share:
    from .client import Gridzen, GridzenError
    try:receipt=Gridzen().share_feedback(result)
    except GridzenError as exc:p.error(str(exc))
    print(json.dumps({'summary':result,'receipt':receipt},indent=2));return
  except (ValueError,OSError) as exc:p.error(str(exc))
  print(json.dumps(result,indent=2));return
 if a.command=='setup':
  from .setup import setup
  try: result=setup(a.client,a.project,a.apply)
  except (ValueError,OSError) as exc:p.error(str(exc))
  print(json.dumps(result,ensure_ascii=False,indent=2));return
 if a.command=='skills':
  from .skills import list_skills
  print(json.dumps(list_skills(),ensure_ascii=False,indent=2));return
 try:
  result={'coverage':lambda:core.coverage(a.country,a.capability),'plan':lambda:core.plan(a.country,a.event,a.task,a.stage),'simulate':lambda:core.simulate(a.country,a.capability,a.scenario),'explain':lambda:core.explain(a.reason_code)}[a.command]()
 except ValueError as e:
  from .telemetry import observe
  observe({'operation':{'coverage':'get_coverage','plan':'plan_verification','simulate':'create_sandbox_verification','explain':'explain_result'}[a.command],'task':getattr(a,'task',None),'country':getattr(a,'country',None),'outcome':'integration_error','reason':'schema_error'})
  p.error(str(e))
 from .telemetry import observe
 blocked=a.command=='plan' and (a.stage=='production' or result.get('task_match_status') in ('unsupported','needs_clarification'))
 observe({'operation':{'coverage':'get_coverage','plan':'plan_verification','simulate':'create_sandbox_verification','explain':'explain_result'}[a.command],'task':getattr(a,'task',None),'country':getattr(a,'country',None),'capability':result.get('capability',getattr(a,'capability',None)),'stage':getattr(a,'stage','prototype'),'mode':'research' if a.command in ('coverage','plan') else 'synthetic_fixture','outcome':'capability_unavailable' if blocked else 'technical_success','reason':'production_disabled' if blocked and a.stage=='production' else 'unavailable_route' if blocked else 'none'})
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
