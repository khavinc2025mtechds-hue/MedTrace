"""Historical retrieval node."""
def run(state,search):
    q=state['input'];return {'similar_cases':search.search(q['text'],q['top_k'],as_of=q['complaint_date'])}
