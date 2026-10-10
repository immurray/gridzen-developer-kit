"""Fixed-category product evidence; no personal fields, raw bodies or user tracking.

Request counters are technical evidence. Voluntary summaries are unverified
reports, never authenticated customer outcomes. Local tools never call this DB.
"""
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from uuid import UUID

TASKS = frozenset(('signup_phone','identity_onboarding','payout_account','phone_possession','account_change','business_onboarding','select_method','diagnose_failure','provider_intake','payout_policy','mexico_pilot','other','unknown'))
CAPABILITIES = frozenset(('official_identity','commercial_identity','consented_eid','bank_account_match','consented_bank','cardholder_name','phone_identity','phone_intelligence','identity_verification','otp','business_kyb','batch','webhook_recovery','policy_design','provider_rights','other','unknown'))
SKILLS = frozenset(('gridzen-select-verification','gridzen-integrate-sandbox','gridzen-explain-verification','provider-rights-readiness','payout-policy-designer','mexico-pilot-scoper','unknown'))
OPERATIONS = frozenset(('get_coverage','plan_verification','create_sandbox_verification','get_sandbox_verification','explain_result','merchant_create','merchant_read','merchant_simulate','merchant_refresh','merchant_capabilities','task_summary','transport_rejected','other'))
SOURCES = frozenset(('internal_test','self_reported_test','unknown','authenticated_merchant_sandbox','self_reported_feedback','authenticated_feedback'))
MODES = frozenset(('research','synthetic_fixture','merchant_sandbox','local_draft','unknown'))
OUTCOMES = frozenset(('technical_success','integration_error','capability_unavailable','completed_prototype','blocked','abandoned','unknown'))
REASONS = frozenset(('none','auth_error','schema_error','rate_limit','timeout','transport_error','tool_error','unknown_country','unknown_capability','unavailable_route','coverage_gap','missing_workflow_step','price_unknown','production_disabled','already_solved_elsewhere','idempotency_conflict','record_not_found','other','unknown'))
STAGES = frozenset(('research','prototype','production','unknown'))
FIELDS = ('operation','task','capability','country','source','mode','outcome','reason','skill','stage')
VOCABULARIES = dict(operation=OPERATIONS,task=TASKS,capability=CAPABILITIES,source=SOURCES,mode=MODES,outcome=OUTCOMES,reason=REASONS,skill=SKILLS,stage=STAGES)


def category(value, allowed, default='unknown'):
    return value if isinstance(value,str) and value in allowed else default


def country_bucket(value):
    # Keep an ISO-like coarse country label, not arbitrary supplied strings.
    return value.upper() if isinstance(value,str) and re.fullmatch('[A-Za-z]{2}',value) else 'unknown'


def safe_dimensions(values):
    return {key:country_bucket(values.get(key)) if key=='country' else category(values.get(key),VOCABULARIES[key], 'other' if key=='operation' else 'unknown') for key in FIELDS}


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS product_events (day TEXT NOT NULL, operation TEXT NOT NULL, task TEXT NOT NULL, capability TEXT NOT NULL, country TEXT NOT NULL, source TEXT NOT NULL, mode TEXT NOT NULL, outcome TEXT NOT NULL, reason TEXT NOT NULL, skill TEXT NOT NULL, stage TEXT NOT NULL, count INTEGER NOT NULL, PRIMARY KEY(day,operation,task,capability,country,source,mode,outcome,reason,skill,stage))')
    db.execute('CREATE TABLE IF NOT EXISTS feedback_receipts (day TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY(day,hash))')
    db.execute('CREATE INDEX IF NOT EXISTS product_events_day ON product_events(day)')


def write(path, values, receipt=None, day=None):
    if not path: return False
    day=day or datetime.now(timezone.utc).date();safe=safe_dimensions(values)
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(path,timeout=2) as db:
        ensure(db);db.execute('BEGIN IMMEDIATE')
        db.execute('DELETE FROM product_events WHERE day<?',((day-timedelta(days=89)).isoformat(),))
        db.execute('DELETE FROM feedback_receipts WHERE day<?',((day-timedelta(days=29)).isoformat(),))
        total=db.execute('SELECT COALESCE(SUM(count),0) FROM product_events WHERE day=?',(day.isoformat(),)).fetchone()[0]
        if total>=10000:return False
        if receipt:
            feedback=db.execute("SELECT COALESCE(SUM(count),0) FROM product_events WHERE day=? AND operation='task_summary'",(day.isoformat(),)).fetchone()[0]
            if feedback>=500:return False
            digest=hashlib.sha256(receipt.encode()).hexdigest()
            if db.execute('SELECT 1 FROM feedback_receipts WHERE day=? AND hash=?',(day.isoformat(),digest)).fetchone():return True
            db.execute('INSERT INTO feedback_receipts VALUES (?,?)',(day.isoformat(),digest))
        columns='day,'+','.join(FIELDS)
        values=(day.isoformat(),*(safe[key] for key in FIELDS))
        db.execute('INSERT INTO product_events ('+columns+',count) VALUES ('+','.join('?' for _ in values)+',1) ON CONFLICT('+columns+') DO UPDATE SET count=count+1',values)
    return True


def record_safe(path, values):
    try:return write(path,values)
    except (OSError,sqlite3.Error,ValueError):return False


def validate_summary(value, require_consent=False):
    keys={'schema_version','summary_id','task','country','requested_capability','stage','outcome','blocker','skill','consent_to_share'}
    if not isinstance(value,dict) or set(value)!=keys or type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('INVALID_FEEDBACK')
    if type(value.get('consent_to_share')) is not bool or (require_consent and not value['consent_to_share']):raise ValueError('SHARING_REQUIRES_EXPLICIT_CONSENT')
    identifier=value.get('summary_id')
    if not isinstance(identifier,str) or len(identifier)!=36:raise ValueError('INVALID_FEEDBACK')
    try:UUID(identifier)
    except ValueError:raise ValueError('INVALID_FEEDBACK') from None
    for key,allowed in [('task',TASKS),('requested_capability',CAPABILITIES),('stage',STAGES),('outcome',OUTCOMES-{'technical_success','integration_error'}),('blocker',REASONS),('skill',SKILLS)]:
        if not isinstance(value.get(key),str) or value[key] not in allowed:raise ValueError('INVALID_FEEDBACK')
    if value.get('country')!='unknown' and (not isinstance(value.get('country'),str) or not re.fullmatch('[A-Z]{2}',value['country'])):raise ValueError('INVALID_FEEDBACK')
    # No authenticated/live completion field exists in this public report contract.
    return dict(value)


def accept_summary(path, value, source='self_reported_feedback'):
    value=validate_summary(value,True)
    source=source if source in ('authenticated_feedback','internal_test','self_reported_test') else 'self_reported_feedback'
    return write(path,{'operation':'task_summary','task':value['task'],'capability':value['requested_capability'],'country':value['country'],'source':source,'mode':'local_draft','outcome':value['outcome'],'reason':value['blocker'],'skill':value['skill'],'stage':value['stage']},receipt=value['summary_id'])


def http_reason(status):
    return {400:'schema_error',401:'auth_error',403:'auth_error',404:'record_not_found',409:'idempotency_conflict',413:'schema_error',422:'schema_error',429:'rate_limit',502:'unavailable_route',503:'unavailable_route',504:'timeout'}.get(status,'tool_error' if status>=400 else 'none')
