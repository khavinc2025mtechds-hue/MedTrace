# Architecture and data flow

New complaint → validated input → evidence-span extraction → historical case retrieval → descriptive trend and candidate recall lookup → transparent priority → date-filtered regulatory retrieval → investigation synthesis → SQLite/PostgreSQL snapshot → dashboard/report → human review.

The sequential and LangGraph modes share node functions, allowing direct output comparison. No agent independently decides legal reportability. `config/config.yaml` controls data scope, retrieval model, thresholds, and paths; `.env` contains optional connection settings.

## Modules
- `src/ingestion` and `src/preprocessing`: API downloads, provenance, FDA raw joins and normalized CSV.
- `src/nlp`: evidence extraction and trainable baseline/transformer classifiers; model prediction is separate from observed facts.
- `src/retrieval`: TF-IDF baseline, normalized sentence embeddings, FAISS inner-product search.
- `src/analytics`: sample EDA, descriptive counts, rule contributions, optional reviewer-trained XGBoost/SHAP.
- `src/rag`: source-aware documents/chunks, applicable-date filtering, retrieval, extractive answer and optional provider-swappable drafting.
- `src/agents`: explicit workflow nodes and claim-to-evidence synthesis.
- `src/database`: complaints, devices, investigations, similar-case links, priority, regulatory evidence, reports; human review is stored separately from machine output.
- `src/api` and `app`: shared workflow exposed through FastAPI and Streamlit.
- `src/reports`: source-preserving Markdown, escaped HTML and JSON; browser printing provides PDF.

## Boundaries
Default execution is local and does not send complaint text to an LLM. Enabling an external provider transmits the query/evidence supplied to it and requires appropriate data authorization. API/dashboard bind to local development use; authentication, role-based access, encryption deployment controls, validated audit trails, migrations, monitoring, and production validation are future deployment work.

MAUDE duplicates can persist despite report-key and exact-narrative deduplication. Near-duplicate, manufacturer-template and follow-up clustering require additional review before publication. Retrieval filters out identical input text and future receipt dates; it cannot guarantee absence of semantic leakage. Sample trends never add risk points. Recall candidates never activate verified-recall points. Missing evidence remains explicit.

The design provides traceable evidence aggregation and investigator workflow, not a proven new NLP algorithm or automated causal inference.
