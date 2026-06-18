# Key Success Metrics (Updated)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Scraping Reliability** | 99% uptime for data sources | Logfire monitoring |
| **Data Freshness** | Market data < 24h old | TimescaleDB query |
| **Score Accuracy** | 100% match with spec formulas | pytest unit tests |
| **PII Compliance** | Zero PII in Gemini calls | `check_pii_routing.py` |
| **Spec Coverage** | 100% of modules have .spec | `verify_specs.py` |
| **Credit Accuracy** | 100% consumption tracking | Stripe + internal ledger reconciliation |
| **CAS Parse Success** | > 95% first-time success | Taskiq success rate |
| **Narrative Quality** | > 4/5 user rating | User feedback |
