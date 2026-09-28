from fastapi.testclient import TestClient
from src.api.main import app
from src.database.db import engine

def test_api_validation_and_health():
    c=TestClient(app)
    assert c.get('/health').status_code==200
    assert c.post('/analyze-complaint',json={'text':'short'}).status_code==422
    assert c.post('/similar-cases',json={'text':'A pump alarm failed','top_k':100}).status_code==422

def test_investigation_persists_and_review(tmp_path,monkeypatch):
    monkeypatch.setenv('DATABASE_URL','sqlite:///'+str(tmp_path/'test.db'));engine.cache_clear()
    c=TestClient(app)
    r=c.post('/full-investigation',json={'text':'Infusion pump stopped medication delivery. No death reported.','analysis_date':'2026-09-27'})
    assert r.status_code==200,r.text
    obj=r.json();assert obj['human_review_required'] and not obj['entities']['serious_outcome']
    assert c.post('/investigations/'+obj['investigation_id']+'/review',json={'reviewer':'Test reviewer','notes':'Evidence reviewed for software test.'}).status_code==200
    engine.cache_clear()
