#!/usr/bin/env python3
"""Offline CEP client-state example. No key, personal data or network required."""
import json

TERMINAL={'verified','review','not_found','blocked','expired','failed'}


def next_action(record):
    state=record.get('status');result=record.get('result') or {}
    if state in {'queued','running','pending'}:return 'poll_same_task_with_limit'
    if state=='verified':
        bindings=result.get('transaction_binding') or {}
        if (result.get('signature_status')=='valid' and result.get('transaction_verified') is True
                and bindings and all(v is True for v in bindings.values())):
            return 'review_name_difference' if result.get('bank_name_match')=='mismatch' else 'store_evidence_and_apply_own_rules'
        return 'manual_review_do_not_release_funds'
    if state=='not_found':return 'check_inputs_or_evidence_generation_not_fraud'
    if state in TERMINAL:return 'manual_review_do_not_release_funds'
    return 'unknown_preserve_task_do_not_resubmit'


def bounded_poll(read,task_id,max_reads=12):
    if type(max_reads) is not int or not 1<=max_reads<=48:raise ValueError('POLL_LIMIT_REQUIRED')
    for _ in range(max_reads):
        record=read(task_id)
        action=next_action(record)
        if action!='poll_same_task_with_limit':return {'mode':'synthetic','verified':False,'record':record,'next_action':action}
    return {'mode':'synthetic','verified':False,'record':record,'next_action':'polling_limit_reached_keep_task_for_later'}


def self_test():
    good={'status':'verified','result':{'signature_status':'valid','transaction_verified':True,'transaction_binding':{'amount':True,'tracking_key':True},'bank_name_match':'matched'}}
    assert next_action(good)=='store_evidence_and_apply_own_rules'
    mismatch=json.loads(json.dumps(good));mismatch['result']['bank_name_match']='mismatch'
    assert next_action(mismatch)=='review_name_difference'
    assert next_action({'status':'review','reason':'CEP_INTERACTIVE_ACCESS_REQUIRED'})=='manual_review_do_not_release_funds'
    assert next_action({'status':'not_found'})=='check_inputs_or_evidence_generation_not_fraud'
    assert next_action({'status':'unexpected'})=='unknown_preserve_task_do_not_resubmit'
    seen=[]
    def waiting(task):seen.append(task);return {'status':'queued'}
    assert bounded_poll(waiting,'synthetic-task',3)['next_action']=='polling_limit_reached_keep_task_for_later'
    assert seen==['synthetic-task']*3
    assert bounded_poll(lambda _:good,'synthetic-task')['verified'] is False
    print(json.dumps({'synthetic_cases':7,'passed':True,'provider_calls':0,'payment_calls':0}))


if __name__=='__main__':self_test()
