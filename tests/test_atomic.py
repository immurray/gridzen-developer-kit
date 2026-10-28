import asyncio,json,os,sys,tomllib
from pathlib import Path
import httpx,pytest
from gridzen_developer.atomic import catalog,execute
from gridzen_developer.setup import setup,CLIENTS
from gridzen_developer.production_mcp import ProductionAPI,make_server,PROFILES
from mcp import Client,StdioServerParameters
from mcp.shared.exceptions import MCPError
from mcp.server.mcpserver.exceptions import ToolError


def test_offline_inputs_and_non_identity_boundaries(monkeypatch):
    def forbidden(*a,**kw):raise AssertionError('network not allowed')
    monkeypatch.setattr(httpx.Client,'request',forbidden)
    monkeypatch.setattr(httpx.AsyncClient,'request',forbidden)
    assert execute('phone-format',{'phone':'+1 (202) 555-0123'})['normalized']=='+12025550123'
    assert execute('clabe-format',{'clabe':'032180000118359719'})['checksum_valid']
    assert not execute('clabe-format',{'clabe':'032180000118359718'})['checksum_valid']
    assert not execute('result-explanation',{'status':'approved'})['automatic_business_approval']
    with pytest.raises(ValueError):execute('phone-format',{'phone':'+12025550123','send_otp':True})
    with pytest.raises(ValueError):execute('mx-cep',{})


@pytest.mark.parametrize('product',[r['id'] for r in catalog()['products']])
def test_each_product_is_independently_installable_for_all_clients(tmp_path,product,monkeypatch):
    monkeypatch.setenv('GRIDZEN_API_KEY','gz_test_PRIVATE_SENTINEL')
    assert setup('all',tmp_path,product=product)['changed_files']>0
    assert list(tmp_path.iterdir())==[]
    summary=setup('all',tmp_path,True,product)
    assert len(summary['clients'])==10 and all(r['skill_count']==1 for r in summary['clients'])
    assert setup('all',tmp_path,True,product)['changed_files']==0
    config=tomllib.loads((tmp_path/'.codex/config.toml').read_text())['mcp_servers']['gridzen-'+product]
    assert config['args']==['-m','gridzen_developer.atomic','--product',product]
    for p in tmp_path.rglob('*'):
        if p.is_file() and p.suffix in ('.json','.toml','.md'):assert 'PRIVATE_SENTINEL' not in p.read_text()


@pytest.mark.parametrize('product',list(PROFILES))
def test_merchant_discovery_filters_without_changing_api_contract(product):
    async def run():
        calls=[]
        def reply(r):calls.append(r);return httpx.Response(200,json={})
        server=make_server(ProductionAPI('gz_test_fixture',httpx.MockTransport(reply)),product)
        assert {t.name for t in await server.list_tools()}==set(PROFILES[product])
        with pytest.raises((MCPError,ToolError,ValueError)):await server.call_tool('enroll_production',{})
        assert not calls
    asyncio.run(run())


def test_real_stdio_local_profiles_and_invalid_extra_arguments():
    async def run():
        for row in catalog()['products']:
            if row['kind']!='local':continue
            async with Client(StdioServerParameters(command=sys.executable,args=['-m','gridzen_developer.atomic','--product',row['id']])) as c:
                tools=await c.list_tools();assert [t.name for t in tools.tools]==row['tools']
                response=await c.call_tool(row['tools'][0],row['sample_input'])
                assert not response.is_error and response.structured_content==execute(row['id'],row['sample_input'])
                try:bad=await c.call_tool(row['tools'][0],{**row['sample_input'],'private':'do-not-accept'})
                except MCPError:pass
                else:assert bad.is_error
    asyncio.run(run())
