"""Equivalent sequential and LangGraph workflows sharing the same nodes."""
import argparse,json,uuid,logging
from datetime import datetime,timezone
from typing import TypedDict
from functools import lru_cache
from config.settings import settings,path
from src.retrieval.similarity_search import CaseSearch
from src.agents import complaint_agent,retrieval_agent,trend_agent,recall_agent,risk_agent,regulatory_agent,synthesis_agent
from src.api.schemas import ComplaintInput
LOG=logging.getLogger(__name__)
class InvestigationState(TypedDict,total=False):
    input:dict
    entities:dict
    similar_cases:list
    trends:dict
    recalls:dict
    priority:dict
    shap:dict
    regulatory:dict
    recommendation:dict
@lru_cache(maxsize=1)
def search_service():return CaseSearch()

def investigate(complaint, persist=True, workflow=None):
    data=complaint.model_dump(mode='json') if isinstance(complaint,ComplaintInput) else ComplaintInput(**complaint).model_dump(mode='json')
    search=search_service();backend=workflow or settings()['workflow'];state={'input':data}
    nodes=[('complaint',complaint_agent.run),('retrieval',lambda s:retrieval_agent.run(s,search)),('trend',lambda s:trend_agent.run(s,search)),('recall',recall_agent.run),('priority',risk_agent.run),('regulatory',regulatory_agent.run),('synthesis',synthesis_agent.run)]
    if backend=='langgraph':
        from langgraph.graph import StateGraph,START,END
        g=StateGraph(InvestigationState);previous=START
        for name,fn in nodes:g.add_node(name,fn);g.add_edge(previous,name);previous=name
        g.add_edge(previous,END);state=g.compile().invoke(state)
    elif backend=='sequential':
        for _,fn in nodes:state.update(fn(state))
    else:raise ValueError('workflow must be sequential or langgraph')
    result={**state,'complaint_id':'C-'+uuid.uuid4().hex[:12],'investigation_id':'I-'+uuid.uuid4().hex[:12],'created_at':datetime.now(timezone.utc).isoformat(),'workflow_backend':backend,'retrieval_backend':search.backend,'data_status':{'loaded_reports':len(search.frame),'scope':'loaded sample/subset; not population estimates'},'human_review_required':True}
    if persist:
        from src.database.crud import save
        from src.reports.report_generator import to_markdown
        save(result,to_markdown(result))
    LOG.info('Investigation %s completed using %s',result['investigation_id'],backend)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--text',default='An infusion pump stopped medication delivery during treatment and displayed an occlusion alarm even though no blockage was found.');p.add_argument('--workflow',choices=['sequential','langgraph']);p.add_argument('--no-save',action='store_true');a=p.parse_args()
    r=investigate(ComplaintInput(text=a.text),persist=not a.no_save,workflow=a.workflow)
    from src.reports.report_generator import export
    print(json.dumps(r,indent=2));print(export(r))
