"""Run: python examples/payout.py. Sends only synthetic scenario parameters."""
from gridzen_developer.client import Gridzen
api=Gridzen()
plan=api.plan('ID','payout')
assert plan['execution']['live_available'] is False
for scenario in ('match','mismatch','not_found','timeout','unsupported'):
 result=api.simulate('ID','bank_account_match',scenario)
 assert result['simulated'] and not result['verified']
 assert api.get_simulation(result['id'])==result
 print(scenario,result['status'],result['reason_code'])
