import pandas as pd
from src.preprocessing.merge_maude import merge
from src.ingestion.load_maude import api_rows

def test_raw_join_does_not_multiply_rows(tmp_path):
    tables={'m':'MDR_REPORT_KEY|DATE_RECEIVED\n1|2025-01-01\n', 'd':'MDR_REPORT_KEY|DEVICE_REPORT_PRODUCT_CODE|MODEL_NUMBER\n1|FRN|A\n1|FRN|B\n','t':'MDR_REPORT_KEY|FOI_TEXT\n1|Alarm failed\n1|Delivery stopped\n'}
    files={}
    for k,v in tables.items():p=tmp_path/(k+'.txt');p.write_text(v);files[k]=str(p)
    df=merge(files['m'],files['d'],files['t'])
    assert len(df)==1 and 'Alarm failed' in df.iloc[0].narrative and 'Delivery stopped' in df.iloc[0].narrative

def test_api_scope_and_empty_narrative():
    assert api_rows([{'mdr_report_key':'1','device':[{'device_report_product_code':'XYZ'}]}]).empty
    assert api_rows([{'mdr_report_key':'2','device':[{'device_report_product_code':'FRN'}]}]).empty
