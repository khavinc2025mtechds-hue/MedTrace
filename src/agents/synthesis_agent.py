"""Deterministic evidence synthesis; hypotheses are explicitly marked."""
DISCLAIMER='Research prototype for decision support. Qualified humans make final regulatory decisions. MAUDE reports do not establish causality or incidence.'

def run(state):
    e=state['entities'];gaps=list(e['missing_evidence']);actions=['Review original complaint details and obtain missing device identifiers.','Compare retrieved reports with the current event before treating them as related.','Have a qualified investigator review the cited regulatory passages.']
    if e['alarm_issue']:actions.insert(0,'Inspect the alarm history and occlusion-detection subsystem if available.')
    if 'software issue' in e['problems']:actions.insert(0,'Review firmware version and device logs if available.')
    if 'delivery interruption' in e['problems']:actions.insert(0,'Inspect the returned pump and delivery pathway if available.')
    if not state['similar_cases']:gaps.append('No sufficiently similar case retrieved from the loaded sample')
    if not state['regulatory']['evidence']:gaps.append('No applicable regulatory evidence retrieved')
    if state['recalls']['status'] in ['unavailable','insufficient_identifiers']:gaps.append(state['recalls']['message'])
    claims=[{'claim':'Complaint reports '+s['value'],'kind':'reported_fact','evidence':[{'source':'complaint','quote':s['quote'],'start':s['start'],'end':s['end']}]} for s in e['evidence_spans']]
    claims.append({'claim':f'{len(state["similar_cases"])} similar reports retrieved from loaded data','kind':'retrieval_result','evidence':[{'report_key':c['mdr_report_key'],'source_url':c['source_url']} for c in state['similar_cases']]})
    return {'recommendation':{'summary':'Reported problems: '+', '.join(e['problems'])+'. Patient impact: '+e['patient_impact']+'.','next_steps':actions,'action_status':'Suggested investigation steps, not confirmed causes','missing_evidence':gaps,'claim_evidence':claims,'final_regulatory_decision':'Pending qualified human review','disclaimer':DISCLAIMER}}
