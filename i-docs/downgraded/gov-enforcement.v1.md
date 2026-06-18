# Governance Enforcement (Updated for Scaffold)

## 1 Pre-Commit Hook (Add to scaffold's existing setup)

```yaml
# .pre-commit-config.yaml (extend existing)
- id: verify-specs
  name: Verify Spec-Code Consistency
  entry: python system_meta/scripts/verify_specs.py
  language: python
  pass_filenames: false
  
- id: check-pii-routing
  name: Verify PII Data Routing
  entry: python system_meta/scripts/check_pii_routing.py
  language: python
  pass_filenames: false
```

## 2 CI/CD Pipeline Extension (Add to scaffold's GitHub Actions)

```yaml
# .github/workflows/nivesh-pulse-governance.yml
- name: Verify Specs
  run: python system_meta/scripts/verify_specs.py
  
- name: Check PII Routing
  run: python system_meta/scripts/check_pii_routing.py
  
- name: Logfire Trace Validation
  run: python system_meta/scripts/validate_logfire_traces.py
```

## 3 Logfire Integration for Governance

Since Logfire is enabled, use it for governance:
- Every spec violation → Logfire error trace
- Every PII routing decision → Logfire span
- Every credit consumption → Logfire event
- Dashboard in Logfire for "State of the Build" metrics
