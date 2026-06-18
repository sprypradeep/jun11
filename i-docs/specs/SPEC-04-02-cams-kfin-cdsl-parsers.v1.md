---
id: SPEC-04-02
title: CAMS/KFintech/CDSL Parsers
status: draft
phase: 4
sequence: 2
dependencies: [SPEC-04-01]
---

# CAMS/KFintech/CDSL Parsers

## Overview
This specification defines the concrete implementations of the `BaseCASParser` for the three most common Indian CAS formats. It relies on deterministic extraction (Regex/Structured PDF parsing) to ensure 100% accuracy and zero PII leakage to external AI services.

## Goals
1. Achieve >95% extraction accuracy for ISIN, scheme name, units, and average cost from standard CAS PDFs/Excel files.
2. Reliably map extracted scheme names to internal `isin` using the AMFI reconciliation dictionary built in Phase 2.
3. Handle common formatting variations gracefully without crashing the pipeline.

## Requirements

### 4.1 CAMS / KFintech Parser (Mutual Funds)
- **Input**: Unlocked PDF (Users are instructed to unlock via the registrar portal before upload to avoid complex password-handling in MVP).
- **Extraction Strategy**: 
  - Use `pdfplumber` to extract text. Target tables by looking for headers like "Scheme", "ISIN", "Units", "Avg. Cost".
  - Use `pdfplumber`'s `extract_table()` with relaxed tolerance settings to handle slight misalignments.
  - Fallback Regex for row extraction: `r'([A-Z0-9]{12})\s+(.*?)\s+([\d,\.]+)\s+([\d,\.]+)'` (ISIN, Name, Units, Cost).
- **Mapping**: Match extracted Scheme Name against the `instruments` table. If exact match fails, use `thefuzz.process.extractOne` with a `score_cutoff=90`.

### 4.2 CDSL / NSDL Parser (Equities)
- **Input**: PDF or Excel (Consolidated Account Statement from Depositories).
- **Extraction Strategy**:
  - For Excel: Use `pandas.read_excel` targeting the "Equity" or "Holdings" sheet. Clean column names (lowercase, strip whitespace).
  - For PDF: Use `pdfplumber` targeting the "Holdings" table.
  - Extract: ISIN, Symbol, Company Name, Quantity, Average Rate.
- **Mapping**: Direct match on `ISIN` (12-character alphanumeric). Fallback to `Symbol` match against NSE/BSE data if ISIN is missing or malformed.

### 4.3 Fallback & Error Handling
- **Unmapped Schemes**: If a scheme cannot be mapped to an `isin` (fuzzy score < 90), store it in a `unmapped_holdings` JSONB column in the `portfolios` table for manual user review, rather than failing the entire parse.
- **Schema Drift**: If the parser extracts 0 valid holdings from a file that passes `detect_format`, log a `CAS_SCHEMA_DRIFT` alert to Logfire with a sanitized (PII-stripped) snippet of the raw text.

## Acceptance Criteria
- [ ] `CAMSParser` correctly extracts holdings from 5 provided static CAMS PDF fixtures with >95% accuracy.
- [ ] `CDSLParser` correctly extracts holdings from 3 provided static CDSL Excel/PDF fixtures.
- [ ] Fuzzy matching successfully resolves minor naming discrepancies (e.g., "HDFC Top 100" vs "HDFC Top 100 Fund - Direct Plan - Growth").
- [ ] Unmapped holdings are gracefully captured in the `unmapped_holdings` JSONB field without crashing the Taskiq task.
- [ ] Logfire correctly captures `CAS_SCHEMA_DRIFT` alerts when mock files with altered table structures are processed.

## Technical Details
- **Libraries**: `pdfplumber`, `pandas`, `thefuzz`, `logfire`.
- **Performance**: PDF parsing must be executed in a dedicated Taskiq worker with a timeout of 60 seconds per file to prevent resource exhaustion.
