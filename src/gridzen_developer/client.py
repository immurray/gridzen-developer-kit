"""Small synchronous HTTP SDK for the research/sandbox API only."""
import json
from urllib.request import Request,urlopen
from urllib.parse import urlencode,urlsplit,quote

class Gridzen:
 def __init__(self,base_url='https://gridzen.ai/developers/api',timeout=10):
  u=urlsplit(base_url)
  if u.scheme!='https' and not (u.scheme=='http' and u.hostname in ('127.0.0.1','localhost')):raise ValueError('HTTPS required outside localhost')
  if u.username or u.password or u.query or u.fragment:raise ValueError('Invalid base URL')
  self.base_url=base_url.rstrip('/');self.timeout=timeout
 def _call(self,path,payload=None):
  r=Request(self.base_url+path,data=json.dumps(payload).encode() if payload is not None else None,headers={'Content-Type':'application/json','User-Agent':'GridzenDeveloperKit/0.1'})
  with urlopen(r,timeout=self.timeout) as response:return json.load(response)
 def coverage(self,country=None,capability=None):return self._call('/coverage?'+urlencode({k:v for k,v in {'country':country,'capability':capability}.items() if v}))
 def plan(self,country,event='payout'):return self._call('/plan',{'country':country,'event':event})
 def simulate(self,country,capability,scenario='match'):return self._call('/sandbox/verifications',{'country':country,'capability':capability,'scenario':scenario})
 def get_simulation(self,identifier):return self._call('/sandbox/verifications/'+quote(identifier,safe=''))
 def explain(self,reason_code):return self._call('/explain/'+quote(reason_code,safe=''))
