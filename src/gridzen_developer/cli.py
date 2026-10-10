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
 a=p.parse_args()
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
 except ValueError as e:p.error(str(e))
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
