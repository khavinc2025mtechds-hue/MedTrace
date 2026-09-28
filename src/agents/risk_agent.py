"""Priority and optional model explanation node."""
from src.analytics.priority_rules import score_priority
from src.analytics.shap_explainer import explain

def run(state):
    p=score_priority(state['entities'],state['similar_cases'],state['trends'],state['recalls'])
    f={'serious_outcome':int(state['entities']['serious_outcome']),'delivery_interruption':int('delivery interruption' in state['entities']['problems']),'qualified_similar_reports':p['qualified_retrieved_reports'],'verified_recall':int(any(x['active'] and x['factor']=='verified_recall' for x in p['contributions']))}
    try:shap=explain(f)
    except ImportError:shap={'status':'dependency_unavailable','message':'Install requirements-advanced.txt to explain a trained ML priority model.'}
    return {'priority':p,'shap':shap}
