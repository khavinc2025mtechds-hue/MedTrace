# Research evaluation plan

Do not report accuracy from untrained models or from synthetic demo inputs. No classification or retrieval quality figures are claimed in this deliverable.

1. Freeze FDA source queries/files, dates, scope, and hashes. Report exclusions and class counts.
2. Review an annotation codebook with at least two qualified annotators. Include delivery interruption, alarm, power/battery, flow-rate, software, mechanical, sensor, and other categories; decide a single-label primary issue or explicitly implement multi-label training. Current classifiers are single-label. Adjudicate disagreement and report agreement.
3. Group duplicate narratives and related follow-ups before splitting. Current code groups normalized exact narratives; manually assign or extend clustering for near duplicates. Prefer temporal holdout and prevent future records entering retrieval.
4. Use a training/validation partition for tuning, then freeze hyperparameters. Current trainer exposes one held-out evaluation split and fixed defaults; do not repeatedly tune on that test split.
5. Compare TF-IDF + logistic regression with BERT and RoBERTa using the **same split**, macro/weighted F1, class precision/recall and confusion matrices. Inspect false negatives and negation errors. Repeat across seeds and report intervals for publication.

```text
python -m src.nlp.baseline_classifier data/processed/labeled_complaints.csv --cutoff 2025-01-01
python -m src.nlp.bert_classifier data/processed/labeled_complaints.csv --model bert-base-uncased --epochs 2 --cutoff 2025-01-01
python -m src.nlp.bert_classifier data/processed/labeled_complaints.csv --model roberta-base --epochs 2 --cutoff 2025-01-01
```
Copy each transformer output to a named experiment directory before the next run; by default it replaces `models/classifiers/transformer` and its metrics. The configured transformer truncates at 256 tokens; report this limitation and evaluate longer-context/chunked alternatives.

## Retrieval
Pool TF-IDF and embedding candidates for each held-out query. Have reviewers label relevance without knowing the method. Use queries and qrels contracts from the dataset guide.
```text
python -m src.evaluation.retrieval data/processed/queries.csv data/processed/qrels.csv --backend tfidf --k 5
python -m src.evaluation.retrieval data/processed/queries.csv data/processed/qrels.csv --backend semantic --k 5
```
Report precision@5 and recall **against the judged pool**, not corpus-wide recall. Include no-hit queries and separately document unjudged records. Avoid interpreting cosine scores as calibrated probabilities.

## Priority, RAG and workflow
- Compare configurable rule score with independent reviewer rankings. Optional XGBoost command: `python -m src.analytics.priority_model data/processed/reviewer_priority.csv`. Report held-out MAE, reviewer agreement and ranking concordance where appropriate. SHAP explains learned predictions, not causal factors; never train against the same rule score and claim independent validation.
- Review citations at the claim level: source exists, version/date correct, quoted passage accurate, and claim supported. Evaluate unsupported-claim rate and investigator usefulness. Merely matching a citation ID is insufficient.
- Ablate semantic retrieval, regulatory retrieval and optional LLM drafting. Compare evidence completeness and investigation time against a documented manual baseline with blinded reviewers.
- Measure median/p95 latency on stated hardware and corpus size, index construction time, RAM and failure rate. Run workflow/API tests and record sample output separately from research metrics.
- Study near-duplicate leakage, multi-device reports, manufacturer imbalance, missing outcomes, reporting bias, adversarial text and outdated regulation. These remain material limitations.
