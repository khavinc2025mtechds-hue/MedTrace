"""Evaluate against human relevance judgments; report absent labels explicitly."""
import argparse,json
import pandas as pd
from config.settings import path
from src.retrieval.similarity_search import CaseSearch

def evaluate(query_file,qrels_file,backend='tfidf',k=5):
    queries=pd.read_csv(query_file).fillna('');qrels=pd.read_csv(qrels_file,dtype={'mdr_report_key':str});search=CaseSearch(backend=backend);rows=[]
    for _,q in queries.iterrows():
        relevant=set(qrels[(qrels.query_id==q.query_id)&(qrels.relevance>0)].mdr_report_key)
        if not relevant:continue
        retrieved=search.search(q.narrative,k,exclude_ids=[q.get('mdr_report_key','')],as_of=q.get('as_of') or None)
        ids={str(x['mdr_report_key']) for x in retrieved};hits=len(ids & relevant)
        rows.append({'query_id':q.query_id,'precision_at_k':hits/k,'recall_against_judged_pool':hits/len(relevant),'retrieved':len(ids)})
    if not rows:raise ValueError('No positive relevance judgments. Create a manually judged pool first.')
    out={'backend':backend,'k':k,'queries':rows,'precision_at_k':sum(x['precision_at_k'] for x in rows)/len(rows),'recall_against_judged_pool':sum(x['recall_against_judged_pool'] for x in rows)/len(rows)}
    path('reports/evaluation/retrieval_'+backend+'.json').write_text(json.dumps(out,indent=2));return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('queries');p.add_argument('qrels');p.add_argument('--backend',default='tfidf');p.add_argument('--k',type=int,default=5);a=p.parse_args();print(evaluate(a.queries,a.qrels,a.backend,a.k))
