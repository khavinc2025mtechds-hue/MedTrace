"""Run: python -m streamlit run app/streamlit_app.py"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
from app.components.ui_components import header
from src.agents.workflow import search_service
from config.settings import settings,path
st.set_page_config(page_title='MedTrace AI',page_icon='🔎',layout='wide')
header('MedTrace AI')
st.write('Investigate a device complaint using reported facts, historical cases and cited regulatory evidence.')
a,b,c=st.columns(3);search=search_service();a.metric('Loaded public reports',len(search.frame));b.metric('Retrieval mode',search.backend.upper());c.metric('Final decision','Human review')
st.info('The bundled dataset is a small convenience sample. It supports software demonstrations, not population-level safety conclusions.')
st.page_link('pages/1_New_Complaint.py',label='Start a new investigation',icon='🔎')
st.subheader('Dataset and model status')
st.json({'product_codes':settings()['data']['product_codes'],'configured_dates':[settings()['data']['start_date'],settings()['data']['end_date']],'baseline_trained':path('models/classifiers/baseline.joblib').exists(),'transformer_trained':path('models/classifiers/transformer/config.json').exists(),'priority_model_trained':path('models/priority/priority.joblib').exists(),'regulatory_corpus':path(settings()['regulatory']['corpus']).exists()})
st.caption('Use the sidebar to inspect similar cases, reporting patterns, priority, regulatory evidence and the final report.')
