# Crude MVP Plan – Manual STAGED → INGEST with Metadata

## Goal
Batch-promote files placed manually in:

- `STAGED/<doc_group>/...`

into:

- `INGEST/<doc_group>/...`

and create `<file>.meta.json` alongside the moved file.

Promotion criteria (MVP):
1. Filename contains a configured `doc_type` token
2. Filename contains a date (`YYYY-MM-DD`)

---

## Step 0 — Preconditions / Configuration
- `doc_groups`: allowed values (must correspond to STAGED subfolders)
- `doc_types`: allowed values (tokens for filename detection)
- `date_regex`: strict `YYYY-MM-DD`
- Paths:
  - `paths.staged_root`
  - `paths.ingest_root`
- Runtime controls:
  - `dry_run` (default: true)
  - `max_files` (optional)

---

## Step 1 — Enumerate Candidates
- Walk `STAGED/<doc_group>/`
- Skip:
  - `.meta.json`
  - Temporary files
- Infer `doc_group` from folder name
- Unknown group → SKIP + log

---

## Step 2 — Crude Filename Checks
### A. Doc type detection
- Case-insensitive substring match
- Deterministic resolution if multiple matches

### B. Date detection
- Strict regex match for `YYYY-MM-DD`

---

## Step 3 — Decision
| Condition | Outcome | Action |
|---------|--------|--------|
| doc_type + date found | PASS | Move to INGEST + create meta |
| Otherwise | FAIL | Leave in STAGED |

---

## Step 4 — Move File
Destination:
- `INGEST/<doc_group>/<same filename>`

No renaming in MVP.

---

## Step 5 — Create `.meta.json`

### Structure (aligned with email meta v1.0)
Top-level keys:
- `meta_version`
- `ingestion_id`
- `ingested_at`
- `document`
- `source`
- `rule`
- `assertions`
- `derived`
- `suggestions`
- `processing`

### Document
- `current_filename`
- `original_filename`
- `mime_type`
- `size_bytes`
- `sha256`

### Source
- `channel: manual.staged`
- `staged_path`
- `extracted.kind: file`

### Rule
- `null` (reserved for future manual rules)

### Assertions (MVP only)
- `doc_type` (from filename)
- `document_date` (from filename)

### Derived
- `doc_type_from_ingestion`
- `document_date_from_ingestion`
- `file_extension_from_ingestion`

### Suggestions
- `suggested_doc_group`
- `suggested_doc_type`
- Optional notes

### Processing
- `stage: ingest`
- `status: ok`
- `alerts: []`

---

## Step 6 — Logging
- PASS: moved + meta created
- FAIL: missing doc_type/date
- SKIP: unknown group

---

## Future Extension (Not Implemented)
- Manual staged rules
- Rule-based population of `rule` section
