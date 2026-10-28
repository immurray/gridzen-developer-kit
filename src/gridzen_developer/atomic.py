"""Inspectable product catalog and offline utilities. Never sends live requests."""
import json
from pathlib import Path
from .atomic_tools import LOCAL_TOOLS


def catalog(product=None):
    data=json.loads((Path(__file__).parent/'data/atomic-products.json').read_text())
    if product is None:return data
    for row in data['products']:
        if row['id']==product:return row
    raise ValueError('UNKNOWN_PRODUCT')


def execute(product, value):
    row=catalog(product)
    if product not in LOCAL_TOOLS:
        raise ValueError('MERCHANT_MCP_AND_EXPLICIT_AUTHORIZATION_REQUIRED')
    if not isinstance(value,dict):raise ValueError('JSON_OBJECT_REQUIRED')
    expected=set(row['sample_input'])
    if set(value)!=expected:raise ValueError('ONLY_DOCUMENTED_FIELDS_ALLOWED')
    return LOCAL_TOOLS[product](**value)


def main_mcp():
    import argparse,os
    parser=argparse.ArgumentParser(description='One product profile. Local utilities never use the network; merchant profiles require separate authorization.')
    parser.add_argument('--product',required=True,choices=[r['id'] for r in catalog()['products']])
    args=parser.parse_args();run_mcp(args.product)


def run_mcp(product):
    import os
    row=catalog(product)
    if row['kind']=='merchant':
        from .production_mcp import ProductionAPI,make_server
        try:api=ProductionAPI(os.environ.get('GRIDZEN_API_KEY',''),project_id=os.environ.get('GRIDZEN_PROJECT_ID') or None)
        except ValueError:raise SystemExit('Set your merchant GRIDZEN_API_KEY in the local environment. Never paste it into chat; product enrollment and funding are separate.') from None
        server=make_server(api,product)
    else:
        from mcp.server import MCPServer
        from mcp.types import ToolAnnotations
        from mcp.shared.exceptions import MCPError
        from inspect import signature
        fn=LOCAL_TOOLS[product]
        async def strict(ctx,next_call):
            if ctx.method=='tools/call' and isinstance(ctx.params,dict):
                values=ctx.params.get('arguments',{})
                if not isinstance(values,dict) or set(values)!=set(signature(fn).parameters) or any(type(v) is not str or len(v)>100 for v in values.values()):
                    raise MCPError(code=-32602,message='Only documented, bounded string fields are accepted.')
            return await next_call(ctx)
        server=MCPServer('GridZen '+product,version='0.7.0',middleware=[strict],instructions=row['boundary'])
        server.tool(annotations=ToolAnnotations(readOnlyHint=True,destructiveHint=False,idempotentHint=True,openWorldHint=False),structured_output=True)(fn)
    server.run(transport='stdio')


if __name__=='__main__':main_mcp()
