"""Shared Streamlit views used by all pages."""
import os,json
from datetime import date
import streamlit as st
import pandas as pd
import plotly.express as px
from src.api.schemas import ComplaintInput
from src.agents.workflow import investigate,search_service
from src.reports.report_generator import to_markdown,to_html
EXAMPLE='An infusion pump stopped medication delivery during treatment and displayed an occlusion alarm even though no blockage was found.'
def header(title):
    st.title(title);st.caption('MedTrace AI · Infusion-pump complaint investigation · Research prototype')
def current():
    r=st.session_state.get('investigation')
    if not r:st.info('Run an investigation on the New Complaint page first.');st.stop()
    return r

def complaint_form():
    header('New complaint investigation')
    with st.form('complaint'):
        text=st.text_area('Complaint narrative',EXAMPLE,height=140)
        c1,c2=st.columns(2);manufacturer=c1.text_input('Manufacturer (if known)');model=c2.text_input('Model (if known)')
        device=st.text_input('Device name','Infusion pump');impact=st.text_input('Reported patient impact (leave blank if unknown)')
        c1,c2=st.columns(2);serial=c1.text_input('Serial number (optional)');lot=c2.text_input('Lot number (optional)')
        c1,c2=st.columns(2);when=c1.date_input('Complaint date',date.today());analysis=c2.date_input('Regulatory analysis date',date.today())
        source=st.selectbox('Input source',['DEMO user-entered complaint','Authorized internal complaint','Held-out public report'])
        k=st.slider('Similar cases to retrieve',1,20,5);submitted=st.form_submit_button('Investigate complaint',type='primary')
    if submitted:
        try:
            q=ComplaintInput(text=text,manufacturer=manufacturer,model=model,device_name=device,patient_impact=impact,serial_number=serial,lot_number=lot,complaint_date=when,analysis_date=analysis,source=source,top_k=k)
            with st.spinner('Collecting evidence and preparing the investigation…'):
                url=os.getenv('MEDTRACE_API_URL','').strip()
                if url:
                    import requests
                    response=requests.post(url.rstrip('/')+'/full-investigation',json=q.model_dump(mode='json'),timeout=120);response.raise_for_status();r=response.json()
                else:r=investigate(q)
            st.session_state['investigation']=r;st.success('Investigation ready for human review.')
        except Exception as exc:st.error(f'Investigation could not complete: {type(exc).__name__}: {exc}')
    if st.session_state.get('investigation'):
        r=current();st.subheader('Reported facts');st.write(r['recommendation']['summary']);st.json(r['entities']);st.warning('Missing information: '+ '; '.join(r['recommendation']['missing_evidence']))

def show_cases():
    header('Similar MAUDE cases');r=current();st.caption('Similarity is a retrieval score, not probability or proof of a common cause.')
    if not r['similar_cases']:st.info('No matching reports in the loaded corpus.');return
    for c in r['similar_cases']:
        with st.expander(f'Report {c["mdr_report_key"]} · {c["similarity_score"]:.3f} · {c["device"]}'):
            st.write(c['narrative']);st.write({k:c[k] for k in ['manufacturer','model','event_type','date_received','device_problems']});st.link_button('Open FDA report',c['source_url'])

def show_trends():
    header('Reporting patterns');r=current();t=r['trends'];st.info(t['interpretation']);st.caption(t['scope'])
    if t['monthly']:st.plotly_chart(px.bar(pd.DataFrame(t['monthly']),x='month',y='reports',title='Reports in loaded data'),width='stretch')
    else:st.write('No dated records for this selection.')
    st.subheader('Recall intelligence');st.write(r['recalls']['message'])
    for m in r['recalls']['matches']:
        with st.expander(m['recall_number']+' · candidate match'):st.json(m)

def show_priority():
    header('Investigation priority');r=current();p=r['priority'];st.metric(p['name'],f'{p["score"]}/100',p['category']);st.caption('Unvalidated analytical score. Low priority does not establish safety.')
    st.plotly_chart(px.bar(pd.DataFrame(p['contributions']),x='points',y='factor',orientation='h'),width='stretch');st.subheader('ML / SHAP explanation');st.json(r['shap'])

def show_regulatory():
    header('Regulatory evidence');r=current();reg=r['regulatory'];st.write(reg['answer']);st.caption('Analysis date: '+reg['analysis_date'])
    for e in reg['evidence']:
        with st.expander(e['section']+' · '+e['id']):st.write(e['text']);st.link_button('Official source',e['source_url']);st.caption('Retrieved: '+e.get('retrieved_at','unknown'))
    if reg['llm_draft'].get('text'):st.warning('LLM draft: semantic support requires human review.');st.write(reg['llm_draft']['text'])

def show_report():
    header('Investigation report');r=current();st.write(r['recommendation']['summary']);st.subheader('Suggested next steps')
    for step in r['recommendation']['next_steps']:st.write('• '+step)
    st.subheader('Missing evidence');st.write(r['recommendation']['missing_evidence']);st.caption(r['recommendation']['disclaimer'])
    st.download_button('Download Markdown',to_markdown(r),'medtrace_report.md','text/markdown')
    st.download_button('Download HTML (browser Print → PDF)',to_html(r),'medtrace_report.html','text/html')
    st.download_button('Download complete JSON',json.dumps(r,indent=2),'medtrace_report.json','application/json')
    st.subheader('Human review')
    with st.form('review'):
        name=st.text_input('Reviewer');notes=st.text_area('Investigator assessment and next action');submit=st.form_submit_button('Record human review')
    if submit:
        try:
            url=os.getenv('MEDTRACE_API_URL','').strip()
            if url:
                import requests
                res=requests.post(url.rstrip('/')+f'/investigations/{r["investigation_id"]}/review',json={'reviewer':name,'notes':notes},timeout=30);res.raise_for_status()
            else:
                from src.database.crud import review
                review(r['investigation_id'],name,notes)
            st.success('Human review recorded.')
        except Exception as exc:st.error(str(exc))
