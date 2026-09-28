"""Complaint extraction node."""
from src.nlp.complaint_parser import parse_complaint

def run(state):
    q=state['input'];return {'entities':parse_complaint(q['text'],q)}
