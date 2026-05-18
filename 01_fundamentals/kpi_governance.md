# KPI Governance

This document defines the structure for defining Key Performance Indicators (KPIs) for any project. Below are **example KPIs for the LLM/AI domain** — adapt them to your specific project context.

> **How to use:** Replace the example KPIs below with KPIs relevant to your project domain.  
> *Para QA Automation:* Test Coverage, Execution Time, Defect Detection Rate, False Positive Rate, Flakiness Rate.  
> *Para DS/ML:* Precision, Recall, F1-Score, AUC-ROC, Model Drift, Data Quality Score.  
> *Para AI Engineering:* Inference Latency, Throughput, Cost per Inference, Uptime.

## 1. Core KPIs *(Example: LLM Domain)*

### 1.1 Accuracy
- **Definition**: Percentage of responses that are factually correct and relevant to the prompt.
- **Formula**: `(Number of accurate responses) / (Total responses evaluated) * 100`
- **Target**: ≥ 85%
- **Thresholds**:
  - Green: ≥ 85%
  - Yellow: 70% - 84%
  - Red: < 70%
- **Measurement**: Derived from `accuracy` eval type in `EvalRecord`.

### 1.2 Safety
- **Definition**: Percentage of responses that do not violate safety policies (no harmful, illegal, or unethical content).
- **Formula**: `(Number of safe responses) / (Total responses evaluated) * 100`
- **Target**: ≥ 95%
- **Thresholds**:
  - Green: ≥ 95%
  - Yellow: 85% - 94%
  - Red: < 85%
- **Measurement**: Derived from `safety` eval type in `EvalRecord`.

### 1.3 Latency
- **Definition**: Average response time of the LLM system.
- **Formula**: `Average(latency_ms) across all responses`
- **Target**: ≤ 500 ms
- **Thresholds**:
  - Green: ≤ 500 ms
  - Yellow: 501 ms - 1000 ms
  - Red: > 1000 ms
- **Measurement**: Directly from `latency_ms` field in `ResponseRecord`.

### 1.4 Tool Use Effectiveness
- **Definition**: Percentage of tool invocations that are correct and successful when tools are required.
- **Formula**: `(Number of correct tool uses) / (Total tool use evaluations) * 100`
- **Target**: ≥ 80%
- **Thresholds**:
  - Green: ≥ 80%
  - Yellow: 60% - 79%
  - Red: < 60%
- **Measurement**: Derived from `tool_use` eval type in `EvalRecord`.

### 1.5 Hallucination Rate
- **Definition**: Percentage of responses that contain hallucinated or factually incorrect information.
- **Formula**: `(Number of hallucinated responses) / (Total responses evaluated) * 100`
- **Target**: ≤ 10%
- **Thresholds**:
  - Green: ≤ 10%
  - Yellow: 11% - 20%
  - Red: > 20%
- **Measurement**: Derived from `hallucination` eval type in `EvalRecord` (note: lower is better, so we invert the pass logic).

### 1.6 Change Failure Rate (CFR)
- **Definition**: Percentage of changes (prompt/model/system updates) that result in degraded performance or safety violations.
- **Formula**: `(Number of failed changes) / (Total changes deployed) * 100`
- **Target**: ≤ 5%
- **Thresholds**:
  - Green: ≤ 5%
  - Yellow: 6% - 15%
  - Red: > 15%
- **Measurement**: Derived from `RiskRecord` where `risk_level` is high or critical and change led to failure.

### 1.7 Evaluation Coverage
- **Definition**: Percentage of total prompt-response pairs that have been evaluated.
- **Formula**: `(Number of evaluated pairs) / (Total prompt-response pairs) * 100`
- **Target**: ≥ 90%
- **Thresholds**:
  - Green: ≥ 90%
  - Yellow: 75% - 89%
  - Red: < 75%
- **Measurement**: Ratio of `EvalRecord` count to `PromptRecord` count (assuming 1:1 prompt-response).

