# Four-minute presentation and viva answers

## 0:00–0:40 — Problem
My project is MedTrace AI, a medical-device complaint investigation platform focused on infusion pumps. Complaint narratives can be lengthy and inconsistent, while investigators must connect the reported problem to historical reports, recall information and applicable regulatory evidence. Manually collecting this information takes time and can leave gaps in the investigation record.

## 0:40–1:20 — Proposed system and data
A user enters a new complaint. The system extracts device details, failure indicators and reported patient impact while keeping evidence spans and missing information. It searches real FDA MAUDE narratives for similar reports. Our development build contains a small real-data sample; the planned research corpus is a filtered 2021–2025 infusion-pump subset. FDA enforcement records provide candidate recall context, and official regulatory documents provide cited passages.

## 1:20–2:10 — Method
The runnable baseline combines rule-based extraction and TF-IDF retrieval. The advanced implementation supports BERT or RoBERTa classification and SentenceTransformer embeddings indexed with FAISS. Descriptive trend analysis shows report counts, while an explainable rule score helps organize investigation priority. An optional XGBoost model and SHAP require independent reviewer labels. Regulatory retrieval preserves source links and applicable dates. A LangGraph workflow coordinates these steps, and FastAPI, Streamlit and a database provide the application interface and investigation record.

## 2:10–3:00 — Contribution and research gaps
The proposed contribution is the integration of complaint understanding, historical evidence, transparent prioritization and regulatory traceability in one review workflow. A classifier alone does not produce a complete investigation record; semantic retrieval alone does not establish a cause; and generated text without source checking can introduce unsupported claims. MedTrace addresses these limitations through evidence spans, linked historical cases, explicit missing information and source-based regulatory passages. These are design motivations. Paper-specific research gaps must be verified against the actual literature before claiming those papers lack a feature.

## 3:00–3:40 — Evaluation and expected outcome
We will compare the TF-IDF baseline with BERT and RoBERTa on reviewed labels using macro F1 and class-level precision and recall. Retrieval will use human relevance judgments. Regulatory answers will be reviewed for citation accuracy and claim support. We will also measure investigation time and usability against a manual baseline. The expected outcome is a more organized, traceable investigation draft; improvements remain hypotheses until measured.

## 3:40–4:00 — Conclusion
MedTrace supports the investigator by gathering evidence, highlighting uncertainty and suggesting next steps. It does not decide causality or regulatory reportability. Human review remains the final stage.

## Likely questions
**What is novel?** The proposed integration and auditable investigation workflow. We do not claim invention of BERT, FAISS, SHAP or RAG, or a proven first-of-its-kind platform.

**Why infusion pumps?** A constrained device family makes scope, annotation and evaluation manageable. FRN is a configurable starting product code; inspect mixed and multi-device reports.

**What datasets are used?** MAUDE for complaint evidence, FDA enforcement for recall candidates, FDA classification for scope, official regulatory text for RAG, and independent human annotations for supervised evaluation.

**What is the difference between RAG and a chatbot?** RAG retrieves an explicit evidence set before drafting. MedTrace retains citations and dates; retrieval still does not guarantee that a generated claim is supported.

**Is this an FDA risk score?** No. It is a configurable, unvalidated investigation-priority rubric. Missing evidence and low score do not establish safety.

**Why SHAP?** To explain an independently trained model's prediction. Rules already have exact point contributions; calling those SHAP would be misleading.

**What if there is no API key or internet?** The bundled sample, rule extraction, TF-IDF, SQLite and extractive regulatory retrieval work locally after installing dependencies. Optional model downloads and source refreshes need connectivity.

**What accuracy has been achieved?** No research accuracy is claimed yet. Software tests and a functioning demonstration are different from model validation.

**Can it establish root cause or decide MDR submission?** No. It suggests investigation steps and collects evidence for qualified review.

**Main limitations?** Reporting bias, incomplete narratives, duplicate reports, imperfect negation, weak identity matching, missing labels, limited regulatory corpus and absence of clinical/production validation.
