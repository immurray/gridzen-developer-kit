import argparse,json
from . import core

def main():
 p=argparse.ArgumentParser(description='Gridzen research + synthetic sandbox (no real provider calls)');s=p.add_subparsers(dest='command',required=True)
 x=s.add_parser('coverage');x.add_argument('--country');x.add_argument('--capability')
 x=s.add_parser('plan');x.add_argument('--country',required=True);x.add_argument('--event',choices=list(core.EVENTS),default='payout')
 x=s.add_parser('simulate');x.add_argument('--country',required=True);x.add_argument('--capability',required=True);x.add_argument('--scenario',choices=core.SCENARIOS,default='match')
 x=s.add_parser('explain');x.add_argument('reason_code')
 s.add_parser('skills',help='List bundled Skill directories; copy a complete directory into your assistant to activate it')
 from .setup import CLIENTS
 x=s.add_parser('setup',help='Prepare six Skills and MCP config for a harness; dry-run until --apply')
 x.add_argument('--client',choices=['all',*CLIENTS],required=True);x.add_argument('--project',default='.');x.add_argument('--apply',action='store_true')
 a=p.parse_args()
 if a.command=='setup':
  from .setup import setup
  try: result=setup(a.client,a.project,a.apply)
  except (ValueError,OSError) as exc:p.error(str(exc))
  print(json.dumps(result,ensure_ascii=False,indent=2));return
 if a.command=='skills':
  from .skills import list_skills
  print(json.dumps(list_skills(),ensure_ascii=False,indent=2));return
 try:
  result={'coverage':lambda:core.coverage(a.country,a.capability),'plan':lambda:core.plan(a.country,a.event),'simulate':lambda:core.simulate(a.country,a.capability,a.scenario),'explain':lambda:core.explain(a.reason_code)}[a.command]()
 except ValueError as e:p.error(str(e))
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