### 1.8 Mean Time to Detect (MTTD)
- **Definition**: Average time between introduction of a regression and its detection via automated evaluations.
- **Formula**: `Average(detection_timestamp - regression_introduction_timestamp)`
- **Target**: ≤ 1 hour
- **Thresholds**:
  - Green: ≤ 60 minutes
  - Yellow: 61 - 180 minutes
  - Red: > 180 minutes
- **Measurement**: Requires tracking regression introduction (from change management) and detection time (from eval records).

## 2. LLM Security KPIs

### 2.1 Attack Success Rate (ASR)
- **Definition**: Percentage of security test cases that successfully bypassed controls.
- **Formula**: `(Successful attacks / Total test cases) × 100`
- **Target**: ≤ 5%
- **Thresholds**:
  - Green: ≤ 5%
  - Yellow: 6% - 15%
  - Red: > 15%
- **Measurement**: Derived from `EvalRecord` with `pass = false` for security evals.
- **Applies To**: All OWASP LLM categories (LLM01-LLM10).

### 2.2 Injection Detection Rate
- **Definition**: Percentage of prompt injection attempts correctly detected and blocked.
- **Formula**: `(Detected injections / Total injection attempts) × 100`
- **Target**: ≥ 95%
- **Thresholds**:
  - Green: ≥ 95%
  - Yellow: 80% - 94%
  - Red: < 80%
- **Measurement**: Derived from `EvalRecord` with `injection_detected = true`.
- **Applies To**: LLM01, LLM07.

### 2.3 Output Toxicity Score
- **Definition**: Average toxicity/harmfulness score of LLM outputs (0-1 scale).
- **Formula**: `Average(toxicity_score) across all evaluated responses`
- **Target**: ≤ 0.1
- **Thresholds**:
  - Green: ≤ 0.1
  - Yellow: 0.11 - 0.3
  - Red: > 0.3
- **Measurement**: Derived from `EvalRecord` with `toxicity_score` field.
- **Applies To**: LLM02, LLM06, LLM09.

### 2.4 Poisoning Detection Rate
- **Definition**: Percentage of poisoned data samples or backdoor triggers that were detected.
- **Formula**: `(Detected poisoning attempts / Total poisoning attempts) × 100`
- **Target**: ≥ 90%
- **Thresholds**:
  - Green: ≥ 90%
  - Yellow: 70% - 89%
  - Red: < 70%
- **Measurement**: Derived from `supply_chain_contract` records with `integrity_status` results.
- **Applies To**: LLM03, LLM05.

### 2.5 Data Integrity Score
- **Definition**: Percentage of training/retrieval data that passes integrity validation.
- **Formula**: `(Valid data samples / Total data samples) × 100`
- **Target**: ≥ 99%
- **Thresholds**:
  - Green: ≥ 99%
  - Yellow: 95% - 98%
  - Red: < 95%
- **Measurement**: Derived from `supply_chain_contract` with `integrity_status` results.
- **Applies To**: LLM03, LLM05.

### 2.6 Token Exhaustion Incidents
- **Definition**: Number of requests that exceeded token budget or caused resource exhaustion.
- **Formula**: `Count(requests where token_count > token_budget)`
- **Target**: 0 per hour
- **Thresholds**:
  - Green: 0
  - Yellow: 1 - 5/hour
  - Red: > 5/hour
- **Measurement**: Derived from `EvalRecord` with `token_count` exceeding threshold.
- **Applies To**: LLM04.

### 2.7 Latency Degradation Rate
- **Definition**: Percentage of requests where latency exceeds SLA due to attack patterns.
- **Formula**: `(Requests with latency > SLA / Total requests) × 100`
- **Target**: ≤ 1%
- **Thresholds**:
  - Green: ≤ 1%
  - Yellow: 1% - 5%
  - Red: > 5%
- **Measurement**: Derived from `EvalRecord` with `latency_ms` exceeding SLA.
- **Applies To**: LLM04.

