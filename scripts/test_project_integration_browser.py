import sys,json
from playwright.sync_api import sync_playwright
base=sys.argv[1] if len(sys.argv)>1 else 'https://gridzen.ai'
checks=[]
def nav_signature(page):
 return page.locator('.site-links a').evaluate_all('(links)=>links.map(a=>[a.textContent,a.getAttribute("href")])')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [360,390,768,1440]:
  page=browser.new_page(viewport={'width':width,'height':900})
  for lang in ['en','es','zh']:
   prefix='' if lang=='en' else '/'+lang
   page.goto(base+prefix+'/');main_nav=nav_signature(page)
   assert len(main_nav)==6
   assert page.locator('.site-links a[href*="skills"]').count()==0
   assert page.locator('.trust-orbit').count()==1,'Homepage animation missing'
   assert page.locator('.trust-orbit').evaluate('(node)=>[...node.querySelectorAll("*")].some(n=>getComputedStyle(n).animationName!=="none")'),'Homepage animation stopped'
   assert page.locator('.developer-entry-card').count()==3
   assert page.locator('.developer-entry-card').first.get_attribute('href')=='/developers/harnesses.html?lang='+lang
   signature=page.locator('.site-nav').evaluate('(node)=>({background:getComputedStyle(node).backgroundColor,border:getComputedStyle(node).borderBottomColor,brand:getComputedStyle(node.querySelector(".brand")).fontFamily})')
   for path in ['','quickstart.html','harnesses.html','privacy.html','support.html','terms.html']:
    errors=[]
    def on_error(error):errors.append(str(error))
    page.on('pageerror',on_error)
    response=page.goto(base+'/developers/'+path+'?lang='+lang)
    assert response.status==200
    page.wait_for_function('()=>window.GridzenShellReady !== undefined')
    assert page.evaluate('window.GridzenShellReady') is True
    assert nav_signature(page)==main_nav,(lang,path,'Different navigation')
    actual=page.locator('.site-nav').evaluate('(node)=>({background:getComputedStyle(node).backgroundColor,border:getComputedStyle(node).borderBottomColor,brand:getComputedStyle(node.querySelector(".brand")).fontFamily})')
    assert actual==signature,(path,'Different shell style')
    assert page.locator('h1').count()==1
    assert page.locator('.site-nav .lang a').all_text_contents()==['EN','ES','中文']
    assert page.locator('.site-nav').bounding_box()['height']<=120,(path,width,'Navigation too tall')
    assert page.evaluate('document.documentElement.scrollWidth-innerWidth')<=2,(path,width,'Overflow')
    assert page.locator('.developer-subnav a').count()==3
    assert page.locator('.foot .foot-links a[href*="skills"]').count()==1
    if path=='' and width==1440:
     page.wait_for_function('()=>document.querySelector("#country").options.length>1')
     assert page.input_value('#country')=='MX'
     for scenario in ['match','mismatch','not_found','timeout','unsupported']:
      page.select_option('#scenario',scenario);page.locator('#run').click()
      page.wait_for_function('(scenario)=>{try{return JSON.parse(document.querySelector("#result").textContent).fixture_outcome===scenario}catch(_){return false}}',arg=scenario)
      value=json.loads(page.locator('#result').text_content())
      assert value['country']=='MX' and value['simulated'] is True and value['verified'] is False and value['provider_calls']==0
      if scenario in ['not_found','timeout','unsupported']:assert value['status']=='inconclusive'
    if path=='harnesses.html':
     page.wait_for_function('()=>document.querySelector("#client").options.length===10')
     for client in ['codex','claude-code','claude-desktop','cursor','vscode','copilot-cli','gemini-cli','cline','roo-code','opencode']:
      page.select_option('#client',client)
      assert client in page.locator('#setup').inner_text()
      assert page.locator('#config').text_content().strip()
      assert page.locator('#client-status').inner_text().strip()
     assert page.locator('#skills a').count()==6
     assert not page.locator('.config-details').get_attribute('open')
    assert not errors,(path,errors)
    page.remove_listener('pageerror',on_error)
    checks.append({'page':path or 'index','language':lang,'width':width,'status':'passed'})
   # Traverse actual project entry points, rather than only testing URLs independently.
   page.goto(base+prefix+'/docs/')
   page.locator('.developer-entry-card').first.click()
   page.wait_for_function('()=>window.GridzenShellReady !== undefined');page.evaluate('window.GridzenShellReady')
   assert page.url.endswith('/developers/harnesses.html?lang='+lang)
   page.locator('.site-links a').first.click()
   assert page.url.endswith(prefix+'/docs/')
   page.goto(base+prefix+'/skills/')
   page.locator('a[href="/developers/harnesses.html?lang='+lang+'"]').first.click()
   page.wait_for_function('()=>window.GridzenShellReady !== undefined');page.evaluate('window.GridzenShellReady')
   page.locator('.foot-links a[href="'+prefix+'/skills/"]').click()
   assert page.url.endswith(prefix+'/skills/')
  page.close()
 browser.close()
print(json.dumps({'base':base,'passed':len(checks),'failed':0,'cross_project_round_trips':24,'synthetic_ui_cases':15,'checks':checks},ensure_ascii=False,indent=2))
