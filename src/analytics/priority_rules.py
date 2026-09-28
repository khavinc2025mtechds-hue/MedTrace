"""Transparent configurable points; neither harm probability nor FDA risk class."""
from config.settings import settings

def score_priority(entities,cases=None,trends=None,recalls=None,config=None):
    cfg=config or settings()['priority'];w=cfg['weights'];p=entities.get('problems',[]);cases=cases or [];trends=trends or {};recalls=recalls or {}
    # No double-counting general malfunction when delivery interruption is present.
    flags={'serious_outcome':bool(entities.get('serious_outcome')),'delivery_interruption':'delivery interruption' in p,
      'other_malfunction':p!=['other'] and 'delivery interruption' not in p,
      'repeated_reports':False,'reporting_spike':bool(trends.get('score_eligible') and trends.get('spike')),
      'verified_recall':any(x.get('match_status')=='verified_identifier_match' for x in recalls.get('matches',[]))}
    # Count qualified unique retrieved reports only; top-K is not total incidence.
    qualifying={str(c['mdr_report_key']) for c in cases if c.get('similarity_score',0)>=0.35}
    flags['repeated_reports']=len(qualifying)>=cfg['repeated_minimum']
    contributions=[{'factor':k,'points':int(w[k]) if v else 0,'active':v} for k,v in flags.items()]
    score=min(100,sum(x['points'] for x in contributions));t=cfg['thresholds']
    category='Critical' if score>=t['critical'] else 'High' if score>=t['high'] else 'Medium' if score>=t['medium'] else 'Low'
    return {'name':'MedTrace Analytical Investigation Priority Score','score':score,'out_of':100,'category':category,'method':'configurable rules','contributions':contributions,'qualified_retrieved_reports':len(qualifying),'limitations':['Unvalidated project rules; not a medical risk probability.','Low score does not establish safety or non-reportability.','Unknown evidence does not mean absence of risk.','Sample trends are not used as priority evidence.'],'human_review_required':True}
