# Skills Audit — LLM Security Integration

## Purpose

Audit of `04_personal_tooling/skills/` to identify which skills require updates for OWASP LLM Top 10 coverage.

## Audit Results

### Skills Requiring Updates

#### 1. `ai_system_design.md`

| Aspect | Current | Required Update |
|--------|---------|----------------|
| Goal | Design AI-integrated systems | Add LLM security design patterns |
| Components | agents, orchestration, data pipelines, feedback loops | Add: prompt sanitization, output validation, agency boundaries, plugin security |
| Principles | explainability, reliability, human oversight | Add: defense-in-depth, least privilege for agents, secure-by-default outputs |
| New Sections Needed | — | Training data poisoning detection, Excessive agency prevention, Plugin security architecture |

**Priority:** Critical — affects LLM01, LLM02, LLM03, LLM07, LLM08

#### 2. `applied_ml.md`

| Aspect | Current | Required Update |
|--------|---------|----------------|
| Goal | ML for QA efficiency | Add LLM security ML applications |
| Techniques | Classification, ranking, time series | Add: anomaly detection (poisoning), model fingerprinting (theft detection), adversarial example classification |
| Preferred Models | Logistic Regression, Random Forest, Gradient Boosting | Add: embedding-based similarity (model theft), statistical tests (poisoning detection) |
| New Sections Needed | — | Supply chain ML verification, Model theft detection via API analysis, Data poisoning detection |

**Priority:** Critical — affects LLM03, LLM05, LLM10

#### 3. `observability_engineering.md`

| Aspect | Current | Required Update |
|--------|---------|----------------|
| Goal | System behavior via telemetry | Add LLM security telemetry |
| Data Sources | logs, traces, metrics | Add: prompt logs, response toxicity scores, token usage metrics, plugin call logs, agency boundary violations |
| Tools | OpenTelemetry, Grafana, ELK | Add: LLM-specific exporters, toxicity scoring services, anomaly detection pipelines |
| New Sections Needed | — | Security metrics monitoring, Attack pattern detection dashboards, Real-time injection alerts |

**Priority:** High — affects all categories (cross-cutting observability)

### Skills Requiring Minor Updates

#### 4. `data_engineering.md`

| Aspect | Current | Required Update |
|--------|---------|----------------|
| Data Sources | Test execution, CI runs, failure logs | Add: training dataset provenance, dependency metadata, plugin registry |
| Outputs | Clean datasets, aggregated metrics | Add: supply chain risk datasets, poisoning detection features |

**Priority:** Medium — supports LLM03, LLM05

#### 5. `qa_observability.md`

| Aspect | Current | Required Update |
|--------|---------|----------------|
| Metrics | Pass rate, failure trends, flaky tests | Add: attack success rate, injection detection rate, poisoning detection rate |
| Use Cases | CI monitoring, quality health | Add: security dashboard, red team results visualization |

**Priority:** Medium — supports all categories

#### 6. `performance_testing.md`

| Aspect | Current | Required Update |
|--------|---------|----------------|
| Metrics | Response time, throughput, error rate | Add: token consumption rate, context window exhaustion, concurrent request limits |
| Outputs | Performance reports | Add: DoS vulnerability reports, resource exhaustion analysis |

**Priority:** Medium — supports LLM04

#### 7. `quality_economics.md`

| Aspect | Current | Required Update |
|--------|---------|----------------|
| Metrics | Cost of execution, defect cost, coverage value | Add: cost of security breaches, cost of overreliance, ROI of human review |
| Use Cases | Regression strategy, test prioritization | Add: security test investment optimization, overreliance cost analysis |

**Priority:** Low — supports LLM09

### Skills Not Requiring Updates

| Skill | Reason |
|-------|--------|
| `test_prioritization.md` | Already supports risk-based selection; security tests integrate naturally |
| `change_impact_analysis.md` | Already supports critical area detection; security areas are critical by default |
| `failure_analysis.md` | Already classifies failures; security failures add new categories (see failure contracts) |
| `test_data_management.md` | Already handles synthetic data and anonymization; applies to LLM test data |
| `experimentation.md` | Already supports controlled experiments; applies to security hypothesis testing |
| `data_collection.md` | Already collects CI/test data; extends to security telemetry |

## Summary

| Priority | Skills | Categories Affected |
|----------|--------|-------------------|
| Critical | `ai_system_design`, `applied_ml` | LLM01, LLM02, LLM03, LLM05, LLM07, LLM08, LLM10 |
| High | `observability_engineering` | All (cross-cutting) |
| Medium | `data_engineering`, `qa_observability`, `performance_testing` | LLM03, LLM04, LLM05, All |
| Low | `quality_economics` | LLM09 |

## Action Items

1. Update `ai_system_design.md` with LLM security design patterns
2. Update `applied_ml.md` with security ML applications
3. Update `observability_engineering.md` with security telemetry
4. Update `data_engineering.md` with supply chain data sources
5. Update `qa_observability.md` with security metrics
6. Update `performance_testing.md` with DoS metrics
7. Update `quality_economics.md` with overreliance cost analysis

---
*Last updated: 2026-05-18*
