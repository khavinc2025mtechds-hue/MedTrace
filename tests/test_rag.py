from src.rag.regulatory_retriever import retrieve
from src.rag.rag_pipeline import answer

def test_historical_date_does_not_use_current_snapshot():
    r=retrieve('manufacturer complaint reporting',as_of='2020-01-01')
    assert r['evidence']==[]
def test_evidence_provenance():
    r=answer('manufacturer medical device complaint reporting malfunction',as_of='2026-09-27')
    assert r['evidence'] and r['llm_draft']['status']=='disabled'
    for e in r['evidence']:assert e['source_url'].startswith('https://www.ecfr.gov/') and e['document_sha256'] and e['id'].startswith('REG-')
