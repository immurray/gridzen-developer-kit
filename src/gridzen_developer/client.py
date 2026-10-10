"""Small synchronous HTTP SDK for the research/sandbox API only."""
import json
from urllib.error import HTTPError, URLError
from .product_feedback import http_reason
from urllib.request import Request,urlopen
from urllib.parse import urlencode,urlsplit,quote

class GridzenError(RuntimeError):
 def __init__(self,reason,status=None):
  self.reason=reason;self.http_status=status;self.retryable=reason in ('timeout','transport_error','rate_limit','unavailable_route')
  super().__init__('Gridzen integration error: '+reason)

class Gridzen:
 def __init__(self,base_url='https://gridzen.ai/developers/api',timeout=10):
  u=urlsplit(base_url)
  if u.scheme!='https' and not (u.scheme=='http' and u.hostname in ('127.0.0.1','localhost')):raise ValueError('HTTPS required outside localhost')
  if u.username or u.password or u.query or u.fragment:raise ValueError('Invalid base URL')
  self.base_url=base_url.rstrip('/');self.timeout=timeout
 def _call(self,path,payload=None):
  r=Request(self.base_url+path,data=json.dumps(payload).encode() if payload is not None else None,headers={'Content-Type':'application/json','User-Agent':'GridzenDeveloperKit/0.1'})
  try:
   with urlopen(r,timeout=self.timeout) as response:return json.load(response)
  except HTTPError as exc:raise GridzenError(http_reason(exc.code),exc.code) from None
  except (TimeoutError,URLError):raise GridzenError('transport_error') from None
  except (ValueError,UnicodeError):raise GridzenError('schema_error') from None
 def share_feedback(self,summary):
  from .product_feedback import validate_summary
  return self._call('/feedback',validate_summary(summary,True))
 def coverage(self,country=None,capability=None):return self._call('/coverage?'+urlencode({k:v for k,v in {'country':country,'capability':capability}.items() if v}))
 def plan(self,country,event='payout',task=None,stage='prototype'):return self._call('/plan',{'country':country,'event':event,**({'task':task,'stage':stage} if task is not None or stage!='prototype' else {})})
 def simulate(self,country,capability,scenario='match'):return self._call('/sandbox/verifications',{'country':country,'capability':capability,'scenario':scenario})
 def get_simulation(self,identifier):return self._call('/sandbox/verifications/'+quote(identifier,safe=''))
 def explain(self,reason_code):return self._call('/explain/'+quote(reason_code,safe=''))
