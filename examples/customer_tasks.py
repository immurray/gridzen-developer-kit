"""Offline acceptance for two priority tasks; no credentials or network."""
import json
from gridzen_developer import core


def evaluate(task,country='US'):
    plan=core.plan(country,'onboarding',task)
    capability=plan['capability']
    rows=[]
    for scenario in core.SCENARIOS:
        result=core.simulate(country,capability,scenario)
        action='retry_bounded' if scenario=='timeout' else 'manual_review' if scenario in ('mismatch','not_found','unsupported') else 'prototype_only'
        rows.append({'scenario':scenario,'action':action,'reason_code':result['reason_code'],'real_access_granted':False})
    return {'task':task,'capability':capability,'mode':'offline_fixture','cases':rows,'production_blockers':core.plan(country,'onboarding',task,'production')['execution']['blockers'],'remaining_work':plan['workflow_requirements']}


if __name__=='__main__':print(json.dumps([evaluate(task) for task in ('signup_phone','identity_onboarding')],indent=2))
