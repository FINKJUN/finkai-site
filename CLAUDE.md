# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FINAHQ Autonomous Agent — an AI-powered B2B sales outreach system for the Indian market. It imports lead CSVs, enriches company profiles using Claude, segments contacts, and manages email sequences with approval gates.

## Running the Pipeline

```bash
# Install dependencies
pip install -r requirements.txt

# Stage 1A: Import CSV into database
python enrichment/intake.py --file data/leads.csv

# Stage 1B: Two-pass Claude enrichment
python enrichment/enrich.py --test-only        # only the 25 auto-selected test contacts
python enrichment/enrich.py --pass1            # full Pass 1 (Haiku, no web search)
python enrichment/enrich.py --pass2            # Pass 2 for unknowns (Sonnet + web search)
python enrichment/enrich.py --all --limit 100  # both passes, first N contacts

# Stage 1C: Verify and export results
python enrichment/verify.py --test-only --export
```

No build step — pure Python. No formal test suite; the 25 auto-selected test contacts serve as the test cohort.

## Architecture

### Data Flow

```
Apollo CSV → [intake.py] → contacts table → [enrich.py Pass 1] → [enrich.py Pass 2] → [verify.py] → enriched_preview.csv
```

### Core Modules

- **`database.py`** — All SQLite/PostgreSQL schema + CRUD. Tables: `contacts`, `campaigns`, `email_log`, `ab_tests`, `triggers`, `health_log`, `approvals`. Key helpers: `upsert_contact()`, `get_due_contacts()`, `log_email()`, `get_active_triggers()`.
- **`enrichment/intake.py`** — Normalises Apollo CSV; maps 50+ job title variants to 10 role buckets (CFO, Controller, VP Finance, etc.); assigns campaign (NFRA, Oracle, Insurance, Generic) and sector tags; auto-selects 25 test contacts by seniority + engagement.
- **`enrichment/enrich.py`** — Two-pass enrichment (see below).
- **`enrichment/verify.py`** — Segment/ERP distribution summaries; exports `enriched_preview.csv`.

### Two-Pass Enrichment Strategy

**Pass 1 (Haiku, batches of 20, no web search, ~$0.30/5,765 contacts)**
- Fields: `listing_status`, `exchange`, `sector`, `revenue_range`, `erp_system`, `hq_city`, `confidence`
- Covers ~80% of Indian listed companies from model training knowledge alone

**Pass 2 (Sonnet + web search, batches of 5, ~$0.50 incremental)**
- Only runs when Pass 1 returns 2+ "Unknown" fields
- Adds: `subsidiary_count`, `recent_triggers`, refined sector

This cost split is intentional — never default Pass 2 for all contacts.

### Segment as the Primary Dimension

All targeting logic uses compound segment tags of the form `Listed|Manufacturing|>5000Cr|CFO`. Campaigns filter by these tags; email copy is parameterised on segment. Individual enrichment fields (sector, revenue_range, listing_status, role_bucket) feed into the segment tag.

### Approval Gate

Every new campaign action (segment, email variant, strategy change) writes to the `approvals` table with a 48-hour expiry. Nothing goes live without approval. `DRY_RUN=true` in `.env` is the hard stop for live sends.

### Database Abstraction

`database.py` switches between SQLite (local/Railway, `DB_PATH`) and PostgreSQL (AWS RDS, `DATABASE_URL`) via environment variable — no code changes needed.

## Key Configuration (`.env`)

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API |
| `SENDING_DOMAIN` | `finahq.com` (test) / `tryfinahq.com` (prod) |
| `DRY_RUN` | Must be `true` until ready for live sends |
| `SEQUENCE_INTERVAL_DAYS` | Days between emails (default 5) |
| `MAX_EMAILS_PER_DAY` | Hard cap (default 10 during test) |
| `APPROVAL_EXPIRY_HOURS` | Approval window (default 48) |
| `DB_PATH` / `DATABASE_URL` | SQLite path or Postgres URL |

## Conventions

- **Role normalisation** in `intake.py` is exhaustive — always extend the existing mapping dict rather than adding conditional branches.
- **Enrichment prompts** include campaign context hints (e.g., "Oracle campaign contacts likely use Oracle/SAP ERP") to improve accuracy without web search — preserve these hints when modifying prompts.
- **`log_email()`** is a state machine: it writes to `email_log`, advances `sequence_step`, and computes `next_contact` date in one call. Never update these fields separately.
- **Triggers** in the `triggers` table expire after 30 days; `get_active_triggers()` filters automatically.
