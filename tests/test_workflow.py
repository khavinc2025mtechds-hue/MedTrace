import pytest
from src.agents.workflow import investigate
from src.reports.report_generator import to_html

def test_workflow_graph_matches_sequential():
    pytest.importorskip('langgraph')
    q={'text':'An infusion pump stopped medication delivery with an occlusion alarm.','analysis_date':'2026-09-27'}
    a=investigate(q,persist=False,workflow='sequential');b=investigate(q,persist=False,workflow='langgraph')
    for key in ['entities','priority','similar_cases','regulatory','recommendation']:assert a[key]==b[key]

def test_html_escapes_complaint():
    r=investigate({'text':'Pump failed <script>alert(1)</script>','analysis_date':'2026-09-27'},persist=False)
    h=to_html(r);assert '<script>' not in h and '&lt;script&gt;' in h
