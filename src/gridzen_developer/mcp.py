"""Local, offline MCP: no credentials, no external calls, no real verification."""
from typing import Any
from inspect import signature
from mcp.server import MCPServer
from mcp.shared.exceptions import MCPError
from mcp.types import ToolAnnotations
from . import core

async def strict_arguments(ctx, call_next):
 """Reject unknown/personal fields before SDK coercion; never echo their values."""
 if ctx.method == 'tools/call' and isinstance(ctx.params, dict):
  name=ctx.params.get('name'); arguments=ctx.params.get('arguments', {})
  fn=TOOLS.get(name) if isinstance(name,str) else None
  if fn:
   allowed=signature(fn).parameters
   if not isinstance(arguments,dict) or set(arguments)-set(allowed):
    raise MCPError(code=-32602,message='Only documented sandbox/research arguments are accepted; do not send personal data.')
   for key,value in arguments.items():
    if value is None and allowed[key].default is None:continue
    if not isinstance(value,str) or len(value)>160:
     raise MCPError(code=-32602,message='Invalid argument type or length.')
 return await call_next(ctx)

class GridzenMCP(MCPServer):
 async def list_tools(self):
  tools=await super().list_tools()
  for tool in tools:tool.input_schema['additionalProperties']=False
  return tools

server=GridzenMCP('Gridzen Developer Kit',version='0.6.0',website_url='https://gridzen.ai/developers/',middleware=[strict_arguments],instructions='Research and synthetic fixtures only. No live providers are enabled. Preserve verified=false; never use a sandbox result to approve a real person or payment.')
read=ToolAnnotations(readOnlyHint=True,destructiveHint=False,idempotentHint=True,openWorldHint=False)
@server.tool(annotations=read,structured_output=True)
def get_coverage(country: str | None=None, capability: str | None=None) -> dict[str, Any]:
 """List country research or inspect one ISO-2 country's capability/access evidence; not live coverage."""
 return core.coverage(country,capability)
@server.tool(annotations=read,structured_output=True)
def plan_verification(country: str, event: str='payout', task: str | None=None, stage: str='prototype') -> dict[str, Any]:
 """Plan a specific signup_phone, identity_onboarding or payout_account task. Set stage=production to report missing live routes; legacy event-only calls remain supported."""
 return core.plan(country,event,task,stage)
@server.tool(annotations=read,structured_output=True)
def create_sandbox_verification(country: str, capability: str, scenario: str='match') -> dict[str, Any]:
 """Return a synthetic match/mismatch/not_found/timeout/unsupported fixture. Never provide personal data."""
 return core.simulate(country,capability,scenario)
@server.tool(annotations=read,structured_output=True)
def get_sandbox_verification(identifier: str) -> dict[str, Any]:
 """Retrieve a deterministic sim_v1 fixture, not a real transaction."""
 return core.get_simulation(identifier)
@server.tool(annotations=read,structured_output=True)
def explain_result(reason_code: str) -> dict[str, Any]:
 """Explain a sandbox reason code; missing data and timeout remain inconclusive."""
 return core.explain(reason_code)
TOOLS={fn.__name__:fn for fn in (get_coverage,plan_verification,create_sandbox_verification,get_sandbox_verification,explain_result)}
async def local_feedback(ctx, call_next):
 from .telemetry import observe
 import asyncio
 params=ctx.params if isinstance(ctx.params,dict) else {}
 args=params.get('arguments') if isinstance(params.get('arguments'),dict) else {}
 dims={'operation':params.get('name'),'task':args.get('task'),'country':args.get('country'),'capability':args.get('capability'),'stage':args.get('stage','prototype'),'mode':'research' if params.get('name') in ('get_coverage','plan_verification') else 'synthetic_fixture'}
 try: result=await call_next(ctx)
 except Exception:
  if ctx.method=='tools/call':await asyncio.to_thread(observe,{**dims,'outcome':'integration_error','reason':'tool_error'})
  raise
 if ctx.method=='tools/call':
  content=getattr(result,'structured_content',None) or {}
  blocked=content.get('requested_stage')=='production' or content.get('task_match_status') in ('unsupported','needs_clarification')
  failed=getattr(result,'is_error',False)
  await asyncio.to_thread(observe,{**dims,'capability':content.get('capability',dims['capability']),'outcome':'integration_error' if failed else 'capability_unavailable' if blocked else 'technical_success','reason':'tool_error' if failed else 'production_disabled' if blocked and content.get('requested_stage')=='production' else 'unavailable_route' if blocked else 'none'})
 return result

def main():
 from .telemetry import enabled
 if enabled():
  read.open_world_hint=True
 server.middleware.insert(0,local_feedback)
 server.run(transport='stdio')
if __name__=='__main__':main()
