from pathlib import Path
import json, os, sqlite3
from .product_feedback import record_safe, http_reason, accept_summary
from .usage import CALL_SOURCE
from contextlib import asynccontextmanager
from typing import Literal
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from . import core
from .remote import make_transport, MCPBounds, CallSourceMiddleware
from .mcp import server as mcp_server

mcp_app=make_transport()
@asynccontextmanager
async def lifespan(_app):
 async with mcp_app.router.lifespan_context(mcp_app):yield

app=FastAPI(title='Gridzen Developer Sandbox',version='0.6.0',lifespan=lifespan,docs_url=None,redoc_url=None,openapi_url='/api/openapi.json',servers=[{'url':'/developers'}])
app.add_middleware(MCPBounds)
app.add_middleware(CallSourceMiddleware)
class PlanRequest(BaseModel):
 model_config=ConfigDict(extra='forbid',strict=True)
 country: str=Field(min_length=2,max_length=2,pattern=r'^[A-Za-z]{2}$')
 event: Literal['onboarding','payout','account_change']='payout'
 task: Literal['signup_phone','identity_onboarding','payout_account','phone_possession','business_onboarding','account_change'] | None=None
 stage: Literal['research','prototype','production']='prototype'
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
  if len(body)>4096:
   record_safe(os.environ.get('GRIDZEN_MCP_EVENTS_DB'),{'operation':'transport_rejected','source':'self_reported_test' if request.headers.get('x-gridzen-purpose')=='internal_test' else 'unknown','outcome':'integration_error','reason':'schema_error'})
   return JSONResponse({'error':'REQUEST_TOO_LARGE'},status_code=413)
 dimensions=None
 operations={'/api/plan':'plan_verification','/api/coverage':'get_coverage','/api/sandbox/verifications':'create_sandbox_verification'}
 operation=operations.get(request.url.path)
 if request.url.path.startswith('/api/sandbox/verifications/'):operation='get_sandbox_verification'
 if request.url.path.startswith('/api/explain/'):operation='explain_result'
 if operation:
  try: arguments=json.loads(body) if request.method=='POST' else dict(request.query_params)
  except (ValueError,TypeError):arguments={}
  if not isinstance(arguments,dict):arguments={}
  dimensions={'operation':operation,'task':arguments.get('task'),'capability':arguments.get('capability'),'country':arguments.get('country'),'stage':arguments.get('stage','prototype'),'source':'self_reported_test' if request.headers.get('x-gridzen-purpose')=='internal_test' else 'unknown','mode':'research' if operation in ('plan_verification','get_coverage') else 'synthetic_fixture'}
 try:response=await call_next(request)
 except Exception:
  if dimensions:record_safe(os.environ.get('GRIDZEN_MCP_EVENTS_DB'),{**dimensions,'outcome':'integration_error','reason':'tool_error'})
  raise
 if dimensions:
  if operation=='plan_verification' and arguments.get('task') in core.TASK_ROUTES:dimensions['capability']=core.TASK_ROUTES[arguments['task']][1]
  blocked=request.url.path=='/api/plan' and response.status_code<400 and (arguments.get('stage')=='production' or arguments.get('task') in ('phone_possession','business_onboarding','account_change'))
  record_safe(os.environ.get('GRIDZEN_MCP_EVENTS_DB'),{**dimensions,'outcome':'integration_error' if response.status_code>=400 else 'capability_unavailable' if blocked else 'technical_success','reason':http_reason(response.status_code) if response.status_code>=400 else 'production_disabled' if blocked and arguments.get('stage')=='production' else 'unavailable_route' if blocked else 'none'})
 response.headers['X-Content-Type-Options']='nosniff'
 response.headers['Referrer-Policy']='no-referrer'
 response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'"
 response.headers['Cache-Control']='no-store' if request.url.path.startswith(('/api','/mcp')) else 'public, max-age=60'
 return response
@app.get('/health')
def health():return {'status':'ok','mode':'sandbox','live_routes':0,'version':'0.6.0','mcp_transport':'streamable-http'}
@app.get('/server-card.json')
async def server_card():
 return {'serverInfo':{'name':'Gridzen Verification','version':'0.6.0'},'authentication':{'required':False},'tools':[tool.model_dump(by_alias=True,exclude_none=True) for tool in await mcp_server.list_tools()],'resources':[],'prompts':[]}
@app.get('/api/coverage')
def coverage(country:str|None=Query(None,max_length=2),capability:str|None=Query(None,max_length=40)):return core.coverage(country,capability)
@app.post('/api/plan')
def plan(request:PlanRequest):return core.plan(request.country,request.event,request.task,request.stage)
@app.post('/api/sandbox/verifications')
def simulate(request:SandboxRequest):return core.simulate(request.country,request.capability,request.scenario)
@app.get('/api/sandbox/verifications/{identifier}')
def get_simulation(identifier:str):return core.get_simulation(identifier)
@app.get('/api/explain/{reason_code}')
def explain(reason_code:str):return core.explain(reason_code)
@app.post('/api/feedback')
async def feedback(request:Request):
 try:
  value=json.loads(await request.body())
  source=CALL_SOURCE.get()
  accepted=accept_summary(os.environ.get('GRIDZEN_MCP_EVENTS_DB'),value,source if source in ('internal_test','self_reported_test') else 'self_reported_feedback')
 except ValueError:
  return JSONResponse({'error':'INVALID_FEEDBACK','message':'Only fixed categories and explicit consent are accepted; never submit personal fields.'},status_code=422)
 except (OSError, sqlite3.Error):
  accepted=False
 if not accepted:return JSONResponse({'error':'FEEDBACK_TEMPORARILY_UNAVAILABLE'},status_code=503)
 return {'accepted':True,'evidence':'self_reported','authenticated_customer':False,'retention':'aggregate 90 days; receipt hash 30 days','duplicate_receipts':'deduplicated within UTC day'}

@app.post('/api/usage-events')
async def local_usage(request:Request):
 from .product_feedback import accept_usage
 try: accepted=accept_usage(os.environ.get('GRIDZEN_MCP_EVENTS_DB'),json.loads(await request.body()))
 except ValueError: return JSONResponse({'error':'INVALID_USAGE_EVENT'},status_code=422)
 except (OSError,sqlite3.Error): accepted=False
 if not accepted: return JSONResponse({'error':'USAGE_TEMPORARILY_UNAVAILABLE'},status_code=503)
 return {'accepted':True,'evidence':'self_reported_local_usage','authenticated_customer':False}

app.router.routes.extend(mcp_app.routes)
app.mount('/',StaticFiles(directory=Path(__file__).parent/'web',html=True),name='developer-web')
