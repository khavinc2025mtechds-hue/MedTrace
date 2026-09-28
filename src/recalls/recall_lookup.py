"""Conservative recall candidates with explicit unavailable/no-match distinction."""
import json
import re
from config.settings import path,settings

def lookup(entities,records=None):
    if records is None:
        p=path(settings()['data']['recalls'])
        if not p.exists():return {'status':'unavailable','matches':[],'message':'Recall dataset unavailable; no conclusion about recall status.'}
        obj=json.loads(p.read_text(encoding='utf-8'));records=obj.get('results',[]) if isinstance(obj,dict) else obj
    model=entities.get('model','').strip();maker=entities.get('manufacturer','').strip()
    if not model and not maker:return {'status':'insufficient_identifiers','matches':[],'message':'Provide manufacturer and model to assess possible recall matches.'}
    matches=[]
    for r in records:
        product=r.get('product_description','');firm=r.get('recalling_firm','')
        model_match=bool(model and re.search(r'(?<![a-z0-9])'+re.escape(model)+r'(?![a-z0-9])',product,re.I))
        maker_match=bool(maker and maker.casefold()==firm.casefold())
        if not (model_match or maker_match):continue
        matches.append({'recall_number':r.get('recall_number',''),'product':product,'firm':firm,'reason':r.get('reason_for_recall',''),'status':r.get('status',''),'classification':r.get('classification',''),'match_status':'candidate_requires_lot_and_identifier_review','model_match':model_match,'manufacturer_exact_match':maker_match,'source_url':'https://api.fda.gov/device/enforcement.json?search=recall_number:'+r.get('recall_number','')})
    return {'status':'candidates_found' if matches else 'no_match_in_loaded_data','matches':matches[:10],'message':'Candidate matches require identity and affected-lot verification.' if matches else 'No relevant recall identified in the retrieved FDA data.'}

if __name__=='__main__':
    from src.ingestion.openfda_client import OpenFDAClient
    rows=OpenFDAClient().collect('device/enforcement','product_description:pump',1000)
    dest=path(settings()['data']['recalls']);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps({'results':rows},indent=2));print(len(rows),'recall records saved')
