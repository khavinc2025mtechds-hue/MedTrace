# Validation performed

Verified on 2026-09-28 with Python 3.12 in the execution workspace.

- **18 automated tests passed**: extraction/negation, raw report joining, retrieval exclusions and deduplication, FAISS numeric search, priority contributions, regulatory date filtering/provenance, API input validation, SQLite persistence and human review, sequential/LangGraph parity, HTML escaping.
- Streamlit AppTest passed for the homepage, complaint submission, and all five result pages.
- End-to-end example rerun: 5 retrieved cases, priority 20/100, 4 regulatory passages; no patient outcome invented. Full actual output is in reports/sample_reports/demo_stages.json.
- EDA regenerated from 280 real sample records; source compiled successfully.

## Not claimed as validated
BERT/RoBERTa training, pretrained semantic embeddings, XGBoost/SHAP on reviewer labels, optional LLM providers, PostgreSQL, Docker deployment and Windows execution were not run here. Their implementations and activation instructions are included. FAISS numeric indexing and LangGraph were exercised, but that does not establish semantic retrieval quality.

No research accuracy, F1, retrieval precision or clinical safety performance is fabricated. Independent annotations, trained weights and a proper research evaluation are still required. The 20,000-record download attempt did not complete; only the explicitly described development sample is included.

Commands to repeat: `python -m pytest -q`, `python -m src.analytics.eda`, and `python -m src.agents.workflow --no-save`.
