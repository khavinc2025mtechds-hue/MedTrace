# Implementation guide

Follow README.md from the project root. Install Python 3.12 and VS Code first. Core requirements provide the local dashboard, API, SQLite and TF-IDF/extractive workflow. Git, Docker, PostgreSQL, Ollama and advanced ML dependencies are optional.

## Suggested order
1. Run the bundled example in Streamlit.
2. Review each stage in reports/sample_reports/demo_stages.json.
3. Download/preprocess a larger scoped corpus using DATASET_GUIDE.md. Restart the dashboard after replacing data.
4. Prepare independently reviewed labels and retrieval judgments.
5. Train baseline and transformer models on the same split.
6. Enable semantic retrieval, LangGraph and optional SHAP/LLM components as documented.
7. Re-run tests and record evaluation outputs and hardware.

## Troubleshooting
- Module missing: install requirements using the same virtual-environment Python used to run the app.
- Blank retrieval: verify date range, product code and available narratives; no hit is a valid outcome.
- Missing regulatory evidence for an earlier date: add the applicable historical snapshot.
- Model not trained: provide reviewed labels and run the relevant training command. No fabricated weights are supplied.
- FDA timeout: retry later or use smaller date partitions/raw FDA files. A failed download must not be presented as complete.
- Docker virtualization unavailable: run native Python and SQLite; Docker is optional.
- Managed laptop blocks installation: use your organization's approved installation/transfer process.
