import pandas as pd
from src.retrieval.similarity_search import CaseSearch

def test_excludes_self_duplicates_and_future():
    rows=[('1','pump alarm stopped delivery','2025-01-01'),('2','pump alarm stopped medication','2025-01-01'),('3','pump alarm stopped medication','2025-01-01'),('4','pump alarm stopped','2027-01-01')]
    s=CaseSearch(pd.DataFrame(rows,columns=['mdr_report_key','narrative','date_received']))
    found=s.search(rows[0][1],5,as_of='2026-01-01')
    assert [x['mdr_report_key'] for x in found]==['2']
def test_empty_index():assert CaseSearch(pd.DataFrame()).search('pump')==[]
def test_faiss_cosine():
    import pytest
    pytest.importorskip('faiss')
    import numpy as np
    from src.retrieval.faiss_index import create_index
    idx=create_index(np.array([[1,0],[0,1]],dtype='float32'))
    scores,ids=idx.search(np.array([[1,0]],dtype='float32'),1)
    assert ids[0,0]==0 and abs(scores[0,0]-1)<1e-6
