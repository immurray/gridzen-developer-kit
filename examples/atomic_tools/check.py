"""Offline deterministic examples. No account, telemetry, billing or network."""
from gridzen_developer.atomic import execute
import json
cases={'phone-format':{'phone':'+1 (202) 555-0123'},'clabe-format':{'clabe':'032180000118359719'},'result-explanation':{'status':'timeout'}}
for product,value in cases.items():
    result=execute(product,value)
    assert not result['charged'] and result['network_calls']==0
    print(json.dumps({'product':product,'output':result}))
