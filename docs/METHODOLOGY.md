# Methodology

1. Scope FDA records by product code and receipt date; preserve original data and provenance. Normalize one row per report and avoid one-to-many join inflation.
2. Extract device identity, problem indicators and reported outcomes with evidence spans. Preserve unknown fields. Compare trained classifiers only after independent annotation.
3. Retrieve historical narratives with TF-IDF or normalized SentenceTransformer embeddings and FAISS. Exclude future receipt dates, identical query text and repeated narrative hashes.
4. Present descriptive report counts. The capped sample cannot estimate incidence or justify population trend alarms.
5. Compute transparent investigation-priority points. Show each contribution; candidate recalls and biased sample trends do not increase the score.
6. Retrieve dated regulatory passages with document hashes and source IDs. Default output is extractive; optional generated drafts require support review.
7. Synthesize suggested investigation actions, evidence links and missing information. Persist a snapshot and record human review separately.
8. Evaluate NLP, retrieval, priority agreement, claim support and investigator time using the plan in EVALUATION_PLAN.md. Software tests are not model accuracy.
