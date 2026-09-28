# MedTrace AI
Medical Device Complaint Investigation Platform · Khavin C

A local research prototype for infusion-pump complaint investigation. The working default uses rule-based extraction, TF-IDF case retrieval, transparent priority rules, and source-linked regulatory passages. It needs no paid API, GPU, downloaded model weights, or external database.

## Start on Windows
Install Python **3.12**, Visual Studio Code, and its Python extension. Git is optional for approved version control. Use a terminal inside `MedTrace_AI`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m streamlit run app/streamlit_app.py
```
Open the local URL printed by Streamlit. Select **New Complaint**, keep the example, and click **Investigate complaint**. The remaining pages show cases, trends, scoring, regulatory evidence, and downloadable reports. SQLite is created automatically in `data/medtrace.db`.

Directly invoking the virtual-environment interpreter avoids needing to change PowerShell execution policy. On macOS/Linux use `python3.12 -m venv .venv` and `.venv/bin/python` instead.

## Included evidence
- 280 real openFDA MAUDE reports: FRN, 2025; a capped convenience sample across months, **not** a representative epidemiological dataset.
- 100 real FDA enforcement records returned by a pump-description query; candidate recall context, not confirmed device matches.
- One FDA FRN classification record.
- Current eCFR Part 803 and §820.35 HTML snapshots, indexed into 72 source-linked chunks. Snapshot applicability begins 2026-09-24; historical analyses need historical versions.
- One clearly marked synthetic *new complaint* for demonstrating the workflow. It is never mixed into the public evidence dataset or claimed as a research result.

The project scope is configurable to 2021–2025 and 20,000–100,000 filtered records; the large corpus is **not included**. Use [DATASET_GUIDE.md](docs/DATASET_GUIDE.md) to download it. `data/processed/processed_maude.csv`, when present, takes precedence over the bundled sample. Restart the app after changing data/index settings.

## Command-line investigation and API

```powershell
.\.venv\Scripts\python.exe -m src.agents.workflow
.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```
API docs: http://127.0.0.1:8000/docs . Endpoints: GET `/health`; POST `/analyze-complaint`, `/similar-cases`, `/priority-score`, `/regulatory-search`, `/full-investigation`, `/investigations/{id}/review`. For API-backed Streamlit set `MEDTRACE_API_URL=http://127.0.0.1:8000` in `.env`; otherwise it calls the same pipeline locally.

Example request body:
```json
{"text":"An infusion pump stopped medication delivery and displayed an occlusion alarm even though no blockage was found.","analysis_date":"2026-09-27","complaint_date":"2026-09-27","top_k":5}
```

## Advanced components
Install additional packages only when needed:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-advanced.txt
```

- **SentenceTransformers + FAISS:** set `RETRIEVAL_BACKEND=semantic`; first use downloads `sentence-transformers/all-MiniLM-L6-v2`. Build a persisted index with `python -m src.retrieval.similarity_search --backend semantic`.
- **LangGraph:** set `WORKFLOW_BACKEND=langgraph`. This runs the same explicit nodes in a state graph.
- **Classifier comparison:** supply independently reviewed labels, then train TF-IDF/logistic regression and BERT/RoBERTa with the commands in the evaluation plan. Set `CLASSIFIER_BACKEND=baseline` or `transformer` after training to display its prediction alongside extracted facts. Rules remain the default and model predictions do not replace evidence spans.
- **XGBoost + SHAP:** train only on independent reviewer priority judgments. No rule-generated targets. If weights are absent, the app reports `not_trained`; the transparent rule score still works.
- **Optional LLM:** use `LLM_PROVIDER=openai` with `LLM_MODEL`, `OPENAI_BASE_URL`, `OPENAI_API_KEY`, or `LLM_PROVIDER=ollama` with a locally available model and `OLLAMA_BASE_URL`. Default `none` returns actual passages. LLM text is an unverified draft; citation-ID checks do not establish entailment. Provider failure retains the extractive evidence.
- **PostgreSQL/Docker:** Docker Desktop is optional. Set `POSTGRES_PASSWORD` in `.env`, run `docker compose up --build`, then open http://localhost:8501. SQLite is the native default.

## Verification
```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m src.analytics.eda
.\.venv\Scripts\python.exe -m src.agents.workflow --workflow langgraph --no-save
```
See [VALIDATION.md](docs/VALIDATION.md) for the checks actually performed and unverified optional paths. Generated sample stage outputs are under `reports/sample_reports/`.

## Interpretation and limitations
This is investigator decision support, not a validated medical device, automatic MDR determination, clinical diagnosis, or root-cause determination. MAUDE reports can be incomplete, duplicated, biased, or unverified. Similar wording does not establish identical failure mechanisms. The priority score is an unvalidated project rubric, not an FDA score or probability of harm. Recall text matches require device-identifier review. Final reportability, causality, CAPA, and regulatory decisions remain with qualified people.

The 2026 QMSR transition matters: do not present historical §820.198 as the current complaint-record provision. Current §820.35 and the incorporated QMS requirements require appropriate professional interpretation; this corpus does not reproduce licensed ISO standards.

## Files and transfer
Start with [FILE_MANIFEST.md](FILE_MANIFEST.md), [TRANSFER_GUIDE.md](TRANSFER_GUIDE.md), and [setup_project_structure.ps1](setup_project_structure.ps1). Source files are delivered individually, not in a ZIP. Eight notebooks reproduce the data, NLP, retrieval, priority, RAG, and workflow steps. Architecture, evaluation, dataset guidance, and viva notes are in `docs/`.

To open notebooks in VS Code, install its Jupyter extension and run `python -m pip install ipykernel` in the same virtual environment. Select that environment as the notebook kernel.
