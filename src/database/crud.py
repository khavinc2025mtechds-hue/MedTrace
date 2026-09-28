"""Persist all components atomically and capture human review separately."""
from src.database.db import session
from src.database.models import Complaint,Device,Investigation,SimilarCase,PriorityScore,RegulatoryEvidence,Report

def save(result,markdown):
    with session() as db,db.begin():
        cid=result['complaint_id'];iid=result['investigation_id']
        db.add(Complaint(id=cid,text=result['input']['text'],fields=result['input']));db.flush()
        db.add(Device(complaint_id=cid,details=result['entities']))
        db.add(Investigation(id=iid,complaint_id=cid,result=result));db.flush()
        db.add(PriorityScore(investigation_id=iid,details=result['priority']))
        for c in result['similar_cases']:db.add(SimilarCase(investigation_id=iid,report_key=c['mdr_report_key'],score=c['similarity_score']))
        for e in result['regulatory']['evidence']:db.add(RegulatoryEvidence(investigation_id=iid,details=e))
        db.add(Report(investigation_id=iid,markdown=markdown))

def review(iid,reviewer,notes):
    if not reviewer.strip() or not notes.strip():raise ValueError('Reviewer and review notes required')
    with session() as db,db.begin():
        obj=db.get(Investigation,iid)
        if obj is None:raise KeyError(iid)
        obj.review_status='reviewed';obj.reviewer=reviewer;obj.review_notes=notes
        return {'investigation_id':iid,'review_status':obj.review_status,'reviewer':reviewer,'notes':notes}
