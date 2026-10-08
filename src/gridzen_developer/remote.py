"""Bounded, stateless public MCP transport. No accounts, providers or storage."""
from collections import OrderedDict
from time import monotonic
from starlette.responses import JSONResponse
from mcp.server.transport_security import TransportSecuritySettings
from .mcp import server

def make_transport():
 return server.streamable_http_app(
  streamable_http_path='/mcp',json_response=True,stateless_http=True,
  max_request_body_size=4096,
  transport_security=TransportSecuritySettings(
   allowed_hosts=['gridzen.ai','127.0.0.1:*','localhost:*','testserver'],
   allowed_origins=['https://gridzen.ai','http://127.0.0.1:*','http://localhost:*'],
  ),
 )

class MCPBounds:
 """One process-wide and one per-client fixed window; no payload logging.

 The reverse proxy overwrites X-Real-IP. The service binds to loopback only.
 Buckets are in memory, bounded to 1024 clients, and reset after 60 seconds.
 """
 def __init__(self,app,per_client=120,total=600,clock=monotonic):
  self.app=app;self.per_client=per_client;self.total=total;self.clock=clock
  self.started=clock();self.count=0;self.clients=OrderedDict()

 async def __call__(self,scope,receive,send):
  if scope['type']!='http' or scope['path']!='/mcp':
   return await self.app(scope,receive,send)
  now=self.clock()
  if now-self.started>=60:
   self.started=now;self.count=0;self.clients.clear()
  headers=dict(scope.get('headers',[]))
  client=headers.get(b'x-real-ip',str(scope.get('client',('unknown',))[0]).encode())
  count=self.clients.get(client,0)
  if self.count>=self.total or count>=self.per_client or (client not in self.clients and len(self.clients)>=1024):
   return await JSONResponse({'error':'RATE_LIMITED'},status_code=429,headers={'Retry-After':'60','Cache-Control':'no-store'})(scope,receive,send)
  self.count+=1;self.clients[client]=count+1
  return await self.app(scope,receive,send)
