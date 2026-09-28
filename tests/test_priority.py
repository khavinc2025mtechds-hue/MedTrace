from src.analytics.priority_rules import score_priority

def test_unverified_recall_and_sample_trend_add_no_points():
    r=score_priority({'problems':['other']},trends={'spike':True,'score_eligible':False},recalls={'matches':[{'match_status':'candidate'}]})
    assert r['score']==0
def test_delivery_not_double_counted():
    r=score_priority({'problems':['delivery interruption','occlusion alarm']})
    assert r['score']==20
    assert not next(x for x in r['contributions'] if x['factor']=='other_malfunction')['active']
def test_repeated_duplicate_id_does_not_raise_score():
    r=score_priority({'problems':['other']},cases=[{'mdr_report_key':'1','similarity_score':.9}]*5)
    assert r['score']==0 and r['qualified_retrieved_reports']==1
