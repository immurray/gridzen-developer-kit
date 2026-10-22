from gridzen_developer import core
from gridzen_developer.server import PlanRequest
from pydantic import ValidationError
import pytest

def test_cep_discovery_does_not_enable_public_execution():
    r=core.plan('MX','payout','mx_cep_existing_payment','production')
    assert r['task_match_status']=='matched'
    assert r['provider_calls']==0 and r['verified'] is False
    assert r['execution']['live_available'] is False
    assert r['merchant_surface']['availability_must_be_checked']
    assert not r['merchant_surface']['creates_transfer']
    assert core.plan('US','payout','mx_cep_existing_payment')['task_match_status']=='unsupported'
    with pytest.raises(ValueError):core.plan('MX','onboarding','mx_cep_existing_payment')

def test_public_cep_plan_rejects_personal_fields():
    with pytest.raises(ValidationError):PlanRequest(country='MX',event='payout',task='mx_cep_existing_payment',account='private-account')
