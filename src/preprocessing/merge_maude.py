"""Join pipe-delimited FDA files without multiplying report rows."""
import argparse
import pandas as pd
from config.settings import path,settings
from src.ingestion.load_maude import COLUMNS
from src.preprocessing.clean_text import clean_text
from src.preprocessing.filter_infusions import filter_infusions
import hashlib

def read_table(filename):
    df=pd.read_csv(path(filename),sep='|',dtype=str,encoding='latin-1',keep_default_na=False)
    df.columns=df.columns.str.strip().str.lower()
    if 'mdr_report_key' not in df:raise ValueError(f'{filename}: missing MDR_REPORT_KEY')
    df['mdr_report_key']=df.mdr_report_key.str.strip()
    return df

def aggregate(df):
    # Preserve all child values but keep one row per report.
    return df.groupby('mdr_report_key',as_index=False).agg(lambda s:'; '.join(dict.fromkeys(x for x in s if x)))

def merge(master,device,text,problems=None,patient=None):
    cfg=settings()['data'];m=read_table(master).drop_duplicates('mdr_report_key',keep='last');d=read_table(device)
    code='device_report_product_code'
    if code not in d:raise ValueError('Device file requires DEVICE_REPORT_PRODUCT_CODE')
    d=d[d[code].str.upper().isin(cfg['product_codes'])].copy()
    d=d.rename(columns={'date_received':'device_date_received'})
    merged=m.merge(aggregate(d),on='mdr_report_key',how='inner',suffixes=('','_device'),validate='one_to_one')
    t=read_table(text)
    textcol=next((c for c in ['foi_text','text','narrative'] if c in t),None)
    if not textcol:raise ValueError('Narrative file requires FOI_TEXT, TEXT or NARRATIVE')
    merged=merged.merge(aggregate(t[['mdr_report_key',textcol]]).rename(columns={textcol:'narrative'}),on='mdr_report_key',how='left',validate='one_to_one')
    for filename,label in [(problems,'device_problems'),(patient,'patient_problems')]:
        if filename:
            child=read_table(filename);cols=[c for c in child if 'problem' in c]
            if not cols:raise ValueError(f'{filename}: no problem columns found')
            child[label]=child[cols].agg('; '.join,axis=1)
            merged=merged.merge(aggregate(child[['mdr_report_key',label]]),on='mdr_report_key',how='left',validate='one_to_one')
    aliases={'device':'generic_name','manufacturer':'manufacturer_d_name','model':'model_number','product_code':code,'event_date':'date_of_event'}
    for target,source in aliases.items():merged[target]=merged.get(source,'')
    for c in COLUMNS:
        if c not in merged:merged[c]=''
        merged[c]=merged[c].map(clean_text)
    for c in ['date_received','event_date']:merged[c]=pd.to_datetime(merged[c],errors='coerce',format='mixed').dt.strftime('%Y-%m-%d').fillna('')
    merged['source_kind']='FDA MAUDE raw files'
    merged['source_url']=merged.mdr_report_key.map(lambda k:f'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id={k}')
    merged['narrative_hash']=merged.narrative.map(lambda t:hashlib.sha256(t.casefold().encode()).hexdigest())
    # Multiple in-scope devices may give a joined code; retain the configured matching code.
    merged['product_code']=merged.product_code.map(lambda v:next((c for c in v.split('; ') if c in cfg['product_codes']),''))
    merged=filter_infusions(merged[COLUMNS],cfg['product_codes'],cfg['start_date'],cfg['end_date'],cfg['max_rows'])
    return merged[merged.narrative.ne('')]
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for x in ['master','device','text']:p.add_argument('--'+x,required=True)
    p.add_argument('--problems');p.add_argument('--patient');a=p.parse_args()
    df=merge(a.master,a.device,a.text,a.problems,a.patient);dest=path(settings()['data']['processed']);dest.parent.mkdir(parents=True,exist_ok=True);df.to_csv(dest,index=False);print(len(df),'reports saved')
