"""Regulatory evidence retrieval node."""
from src.rag.rag_pipeline import answer

def run(state):
    question='manufacturer medical device complaint investigation reporting malfunction death serious injury records '+ ' '.join(state['entities']['problems'])
    return {'regulatory':answer(question,state['input']['analysis_date'])}
