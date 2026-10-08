import argparse,json
from . import core

def main():
 p=argparse.ArgumentParser(description='Gridzen research + synthetic sandbox (no real provider calls)');s=p.add_subparsers(dest='command',required=True)
 x=s.add_parser('coverage');x.add_argument('--country');x.add_argument('--capability')
 x=s.add_parser('plan');x.add_argument('--country',required=True);x.add_argument('--event',choices=list(core.EVENTS),default='payout')
 x=s.add_parser('simulate');x.add_argument('--country',required=True);x.add_argument('--capability',required=True);x.add_argument('--scenario',choices=core.SCENARIOS,default='match')
 x=s.add_parser('explain');x.add_argument('reason_code')
 a=p.parse_args()
 try:
  result={'coverage':lambda:core.coverage(a.country,a.capability),'plan':lambda:core.plan(a.country,a.event),'simulate':lambda:core.simulate(a.country,a.capability,a.scenario),'explain':lambda:core.explain(a.reason_code)}[a.command]()
 except ValueError as e:p.error(str(e))
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