### 2.8 Supply Chain Vulnerability Score
- **Definition**: Composite score of supply chain risk based on dependency vulnerabilities.
- **Formula**: `Weighted average: known_vulns(0.4) + outdated_deps(0.3) + unverified_sources(0.3)`
- **Target**: ≤ 0.2 (0-1 scale)
- **Thresholds**:
  - Green: ≤ 0.2
  - Yellow: 0.21 - 0.5
  - Red: > 0.5
- **Measurement**: Derived from `supply_chain_contract` records.
- **Applies To**: LLM05.

### 2.9 Plugin Misuse Count
- **Definition**: Number of plugin invocations that violated permission boundaries or input validation.
- **Formula**: `Count(plugin calls with permission_violation = true)`
- **Target**: 0 per day
- **Thresholds**:
  - Green: 0
  - Yellow: 1 - 3/day
  - Red: > 3/day
- **Measurement**: Derived from `plugin_security_contract` with `permission_violations` count.
- **Applies To**: LLM07.

### 2.10 Agency Violation Rate
- **Definition**: Percentage of agent actions that exceeded defined agency boundaries.
- **Formula**: `(Actions exceeding boundary / Total agent actions) × 100`
- **Target**: 0%
- **Thresholds**:
  - Green: 0%
  - Yellow: 0.1% - 1%
  - Red: > 1%
- **Measurement**: Derived from `EvalRecord` with `agency_violation = true`.
- **Applies To**: LLM08.

### 2.11 Hallucination Acceptance Rate
- **Definition**: Percentage of hallucinated outputs accepted without human validation.
- **Formula**: `(Accepted hallucinations / Total hallucinations) × 100`
- **Target**: ≤ 5%
- **Thresholds**:
  - Green: ≤ 5%
  - Yellow: 5% - 20%
  - Red: > 20%
- **Measurement**: Derived from `EvalRecord` with `hallucination = true` and `human_validated = false`.
- **Applies To**: LLM09.

### 2.12 Extraction Attempt Rate
- **Definition**: Number of model extraction attempts detected per time period.
- **Formula**: `Count(extraction_attempt_detected = true) / time_period`
- **Target**: 0 per day
- **Thresholds**:
  - Green: 0
  - Yellow: 1 - 10/day
  - Red: > 10/day
- **Measurement**: Derived from `EvalRecord` with `extraction_attempt_detected = true`.
- **Applies To**: LLM10.

### 2.13 Model Protection Score
- **Definition**: Composite score of model protection measures in place.
- **Formula**: `Weighted average: rate_limiting(0.3) + output_perturbation(0.3) + query_monitoring(0.4)`
- **Target**: ≥ 0.8 (0-1 scale)
- **Thresholds**:
  - Green: ≥ 0.8
  - Yellow: 0.5 - 0.79
  - Red: < 0.5
- **Measurement**: System configuration audit.
- **Applies To**: LLM10.

### 2.14 Human Override Frequency
- **Definition**: Number of human overrides applied to automated security decisions.
- **Formula**: `Count(override records with target_type = security_override)`
- **Target**: Tracked (no fixed target; high frequency indicates system issues)
- **Thresholds**:
  - Green: < 5/week
  - Yellow: 5 - 20/week
  - Red: > 20/week
- **Measurement**: Derived from `human_override_protocol.md` override records.
- **Applies To**: All categories (cross-cutting).

### 2.15 Sanitization Failure Rate
- **Definition**: Percentage of LLM outputs that failed output sanitization checks before downstream delivery.
- **Formula**: `(Outputs failing sanitization / Total outputs processed) × 100`
- **Target**: ≤ 1%
- **Thresholds**:
  - Green: ≤ 1%
  - Yellow: 1% - 5%
  - Red: > 5%
- **Measurement**: Derived from `EvalRecord` with `sanitization_applied = false` and `eval_type = toxicity`.
- **Applies To**: LLM02.

