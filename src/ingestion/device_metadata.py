"""Fetch product classification and optional identifier-specific FDA metadata."""
import argparse,json
from datetime import datetime,timezone
from src.ingestion.openfda_client import OpenFDAClient
from config.settings import path

def fetch(product_code='FRN',k_number=None,pma_number=None,udi_query=None):
    client=OpenFDAClient();queries=[('classification','device/classification','product_code:'+product_code)]
    if k_number:queries.append(('510k','device/510k','k_number:'+k_number))
    if pma_number:queries.append(('pma','device/pma','pma_number:'+pma_number))
    # UDI field definitions vary; accept an explicit query checked against FDA documentation.
    if udi_query:queries.append(('udi','device/udi',udi_query))
    output=[]
    for name,endpoint,query in queries:
        rows=client.collect(endpoint,query,100);p=path('data/raw/'+name+'_metadata.json');p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps({'results':rows,'provenance':{'endpoint':'https://api.fda.gov/'+endpoint+'.json','query':query,'retrieved_at':datetime.now(timezone.utc).isoformat(),'maximum':100}},indent=2))
        output.append({'file':str(p),'rows':len(rows)})
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--product-code',default='FRN');p.add_argument('--k-number');p.add_argument('--pma-number');p.add_argument('--udi-query');a=p.parse_args();print(fetch(a.product_code,a.k_number,a.pma_number,a.udi_query))
