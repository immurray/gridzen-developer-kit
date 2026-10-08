"""Actual MCP client acceptance over HTTP. Synthetic values only."""
import asyncio,sys
from mcp import Client

async def main(url):
 async with Client(url) as client:
  response=await client.list_tools()
  assert len(response.tools)==5
  assert all(t.input_schema.get('additionalProperties') is False for t in response.tools)
  for scenario in ('match','mismatch','not_found','timeout','unsupported'):
   result=await client.call_tool('create_sandbox_verification',{'country':'ID','capability':'bank_account_match','scenario':scenario})
   data=result.structured_content
   assert not result.is_error and data['simulated'] and data['verified'] is False and data['provider_calls']==0
   if scenario in ('not_found','timeout','unsupported'):assert data['status']=='inconclusive'
   stored=await client.call_tool('get_sandbox_verification',{'identifier':data['id']})
   assert stored.structured_content==data
  plan=await client.call_tool('plan_verification',{'country':'ID','event':'payout'})
  assert plan.structured_content['execution']['live_available'] is False
  print('PASS remote MCP: discovery, five outcomes, retrieval and plan; zero live checks')
asyncio.run(main(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8030/mcp'))
