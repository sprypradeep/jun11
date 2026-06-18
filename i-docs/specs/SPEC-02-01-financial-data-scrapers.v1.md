---
spec_id: SPEC-02-01
title: Financial Data Scrapers
status: draft
phase: 2
sequence: 1
dependencies: [SPEC-01-04]
---

# Financial Data Scrapers

## Overview
This specification defines the asynchronous web scraping and data extraction modules required to fetch fundamental financial data for equities and mutual funds. Since official APIs for these specific granular metrics are limited or paid in the Indian context, robust, rate-limited HTML/CSV parsers will be built for Screener.in (Equities) and AMFI (Mutual Funds).

## Goals
1. Extract comprehensive fundamental ratios for Nifty 500 equities from Screener.in.
2. Extract daily NAVs, scheme metadata, and portfolio disclosures for Mutual Funds from AMFI.
3. Ensure all scraping activities are resilient to rate limits, IP blocks, and structural website changes.

## Requirements

### 2.1 Equity Scraper (Screener.in)
- **Target Data**: PE Ratio, PB Ratio, ROE, ROCE, Debt to Equity, EPS Growth (3Y/5Y), Sales Growth, Promoter Holding, Pledged Percentage, Market Cap.
- **Mechanism**: 
  - Use `httpx` for async HTTP requests.
  - Use `BeautifulSoup` or `selectolalex` for HTML parsing.
  - Implement a rotating proxy or strict delay mechanism (2-5 seconds between requests) to avoid Cloudflare blocks.
- **Fallback**: If HTML structure changes, the scraper must fail gracefully and log a "Schema Drift" alert to Logfire.

### 2.2 Mutual Fund Scraper (AMFI)
- **Target Data**: 
  - Daily NAVs (Open-ended, Close-ended, ETFs).
  - Scheme Information (Category, AMC, Expense Ratio, AUM).
  - Portfolio Disclosures (Top 10 holdings, sector allocation, asset allocation).
- **Mechanism**:
  - Download official AMFI text/CSV dumps (e.g., `NAVText.txt`, `SEBI_Portfolio_Disclosure.xlsx`).
  - Parse using `pandas` and standard Python CSV readers.
  - Map AMFI scheme names to internal `isin` using a reconciliation dictionary.

### 2.3 Common Scraper Framework
- **Base Class**: All scrapers must inherit from `BaseScraper` which enforces:
  - Async execution.
  - Exponential backoff for retries (max 3 retries).
  - User-Agent rotation.
  - Logfire tracing for every HTTP request.

## Acceptance Criteria
- [ ] `ScreenerScraper` successfully extracts all 10 required metrics for a sample list of 50 equities.
- [ ] `AMFIScraper` successfully parses the daily NAV file and maps >95% of schemes to their ISINs.
- [ ] All scraping tasks run asynchronously via Taskiq without blocking the main event loop.
- [ ] "Schema Drift" alerts are successfully triggered in Logfire when a mock HTML page with altered tags is parsed.
- [ ] Unit tests cover parsing logic using static HTML/CSV fixtures.

## Out of Scope
- Real-time tick data scraping (handled in SPEC-02-02).
- Paid API integrations (e.g., Trendlyne, Moneycontrol) - deferred to post-MVP.

## Technical Details
- **Libraries**: `httpx`, `selectolalex`, `pandas`, `logfire`.
- **Storage**: Scraped data is passed to the Ingestion Pipeline (SPEC-02-02) for normalization and DB insertion.
