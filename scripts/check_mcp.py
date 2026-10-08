"""Actual stdio handshake/tool calls; no network or live provider."""
import asyncio,sys
from mcp import Client,StdioServerParameters
async def main():
 async with Client(StdioServerParameters(command=sys.executable,args=['-m','gridzen_developer.mcp'])) as c:
  tools=await c.list_tools()
  names={t.name for t in tools.tools}
  assert names=={'get_coverage','plan_verification','create_sandbox_verification','get_sandbox_verification','explain_result'},names
  r=await c.call_tool('create_sandbox_verification',{'country':'ID','capability':'bank_account_match','scenario':'timeout'})
  data=r.structured_content
  assert not r.is_error and data['simulated'] and not data['verified'] and data['status']=='inconclusive',r
  r=await c.call_tool('get_sandbox_verification',{'identifier':data['id']})
  assert r.structured_content==data
  p=await c.call_tool('plan_verification',{'country':'ID','event':'payout'})
  assert p.structured_content['execution']['live_available'] is False
  print('PASS actual MCP stdio discovery, sandbox retrieval and plan')
asyncio.run(main())
