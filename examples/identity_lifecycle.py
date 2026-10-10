"""Caller-owned local identity lifecycle prototype, not a provider integration.
Actual hosted sessions and signed webhook processing remain deployment work.
"""
import json


def apply(state,event,seen):
    identifier,status=event
    if identifier in seen:return state
    seen.add(identifier)
    if state in ('expired','abandoned'):return state
    return {'pending':'pending','review':'review','completed':'completed_prototype','expired':'expired','abandoned':'abandoned'}.get(status,state)


if __name__=='__main__':
    cases=[]
    for status in ('pending','review','completed','expired','abandoned'):
        seen=set();event=('synthetic-event',status)
        state=apply('pending',event,seen)
        assert apply(state,event,seen)==state
        cases.append(dict(event=status,state=state,duplicate_ignored=True,real_person_verified=False))
    print(json.dumps({'mode':'local_prototype','hosted_session_created':False,'webhook_signature_verified':False,'cases':cases},indent=2))
