from pathlib import Path
from contextlib import asynccontextmanager
from typing import Literal
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from . import core
from .remote import make_transport, MCPBounds
from .mcp import server as mcp_server

mcp_app=make_transport()
@asynccontextmanager
async def lifespan(_app):
 async with mcp_app.router.lifespan_context(mcp_app):yield

app=FastAPI(title='Gridzen Developer Sandbox',version='0.4.1',lifespan=lifespan,docs_url=None,redoc_url=None,openapi_url='/api/openapi.json',servers=[{'url':'/developers'}])
app.add_middleware(MCPBounds)
class PlanRequest(BaseModel):
 model_config=ConfigDict(extra='forbid',strict=True)
 country: str=Field(min_length=2,max_length=2,pattern=r'^[A-Za-z]{2}$')
 event: Literal['onboarding','payout','account_change']='payout'
class SandboxRequest(BaseModel):
 model_config=ConfigDict(extra='forbid',strict=True)
 country: str=Field(min_length=2,max_length=2,pattern=r'^[A-Za-z]{2}$')
 capability: str=Field(max_length=40)
 scenario: Literal['match','mismatch','not_found','timeout','unsupported']='match'
@app.exception_handler(ValueError)
async def invalid(_r,exc):return JSONResponse({'error':str(exc)},status_code=400)
@app.exception_handler(RequestValidationError)
async def invalid_schema(_r,_exc):return JSONResponse({'error':'INVALID_INPUT','message':'Only documented country, capability, event and synthetic scenario fields are accepted.'},status_code=422)
@app.middleware('http')
async def bounds(request:Request,call_next):
 if request.method=='POST':
  body=await request.body()
  if len(body)>4096:return JSONResponse({'error':'REQUEST_TOO_LARGE'},status_code=413)
 response=await call_next(request)
 response.headers['X-Content-Type-Options']='nosniff'
 response.headers['Referrer-Policy']='no-referrer'
 response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"
 response.headers['Cache-Control']='no-store' if request.url.path.startswith(('/api','/mcp')) else 'public, max-age=60'
 return response
@app.get('/health')
def health():return {'status':'ok','mode':'sandbox','live_routes':0,'version':'0.4.1','mcp_transport':'streamable-http'}
@app.get('/server-card.json')
async def server_card():
 return {'serverInfo':{'name':'Gridzen Verification','version':'0.4.1'},'authentication':{'required':False},'tools':[tool.model_dump(by_alias=True,exclude_none=True) for tool in await mcp_server.list_tools()],'resources':[],'prompts':[]}
@app.get('/api/coverage')
def coverage(country:str|None=Query(None,max_length=2),capability:str|None=Query(None,max_length=40)):return core.coverage(country,capability)
@app.post('/api/plan')
def plan(request:PlanRequest):return core.plan(request.country,request.event)
@app.post('/api/sandbox/verifications')
def simulate(request:SandboxRequest):return core.simulate(request.country,request.capability,request.scenario)
@app.get('/api/sandbox/verifications/{identifier}')
def get_simulation(identifier:str):return core.get_simulation(identifier)
@app.get('/api/explain/{reason_code}')
def explain(reason_code:str):return core.explain(reason_code)
app.router.routes.extend(mcp_app.routes)
app.mount('/',StaticFiles(directory=Path(__file__).parent/'web',html=True),name='developer-web')
