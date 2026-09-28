from src.nlp.entity_extractor import extract

def test_negation():
    e=extract('No death or serious injury was reported. The infusion pump stopped delivery.')
    assert not e['serious_outcome']
    assert 'delivery interruption' in e['problems']
def test_alarm_absence_is_issue():
    assert 'alarm failure' in extract('The pump failed with no alarm.')['problems']
def test_no_outcome_invented():
    e=extract('Occlusion alarm during medication delivery.')
    assert e['outcome']=='Unknown' and e['patient_impact']=='Not reported'
def test_spans_reproduce_evidence():
    s='The pump stopped medication delivery; no death occurred.'
    for e in extract(s)['evidence_spans']:assert s[e['start']:e['end']]==e['quote']
