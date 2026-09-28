"""Recall evidence node."""
from src.recalls.recall_lookup import lookup

def run(state):return {'recalls':lookup(state['entities'])}
