import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
@pytest.fixture(autouse=True)
def local_defaults(monkeypatch):
    monkeypatch.setenv('LLM_PROVIDER','none')
    monkeypatch.setenv('RETRIEVAL_BACKEND','tfidf')
    monkeypatch.setenv('WORKFLOW_BACKEND','sequential')
