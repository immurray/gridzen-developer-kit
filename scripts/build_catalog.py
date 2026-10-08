"""Export only country/service research; never company/CRM/mailbox data."""
import csv, json, hashlib, sys
from pathlib import Path
root=Path(sys.argv[1]); out=Path(__file__).resolve().parents[1]/'src/gridzen_developer/data/catalog.json'
files=[root/'current/country-matrix.json',root/'csv/current/具体服务与接入.csv']
countries=json.loads(files[0].read_text()); rows=list(csv.DictReader(files[1].open(encoding='utf-8-sig')))
capabilities={'official_identity':'官方身份信息核验','commercial_identity':'商业身份数据核验','consented_eid':'用户授权电子身份','bank_account_match':'银行账户姓名匹配','consented_bank':'用户授权银行认证','cardholder_name':'银行卡持卡人姓名','phone_identity':'手机号实名或关联'}
data={'research_date':'2026-10-07','repository_commit':'d790d0ebfc5dd745d92515db04c9bb058897de9e','source_hashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'capabilities':capabilities,'countries':[]}
for c in countries:
 services=[]
 for r in rows:
  if r['ISO2']!=c['ISO2']:continue
  services.append({'capability':next(k for k,v in capabilities.items() if v==r['能力']),'name':r['现成服务'],'reported_status':r['状态'],'inputs':r['输入'],'outputs':r['输出'],'access_requirements':r['企业接入条件'],'user_participation':r['用户参与'],'limitations':r['边界/限制'],'source_ids':r['来源编号'],'source_urls':r['原文URL'].splitlines(),'observed_at':r['检索日期'],'live_available':False})
 data['countries'].append({'code':c['ISO2'],'name':c['国家或地区'],'region':c['区域'],'research_class':c['采购判断'],'limitations':c['边界与备注'],'capability_evidence':{k:c[v] for k,v in capabilities.items()},'services':services,'live_available':False})
assert len(data['countries'])==198 and sum(len(c['services']) for c in data['countries'])==230
out.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
print('198 country research records / 230 service records exported; no live routes')
