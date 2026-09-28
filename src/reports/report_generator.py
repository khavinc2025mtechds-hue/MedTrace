"""Escaped HTML and Markdown exports preserve sources and uncertainty."""
import html,json
from config.settings import path

def to_markdown(r):
    e=r['entities'];p=r['priority'];rec=r['recommendation']
    lines=['# MedTrace investigation report',f'Investigation: {r["investigation_id"]}',f'Created: {r["created_at"]}','## Complaint',r['input']['text'],'## Extracted facts',json.dumps(e,indent=2),'## Historical evidence']
    for c in r['similar_cases']:lines += [f'- Report {c["mdr_report_key"]}; similarity {c["similarity_score"]} ({c["similarity_method"]}); {c["date_received"]}',c['narrative'],c['source_url']]
    lines += ['## Reporting patterns',json.dumps(r['trends'],indent=2),'## Investigation priority',f'{p["score"]}/100 ({p["category"]})',json.dumps(p['contributions'],indent=2),'## SHAP / model explanation',json.dumps(r['shap'],indent=2),'## Recall evidence',json.dumps(r['recalls'],indent=2),'## Regulatory evidence']
    for doc in r['regulatory']['evidence']:lines += [f'[{doc["id"]}] {doc["section"]}',doc['text'],doc['source_url']]
    draft=r['regulatory'].get('llm_draft',{})
    if draft.get('text'):lines += ['## Unverified LLM draft (requires review)',draft['text']]
    lines += ['## Suggested next steps']+['- '+a for a in rec['next_steps']]+['## Missing evidence']+['- '+g for g in rec['missing_evidence']]+['## Claim-to-evidence record',json.dumps(rec['claim_evidence'],indent=2),'## Human decision',rec['final_regulatory_decision'],rec['disclaimer']]
    return '\n\n'.join(lines)

def to_html(r):
    return '<!doctype html><html><head><meta charset="utf-8"><title>MedTrace report</title><style>body{max-width:960px;margin:40px auto;font:16px system-ui;color:#163246}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style></head><body><pre>'+html.escape(to_markdown(r))+'</pre></body></html>'

def export(r):
    folder=path('reports/sample_reports');folder.mkdir(parents=True,exist_ok=True);name=r['investigation_id']
    for ext,body in [('md',to_markdown(r)),('html',to_html(r)),('json',json.dumps(r,indent=2))]:(folder/(name+'.'+ext)).write_text(body,encoding='utf-8')
    return str(folder/(name+'.html'))
