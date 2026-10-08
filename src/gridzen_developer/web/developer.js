(()=>{
 'use strict';
 const $=id=>document.getElementById(id),api='/developers/api',L=window.GridzenLanguage;
 const caps={payout:'bank_account_match',onboarding:'commercial_identity',account_change:'phone_identity'};
 let result=null,countries=[],kind=null,pending=false,failed=false,copyKey='',sequence=0;
 const node=(tag,text)=>{const n=document.createElement(tag);n.textContent=text;return n};
 function countriesView(){if(!countries.length)return;const selected=$('country').value||'ID';$('country').replaceChildren();const rows=[...countries].sort((a,b)=>L.region(a.code).localeCompare(L.region(b.code),L.lang()));for(const c of rows){const option=node('option',c.code+' · '+L.region(c.code));option.value=c.code;$('country').append(option)}$('country').value=selected;}
 function line(label,value){const row=node('dl','');row.className='result-line';row.append(node('dt',label),node('dd',value));$('summary').append(row)}
 function render(){
  $('sources').replaceChildren();$('summary').replaceChildren();$('copy-status').textContent=copyKey?L.t(copyKey):'';
  $('status').textContent=L.t(pending?'dev.loading':failed?'dev.error':!result?'dev.choose':kind==='plan'?'dev.plan-status':'dev.sim-status',result?{scenario:L.t('dev.'+result.fixture_outcome)}:{});
  if(!result){$('result').textContent=L.t(failed?'dev.no-result':'dev.no-provider');return}
  $('result').textContent=JSON.stringify(result,null,2);
  line(L.t('dev.country'),L.region(result.country)+' · '+result.country);
  line(L.t('dev.capability'),L.t('cap.'+result.capability));
  if(kind==='plan'){
   line(L.t('dev.date'),result.research_date);
   line(L.t('dev.evidence'),L.t(result.evidence_status==='RESEARCH_EVIDENCE'?'dev.found':'dev.unconfirmed'));
   line(L.t('dev.next'),L.t('dev.plan-next'));
   for(const service of result.services||[]){const details=node('details',''),heading=node('summary',L.t('dev.source-note'));details.append(heading,node('p',service.name));for(const url of service.source_urls){let u;try{u=new URL(url)}catch{continue}if(u.protocol!=='https:'||u.username||u.password)continue;const link=node('a',L.t('dev.source')+' · '+u.hostname);link.href=u.href;link.target='_blank';link.rel='noopener noreferrer';const p=node('p','');p.append(link);details.append(p)}$('sources').append(details)}
  }else{
   line(L.t('dev.outcome'),L.t('meaning.'+result.fixture_outcome));
   line(L.t('dev.next'),L.t('next.'+result.fixture_outcome));
   $('summary').append(node('p',L.t('dev.sim-note')));
  }
 }
 async function request(path,payload){const r=await fetch(api+path,{method:payload?'POST':'GET',headers:{'Content-Type':'application/json'},body:payload?JSON.stringify(payload):undefined,signal:AbortSignal.timeout(12000)});if(!r.ok)throw Error('request failed');return r.json()}
 async function act(action){const current=++sequence;kind=action;pending=true;failed=false;result=null;copyKey='';$('plan').disabled=$('run').disabled=true;render();try{const data=action==='plan'?await request('/plan',{country:$('country').value,event:$('event').value}):await request('/sandbox/verifications',{country:$('country').value,capability:caps[$('event').value],scenario:$('scenario').value});if(current!==sequence)return;result=data}catch{if(current!==sequence)return;failed=true}finally{if(current===sequence){pending=false;$('plan').disabled=$('run').disabled=false;render()}}}
 $('plan').onclick=()=>act('plan');$('run').onclick=()=>act('run');
 $('copy').onclick=async()=>{if(!result)return;try{await navigator.clipboard.writeText(JSON.stringify(result,null,2));copyKey='dev.copied'}catch{copyKey='dev.copy-failed'}render()};
 window.addEventListener('gridzen:language',()=>{countriesView();render()});
 request('/coverage').then(data=>{countries=data.countries;countriesView();act('plan')}).catch(()=>{failed=true;render()});
})();
