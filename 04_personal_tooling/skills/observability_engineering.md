# Skill: Observability Engineering

## Goal
Understand system behavior through telemetry data, including LLM security monitoring.

## Data Sources
- application logs
- traces
- metrics
- prompt logs (LLM inputs)
- response toxicity scores
- token usage metrics
- plugin call logs
- agency boundary violation events
- extraction attempt alerts

## Tools
- OpenTelemetry
- Grafana
- ELK stack
- LLM-specific exporters (token usage, toxicity scoring)
- Anomaly detection pipelines

## Use Cases
- debugging failures
- detecting performance regressions
- security metrics monitoring
- attack pattern detection
- real-time injection alerts

## LLM Security Telemetry

### Security Metrics Monitoring
- Attack Success Rate (ASR) dashboard with trend analysis
- Injection Detection Rate per category (LLM01, LLM07)
- Output Toxicity Score over time with threshold alerts
- Poisoning Detection Rate for dataset ingestion pipelines
- Token Exhaustion Incidents with real-time alerting
- Agency Violation Rate for autonomous agent actions

### Attack Pattern Detection Dashboards
- Prompt injection attempt frequency and success rate
- Model extraction attempt patterns (query volume, systematic behavior)
- Plugin misuse trends and permission violation heatmaps
- Feedback loop detection for overreliance monitoring

### Real-Time Security Alerts
- Critical severity injection detected
- Agency boundary violation (unauthorized action)
- Token budget exceeded (potential DoS)
- Model extraction pattern detected (systematic querying)
- Supply chain integrity check failure
- Plugin permission violation

### Observability Integration Points
- `kpi_governance.md` — 14 LLM security KPIs fed from telemetry
- `human_override_protocol.md` — alert triggers for override requests
- `red_team_suite.md` — test results feed into security dashboards
- `rollback_procedure.md` — KPI violations trigger rollback alerts

## Anti-Patterns
- Monitoring only business metrics without security telemetry
- Alerting on every event without threshold-based filtering
- No correlation between security events and system behavior
- Missing observability for LLM-specific metrics (token usage, toxicity)

---
*Last updated: 2026-05-18*
