"""Report-count analysis node."""
from src.analytics.trend_analysis import analyze_trends

def run(state,search):
    e=state['entities'];return {'trends':analyze_trends(search.frame,state['input']['complaint_date'],e['manufacturer'],e['model'])}
