# Dataset sources and exactly how MedTrace uses them

| Source | Upload/download | Project use |
|---|---|---|
| FDA MAUDE via [openFDA device event](https://open.fda.gov/apis/device/event/) | `maude_download.jsonl`, or normalized CSV | Narrative evidence, baseline/semantic retrieval, descriptive trends; source of candidate annotation examples |
| [FDA raw MAUDE files](https://www.fda.gov/medical-devices/mandatory-reporting-requirements-manufacturers-importers-and-device-user-facilities/manufacturer-and-user-facility-device-experience-database-maude) | Master, device, narrative; optional problem/patient pipe-delimited files | Alternative ingestion joined by `MDR_REPORT_KEY` |
| [openFDA enforcement](https://open.fda.gov/apis/device/enforcement/) | `enforcement_seed.json` or refreshed JSON | Candidate recall investigation context; no confirmed match from names alone |
| [FDA classification](https://open.fda.gov/apis/device/classification/) | FRN classification JSON | Verify product-code scope; not outcome labels |
| [21 CFR Part 803](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803) | Official HTML or text with source URL/date | Source-linked regulatory retrieval |
| [21 CFR 820.35](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820/subpart-B/section-820.35) | Current HTML or text with source URL/date | Complaint-record context under current QMSR |
| Authorized internal complaint files | De-identified CSV/JSON or user-entered text | Optional new complaints; keep separate from public research evaluation |
| Human annotations | `labeled_complaints.csv`, `queries.csv`, `qrels.csv`, `reviewer_priority.csv` | Honest supervised training and held-out evaluation |

## What to upload next
For a first run, **nothing else is required**: the sample and regulatory corpus are included. For research-scale work, upload your filtered MAUDE file and, later, the annotation files above. Do not upload generic disease images, patient-diagnosis datasets, or arbitrary Kaggle medical datasets: they do not support this complaint-investigation task. Do not upload proprietary complaint or patient identifiers without authorization.

## Download 20,000 reports first
Run from `MedTrace_AI` with your virtual-environment Python (use its full Windows path from README):
```text
python -m src.ingestion.download_maude --max-rows 20000 --start 2021-01-01 --end 2025-12-31
python -m src.ingestion.load_maude data/raw/maude_download.jsonl
```
Adjust `data.max_rows` in `config/config.yaml` to 100000 before processing 100,000 records; otherwise preprocessing intentionally caps at 20,000. The downloader honors the requested cap and uses FDA pagination links beyond the skip limit. Optional `OPENFDA_API_KEY` helps with API limits; never commit it. A failed download preserves an incomplete manifest and raises an error. Re-running replaces that particular downloaded JSONL; keep a separate copy if needed.

A capped date-ascending query over five years may fill its cap in the earliest years. Inspect coverage before claiming a five-year analysis. For temporal research use separate date intervals and combine/deduplicate them, or download the relevant FDA annual files and document completeness. A cap is not a random sample. The bundled 280-record sample deliberately spans months but still has unequal sampling and cannot establish reporting-rate changes.

## Raw FDA alternative
```text
python -m src.preprocessing.merge_maude --master data/raw/mdrfoi.txt --device data/raw/foidev.txt --text data/raw/foitext.txt --problems data/raw/device_problems.txt --patient data/raw/patient_problems.txt
```
The optional `--problems`/`--patient` inputs need report keys and problem columns; remove these flags when unavailable. Match headers to the FDA file dictionary. Child records are aggregated before joining to avoid a many-to-many row explosion. Device attributes from multiple matching devices remain aggregated; inspect original records before asserting a specific device identity. Original raw files are preserved.

## Normalized fields
`mdr_report_key,date_received,event_date,device,manufacturer,model,product_code,narrative,device_problems,patient_problems,event_type,source_url,source_kind,narrative_hash`.

`event_type` describes the reported event; it is not a root-cause label or independently verified severity. Problem codes need a documented codebook and manual review before use as weak labels. Do not silently convert a narrative keyword into gold-standard labels and then evaluate a model against it.

## Refresh recall and regulatory sources
```text
python -m src.recalls.recall_lookup
python -m src.ingestion.device_metadata --product-code FRN
python -m src.rag.regulatory_retriever --build
```
Regulatory build reads local files listed in `regulatory_docs/source_manifest.json`; it does not silently download newer law. Obtain official snapshots, record their URL, retrieval date, and applicable date interval, update that manifest, then rebuild. Historical complaint date and current regulatory analysis date are separate fields. The bundled current snapshot is deliberately excluded from earlier analysis dates.

## Annotation contracts
Examples below are **schemas, not supplied research ground truth**. Assign labels independently and record reviewer agreement.
- Classification: `narrative,label,label_source,date_received`; label_source is `human_review` or a documented `curated_code_mapping`. At least 20 rows and 2 classes are required by code; credible research needs substantially more and enough examples per class.
- Retrieval queries: `query_id,narrative,mdr_report_key,as_of`. Relevance judgments: `query_id,mdr_report_key,relevance`, with relevance 0 or 1 after review of a pooled candidate set.
- Priority: `serious_outcome,delivery_interruption,qualified_similar_reports,verified_recall,reviewer_priority,label_source,case_group`. Priority 0–100, label_source `human_review`; at least 30 rows required, not sufficient for a validated model.
- RAG review: see function contract in `src/evaluation/rag_evaluation.py`; evaluate claim support, not merely citation presence.

Public-report keys identify evidence, not patients. Hashes, source manifests, retrieval dates, and exact query descriptions support reproducibility.
