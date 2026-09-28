"""Local research API. Bind to loopback unless authentication is added."""
from fastapi import APIRouter,HTTPException
from src.api.schemas import ComplaintInput,RegulatoryQuery,ReviewInput
from src.nlp.complaint_parser import parse_complaint
from src.agents.workflow import investigate,search_service
from src.rag.rag_pipeline import answer
from src.database.crud import review
router=APIRouter()
@router.get('/health')
def health():return {'status':'ok','application':'MedTrace AI','mode':'research decision support'}
@router.post('/analyze-complaint')
def analyze(q:ComplaintInput):return parse_complaint(q.text,q.model_dump(mode='json'))
@router.post('/similar-cases')
def similar(q:ComplaintInput):return {'cases':search_service().search(q.text,q.top_k,as_of=q.complaint_date.isoformat())}
@router.post('/priority-score')
def priority(q:ComplaintInput):return investigate(q,persist=False)['priority']
@router.post('/regulatory-search')
def regulatory(q:RegulatoryQuery):return answer(q.question,q.analysis_date.isoformat())
@router.post('/full-investigation')
def full(q:ComplaintInput):return investigate(q)
@router.post('/investigations/{investigation_id}/review')
def mark_review(investigation_id:str,q:ReviewInput):
    try:return review(investigation_id,q.reviewer,q.notes)
    except KeyError:raise HTTPException(status_code=404,detail='Investigation not found')
