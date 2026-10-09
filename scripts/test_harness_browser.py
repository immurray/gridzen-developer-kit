import sys,json
from pathlib import Path
from playwright.sync_api import sync_playwright
base=sys.argv[1] if len(sys.argv)>1 else 'https://gridzen.ai'
checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width in [390,1440]:
  page=browser.new_page(viewport={'width':width,'height':900})
  for lang in ['en','es','zh']:
   for path in ['','quickstart.html','harnesses.html','privacy.html','support.html','terms.html']:
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    response=page.goto(base+'/developers/'+path+'?lang='+lang);page.wait_for_timeout(200)
    assert response.status==200,(path,response.status)
    assert page.locator('h1').count()==1,path
    assert page.locator('#gz-nav .lang a[lang]').all_text_contents()==['EN','ES','中文'],path
    assert page.evaluate('document.documentElement.lang')==('zh-CN' if lang=='zh' else lang),(path,lang)
    assert page.evaluate('document.documentElement.scrollWidth-innerWidth')<=2,(path,width)
    assert not errors,(path,errors)
    for a in page.locator('a[href^="/developers/"]').all():
     href=a.get_attribute('href')
     if '/downloads/' not in href and '/api/' not in href and '.json' not in href:assert 'lang=' in href,(path,href)
    if path=='harnesses.html':
     page.wait_for_selector('#client option',state='attached')
     assert page.locator('#client option').count()==10
     for client in ['codex','claude-desktop','cline','roo-code','gemini-cli','vscode','opencode']:
      page.select_option('#client',client);assert client in page.locator('#setup').inner_text()
      assert page.locator('#config').text_content().strip()
     assert page.locator('#skills a').count()==6
    checks.append({'page':path or 'index','language':lang,'width':width,'status':'passed'})
  page.close()
 browser.close()
print(json.dumps({'base':base,'passed':len(checks),'failed':0,'checks':checks},ensure_ascii=False,indent=2))
