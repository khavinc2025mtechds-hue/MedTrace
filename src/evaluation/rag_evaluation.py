"""Summarize manual claim judgments; citation presence is not faithfulness."""
import argparse,json
import pandas as pd
from config.settings import path

def evaluate(csv_path):
    df=pd.read_csv(csv_path)
    cols={'claim_id','citation_correct','supported','reviewer'}
    if df.empty or not cols.issubset(df):raise ValueError('Need reviewed claim_id,citation_correct,supported,reviewer rows')
    if not df.citation_correct.isin([0,1]).all() or not df.supported.isin([0,1]).all():raise ValueError('Judgments must be binary 0/1')
    if df.reviewer.isna().any():raise ValueError('Reviewer is required')
    out={'claims':len(df),'citation_correctness':float(df.citation_correct.mean()),'supported_claim_fraction':float(df.supported.mean()),'method':'manual review, not automated entailment'}
    path('reports/evaluation/rag_metrics.json').write_text(json.dumps(out,indent=2));return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');a=p.parse_args();print(evaluate(a.csv))