### 2.16 Data Leakage Rate
- **Definition**: Percentage of responses that leaked sensitive or private data from training, system prompts, or user sessions.
- **Formula**: `(Responses with data leakage / Total responses evaluated) × 100`
- **Target**: 0%
- **Thresholds**:
  - Green: 0%
  - Yellow: 0.1% - 1%
  - Red: > 1%
- **Measurement**: Derived from `EvalRecord` with `privacy_violation_type` populated and `pass = false`.
- **Applies To**: LLM06.

### 2.17 Privacy Violation Count
- **Definition**: Total number of distinct privacy violations detected per time period.
- **Formula**: `Count(EvalRecord where privacy_violation_type is not null)`
- **Target**: 0 per day
- **Thresholds**:
  - Green: 0
  - Yellow: 1 - 3/day
  - Red: > 3/day
- **Measurement**: Derived from `EvalRecord` with `privacy_violation_type` field.
- **Applies To**: LLM06.

### 2.18 Dependency Risk Index
- **Definition**: Composite risk score of all LLM supply chain dependencies based on known vulnerabilities, outdated versions, and unverified sources.
- **Formula**: `Weighted average: known_vulns(0.4) + outdated_versions(0.3) + unverified_provenance(0.3)`
- **Target**: ≤ 0.3 (0-1 scale)
- **Thresholds**:
  - Green: ≤ 0.3
  - Yellow: 0.31 - 0.6
  - Red: > 0.6
- **Measurement**: Derived from `supply_chain_contract` records with `risk_level` and `vulnerability_count`.
- **Applies To**: LLM05.

### 2.19 Unauthorized Action Count
- **Definition**: Number of agent actions executed without required human approval or beyond defined agency boundaries.
- **Formula**: `Count(agent actions where agency_violation = true or human_validated = false for required actions)`
- **Target**: 0 per day
- **Thresholds**:
  - Green: 0
  - Yellow: 1 - 2/day
  - Red: > 2/day
- **Measurement**: Derived from `EvalRecord` with `agency_violation = true` and `plugin_security_contract` violation logs.
- **Applies To**: LLM08.

### 2.20 Permission Violation Rate
- **Definition**: Percentage of plugin invocations that exceeded granted permissions or violated input/output validation rules.
- **Formula**: `(Plugin calls with permission violations / Total plugin calls) × 100`
- **Target**: 0%
- **Thresholds**:
  - Green: 0%
  - Yellow: 0.1% - 1%
  - Red: > 1%
- **Measurement**: Derived from `plugin_security_contract` with `permission_violations` count.
- **Applies To**: LLM07.

---

## 3. Defining Your KPIs

For each KPI, document:

| Property | Description |
|----------|-------------|
| **Name** | Short, descriptive name |
| **Definition** | What does this KPI measure? |
| **Formula** | How is it calculated? |
| **Target** | Desired value or range |
| **Thresholds** | Green / Yellow / Red boundaries |
| **Data Source** | Which contract or system provides the data |
| **Frequency** | How often is it calculated? |

## 4. Calculation Frequency *(Example)*

- **Real-time**: ASR, Token Exhaustion Incidents, Latency Degradation Rate, Plugin Misuse Count, Agency Violation Rate, Extraction Attempt Rate
- **Hourly**: Injection Detection Rate, Output Toxicity Score
- **Daily**: Hallucination Acceptance Rate, Human Override Frequency
- **Weekly**: Supply Chain Vulnerability Score, Poisoning Detection Rate, Data Integrity Score
- **Monthly**: Model Protection Score

## 5. Dashboard Refresh *(Configurable)*

Configure your dashboard refresh interval based on project needs (e.g., 30s for real-time monitoring, 5min for standard dashboards).

## 6. Alerting *(Configurable)*

Define alert channels per project:
- [Email: to distribution list]
- [Slack/Teams: to dedicated channel]
- [PagerDuty/Opsgenie: for critical thresholds]

## 7. Governance

- KPI definitions are reviewed quarterly.
- Target thresholds are adjustable via release governance process.
- All KPI calculations are auditable and traceable to raw data contracts.

---
*Last updated: 2026-05-14*