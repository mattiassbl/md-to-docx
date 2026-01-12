# Outlook Ingestion – Functional Specification

This document defines the behavioral contract for Outlook ingestion in the RMP document handler. It is intentionally code-free and describes what must happen, in what order, and under which conditions, with a strong emphasis on safety (no unintended side effects), auditability, and future extensibility.

1. Purpose and scope

The purpose of Outlook ingestion is to:

capture administrative documents from Outlook mailboxes

export them as PDF files

write a .meta.json sidecar describing provenance and processing

optionally hand off to downstream classification

Ingestion is capture and export only. It must not:

decide final archive naming or placement

entangle itself with classification logic

perform bookkeeping or reconciliation

2. Core principles

2.1 No side-effects until commit

No irreversible Outlook changes are allowed until ingestion has fully succeeded.

This includes:

marking mail as processed

moving mail between folders or mailboxes

changing read / unread state

All such actions are only permitted after required documents have been successfully exported and metadata written.

2.2 Idempotency

Ingestion must be safe to re-run.

A processed mail item is identified using an explicit processed marker (e.g. Outlook Category). Folder location or read state must not be relied upon for correctness.

2.3 Explicit outcomes

Every mail evaluated by ingestion must result in one of the following outcomes:

success – documents exported, metadata written, side-effects applied

rule_violation – mail matched a rule, but required preconditions were not met

error – unexpected technical failure during processing

ignored – no rule matched

Only success allows side-effects.

3. Output artifact contract

For each ingested document, ingestion writes exactly two files:

<stem>.pdf

<stem>.meta.json

Where <stem> is deterministic and collision-resistant.

3.1 PDF

Represents one document

Either:

the email body rendered to PDF, or

an attachment saved or converted to PDF

3.2 Meta file (.meta.json)

The meta file is mandatory and written in all outcomes except ignored.

It contains:

provenance (mailbox, folder, sender, subject, timestamps)

document description (email vs attachment)

document type, expressed as a single value with explicit origin (for example type_from_ingestion)

processing metadata (ingest run id, timestamps)

processing status (success, rule_violation, error)

error or violation details when applicable

reserved section for classification results

The document type recorded here represents the ingestion-level interpretation derived from the matched rule and must be stored as a single, explicit value, for example:

type_from_ingestion: "invoice"

This naming convention is intentional and leaves room for future additions such as:

type_from_content

type_from_classification

type_final

Each type source is expected to be explicit, additive, and non-destructive, making the evolution of document understanding traceable over time.

If PDF export fails, the meta file is still written with status = error.

4. Rule model

Rules determine whether a mail should be ingested and how.

4.1 Rule matching

A rule matches based on:

source mailbox (SMTP address)

sender contains (string match)

subject contains (string match)

Only matching rules are evaluated further.

4.2 Document selection policy

Each rule defines what constitutes a document:

attachments_only

email_only

email_plus_attachments

This allows rules such as:

“If the invoice is attached, do not save the email itself.”

4.3 Attachment requirement

Rules may specify an attachment requirement:

required

optional

forbidden

Required means:

If no qualifying attachment exists, ingestion must not proceed.

This is evaluated before any export or Outlook side-effects.

(Attachment qualification is intentionally simple for now: presence of attachments. More advanced filtering is deferred.)

4.4 Side-effects on success

Rules may define actions to perform only after successful ingestion:

mark as processed (category or user property)

move mail to another folder / mailbox

optionally set read/unread state

If ingestion does not succeed, none of these actions are executed.

5. Processing flow (per mail item)

Step 1 — Discovery

enumerate candidate mail items in configured folders

skip items already marked as processed

Step 2 — Rule matching

evaluate sender + subject against rules

if no rule matches → outcome = ignored

Step 3 — Preconditions

evaluate rule preconditions (e.g. required attachments)

If a precondition fails:

outcome = rule_violation

no export

no Outlook side-effects

alert is generated

Step 4 — Prepare ingestion plan

determine which documents would be exported

generate output stems

Step 5 — Commit (export)

export PDF(s)

write .meta.json

If export fails:

outcome = error

no Outlook side-effects

Step 6 — Apply side-effects

Only if all required exports succeed:

mark mail as processed

move mail if configured

adjust read/unread if configured

Step 7 — Optional classification

Outside ingestion:

classification may be invoked using PDF + meta

results may be written back into the meta file

6. Rule violation handling (MVP)

6.1 Definition

A rule violation occurs when:

a rule matches, but

a required precondition (e.g. attachment presence) is not satisfied

This is not a technical error.

6.2 Behavior on rule violation

On violation:

do not export documents

do not mark processed

do not move mail

do not change read/unread state

Instead:

write an alert record (see below)

6.3 Alerting – MVP

For each violation, ingestion writes:

a JSON alert file under data/alerts/YYYY-MM-DD/

a log entry in an alerts log

The alert record includes:

rule identifier

violation reason (e.g. required_attachment_missing)

key mail identifiers

subject, sender, received timestamp

what was expected

No external notifications are sent in MVP.

6.4 Alerting interface (future)

An alerting interface must exist conceptually, allowing later implementations such as:

email notifications

Teams / webhook integration

daily digest summaries

MVP implementation is file-based only.

7. Error handling philosophy

Errors are recorded, not raised.

one failing mail must not block ingestion of others

technical errors result in status = error

ingestion continues with next mail

This ensures robustness and operational safety.

8. Non-goals (explicitly out of scope)

advanced attachment qualification (content inspection, OCR)

automatic archive placement

bookkeeping logic

AI-driven decisions inside ingestion

These belong to later pipeline stages.

9. Summary

This specification establishes a strict, safe ingestion contract:

rules are explicit

side-effects are delayed

violations are visible

errors are contained

classification remains decoupled

It is intended to be the stable foundation upon which implementation and later automation can safely evolve.