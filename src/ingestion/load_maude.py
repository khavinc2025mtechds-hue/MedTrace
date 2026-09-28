"""Normalize API data while retaining report-level identity and source provenance."""
import argparse
import json
import hashlib
import pandas as pd
from config.settings import path, settings
from src.preprocessing.clean_text import clean_text
from src.preprocessing.filter_infusions import filter_infusions
COLUMNS=['mdr_report_key','date_received','event_date','device','manufacturer','model','product_code','narrative','device_problems','patient_problems','event_type','source_url','source_kind','narrative_hash']
def api_rows(records: list, codes=('FRN',)) -> pd.DataFrame:
    rows=[]
    for r in records:
        devices=[d for d in r.get('device',[]) if d.get('device_report_product_code') in codes]
        if not devices: continue
        # Select an in-scope device, retain complete original JSON for multi-device review.
        d=devices[0]; key=str(r.get('mdr_report_key',''))
        narratives=[t.get('text','') for t in r.get('mdr_text',[]) if t.get('text_type_code')=='Description of Event or Problem']
        if not narratives: narratives=[t.get('text','') for t in r.get('mdr_text',[])]
        narrative=clean_text(' '.join(dict.fromkeys(narratives)))
        if not key or not narrative: continue
        def date(v):
            out=pd.to_datetime(v,errors='coerce')
            return out.strftime('%Y-%m-%d') if pd.notna(out) else ''
        problems=r.get('device_problem',[])
        patient=[p for x in r.get('patient',[]) for p in x.get('patient_problems',[])]
        rows.append(dict(zip(COLUMNS,[key,date(r.get('date_received')),date(r.get('date_of_event')),d.get('generic_name') or d.get('brand_name',''),d.get('manufacturer_d_name',''),d.get('model_number',''),d.get('device_report_product_code',''),narrative,'; '.join(problems),'; '.join(patient),r.get('event_type',''),f'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id={key}','FDA openFDA MAUDE',hashlib.sha256(narrative.casefold().encode()).hexdigest()])))
    return pd.DataFrame(rows,columns=COLUMNS).drop_duplicates('mdr_report_key')

def load(pathname: str) -> pd.DataFrame:
    p=path(pathname)
    if p.suffix=='.csv': return pd.read_csv(p,dtype=str).fillna('')
    if p.suffix=='.parquet':return pd.read_parquet(p).fillna('')
    if p.suffix=='.jsonl': records=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
    else:
        obj=json.loads(p.read_text(encoding='utf-8'));records=obj.get('results',[]) if isinstance(obj,dict) else obj
    return api_rows(records,settings()['data']['product_codes'])

def prepare(input_file: str, output: str | None = None):
    cfg=settings()['data'];df=filter_infusions(load(input_file),cfg['product_codes'],cfg['start_date'],cfg['end_date'],cfg['max_rows'])
    df=df.drop_duplicates('mdr_report_key');df=df[df.narrative.str.strip().ne('')]
    dest=path(output or cfg['processed']);dest.parent.mkdir(parents=True,exist_ok=True);df.to_csv(dest,index=False)
    print(f'{len(df)} unique reports saved to {dest}')
    return df
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output');a=p.parse_args();prepare(a.input,a.output)
