import os,json,mimetypes
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright,expect
local=os.environ.get('GRIDZEN_LOCAL_PREVIEW')=='1'
root=Path(__file__).resolve().parents[1]/'src/gridzen_developer/web'
expected={'en':{'h1':'Build verification','guide':'Your first sandbox','country':'Indonesia','plan':'Research plan','timeout':'provider timeout','error':'Unable to load','copied':'Copied','footer':'Developers'},'zh':{'h1':'为你的下一个产品','guide':'完成第一次沙盒','country':'印度尼西亚','plan':'研究方案','timeout':'供应商超时','error':'结果加载失败','copied':'已复制','footer':'开发者'},'es':{'h1':'Integra la verificación','guide':'Tu primera prueba','country':'Indonesia','plan':'Plan de investigación','timeout':'espera agotada','error':'No se pudieron','copied':'Copiado','footer':'Desarrolladores'}}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox'])
 for lang,text in expected.items():
  ctx=b.new_context(permissions=['clipboard-read','clipboard-write']);page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  if local:
   def serve(route):
    path=urlsplit(route.request.url).path.removeprefix('/developers/')
    f=root/(path or 'index.html')
    if f.is_file():route.fulfill(path=str(f),content_type=mimetypes.guess_type(str(f))[0] or 'application/octet-stream')
    else:route.continue_()
   page.route('https://gridzen.ai/developers/**',serve)
   page.route('**/assets/layout.js*',lambda r:r.fulfill(path=os.environ['GRIDZEN_PREVIEW_LAYOUT'],content_type='application/javascript'))
  page.goto('https://gridzen.ai/developers/',wait_until='networkidle')
  page.locator('.lang button[data-lang="'+lang+'"]').click()
  expect(page.locator('h1')).to_contain_text(text['h1']);expect(page.locator('#country option:checked')).to_contain_text(text['country'])
  expect(page.locator('#status')).to_contain_text(text['plan']);assert page.locator('#country option').count()==198
  page.locator('#country').select_option('NG');page.locator('#scenario').select_option('timeout');page.locator('#run').click()
  expect(page.locator('#summary')).to_contain_text(text['timeout']);raw=json.loads(page.locator('#result').text_content());assert raw['verified'] is False and raw['country']=='NG'
  page.locator('#raw summary').click();page.locator('#copy').click();expect(page.locator('#copy-status')).to_have_text(text['copied'])
  before=page.locator('#result').text_content();page.locator('.lang button[data-lang="en"]').click();page.locator('.lang button[data-lang="'+lang+'"]').click();assert page.locator('#country').input_value()=='NG';assert page.locator('#scenario').input_value()=='timeout';assert before==page.locator('#result').text_content()
  expect(page.locator('footer a[href="/developers/"]')).to_have_text(text['footer'])
  for w in (390,768,1440):
   page.set_viewport_size({'width':w,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(lang,w)
  page.locator('a[href="/developers/quickstart.html"]').click();expect(page.locator('h1')).to_contain_text(text['guide']);page.reload();expect(page.locator('h1')).to_contain_text(text['guide']);assert page.locator('pre').count()==4;assert 'gridzen plan --country ID --event payout' in page.locator('pre').first.text_content()
  page.goto('https://gridzen.ai/developers/',wait_until='networkidle');expect(page.locator('h1')).to_contain_text(text['h1'])
  page.route('**/api/sandbox/verifications',lambda r:r.fulfill(status=503,body='unavailable'));page.locator('#run').click();expect(page.locator('#status')).to_contain_text(text['error'])
  assert not errors,errors
  ctx.close();print('PASS '+lang+': complete page/guide, country labels, dynamic result/error/copy, persistence, stable API JSON, mobile widths')
 b.close()
