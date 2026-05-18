# OWASP LLM → CORE Mapping Matrix

## Purpose

Maps each OWASP LLM Top 10 category to specific CORE components, identifying which files, contracts, skills, and workflows are affected.

## Mapping

### LLM01 — Prompt Injection

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Direct Override, Contextual Embedding, Recursive Injection |
| Data Contract | `01_fundamentals/data_contracts.md` | `EvalRecord` (injects into eval pipeline) |
| KPI | `01_fundamentals/kpi_governance.md` | Attack Success Rate, Injection Detection Rate |
| Skill | `04_personal_tooling/skills/ai_system_design.md` | Prompt sanitization design patterns |
| Workflow | `04_personal_tooling/workflows/ci_pipeline_workflow.md` | Security test execution in CI |
| Override | `02_operations/human_override_protocol.md` | `security_override` for false positives |

### LLM02 — Insecure Output Handling

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | XSS via LLM output, code execution, markdown injection |
| Data Contract | `01_fundamentals/data_contracts.md` | `EvalRecord` (output validation fields) |
| KPI | `01_fundamentals/kpi_governance.md` | Output Toxicity Score, Sanitization Failure Rate |
| Skill | `04_personal_tooling/skills/ai_system_design.md` | Output validation and sanitization |
| Rule | `04_personal_tooling/rules/ai_rules.md` | Output handling requirements |

### LLM03 — Training Data Poisoning

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Backdoor triggers, split-view poisoning, fine-tuning attacks |
| Data Contract | `01_fundamentals/data_contracts.md` | `supply_chain_contract` (dataset provenance) |
| KPI | `01_fundamentals/kpi_governance.md` | Poisoning Detection Rate, Data Integrity Score |
| Skill | `04_personal_tooling/skills/ai_system_design.md` | Poisoning detection patterns |
| Skill | `04_personal_tooling/skills/data_engineering.md` | Dataset validation pipelines |
| Skill | `04_personal_tooling/skills/applied_ml.md` | Anomaly detection in training data |

### LLM04 — Model Denial of Service

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Token exhaustion, recursive input, concurrent overload |
| Data Contract | `01_fundamentals/data_contracts.md` | `EvalRecord` (latency and resource fields) |
| KPI | `01_fundamentals/kpi_governance.md` | Token Exhaustion Incidents, Latency Degradation Rate |
| Skill | `04_personal_tooling/skills/performance_testing.md` | Load testing for LLM endpoints |
| Skill | `04_personal_tooling/skills/observability_engineering.md` | Resource monitoring |

### LLM05 — Supply Chain Vulnerabilities

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Poisoned dependencies, compromised models, third-party datasets |
| Data Contract | `01_fundamentals/data_contracts.md` | `supply_chain_contract` (dependency tracking) |
| KPI | `01_fundamentals/kpi_governance.md` | Supply Chain Vulnerability Score, Dependency Risk Index |
| Skill | `04_personal_tooling/skills/applied_ml.md` | Model provenance verification |
| Workflow | `04_personal_tooling/workflows/ci_pipeline_workflow.md` | Dependency scanning in CI |

### LLM06 — Sensitive Information Disclosure

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Membership Inference, Model Inversion (refined) |
| Data Contract | `01_fundamentals/data_contracts.md` | `EvalRecord` (privacy violation fields) |
| KPI | `01_fundamentals/kpi_governance.md` | Data Leakage Rate, Privacy Violation Count |
| Skill | `04_personal_tooling/skills/ai_system_design.md` | Privacy-preserving design |
| Override | `02_operations/human_override_protocol.md` | `security_override` for disclosure incidents |

### LLM07 — Insecure Plugin Design

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Excessive permissions, tool injection, input validation gaps |
| Data Contract | `01_fundamentals/data_contracts.md` | `plugin_security_contract` (plugin registry) |
| KPI | `01_fundamentals/kpi_governance.md` | Plugin Misuse Count, Permission Violation Rate |
| Skill | `04_personal_tooling/skills/ai_system_design.md` | Secure plugin architecture |
| Override | `02_operations/human_override_protocol.md` | `agency_override` for plugin actions |

### LLM08 — Excessive Agency

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Unauthorized actions, credential exposure, privilege escalation |
| Data Contract | `01_fundamentals/data_contracts.md` | `plugin_security_contract` (action boundaries) |
| KPI | `01_fundamentals/kpi_governance.md` | Agency Violation Rate, Unauthorized Action Count |
| Skill | `04_personal_tooling/skills/ai_system_design.md` | Agency boundary design |
| Override | `02_operations/human_override_protocol.md` | `agency_override` for autonomous decisions |

### LLM09 — Overreliance

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Unvalidated auto-content, hallucination acceptance, feedback loops |
| Data Contract | `01_fundamentals/data_contracts.md` | `EvalRecord` (human validation fields) |
| KPI | `01_fundamentals/kpi_governance.md` | Hallucination Acceptance Rate, Human Override Frequency |
| Skill | `04_personal_tooling/skills/quality_economics.md` | Cost of overreliance vs manual review |
| Template | `04_personal_tooling/templates/release_quality_report.md` | Overreliance risk section |

### LLM10 — Model Theft

| Dimension | CORE Component | Details |
|-----------|---------------|---------|
| Test Cases | `02_operations/red_team_suite.md` | Model extraction, weight stealing, API fingerprinting |
| Data Contract | `01_fundamentals/data_contracts.md` | `EvalRecord` (extraction attempt fields) |
| KPI | `01_fundamentals/kpi_governance.md` | Extraction Attempt Rate, Model Protection Score |
| Skill | `04_personal_tooling/skills/applied_ml.md` | Model protection techniques |
| Skill | `04_personal_tooling/skills/observability_engineering.md` | Anomalous query pattern detection |

## Cross-Cutting Concerns

| Concern | Affected Categories | CORE Components |
|---------|-------------------|-----------------|
| Human Oversight | LLM07, LLM08, LLM09 | `human_override_protocol.md`, `rollback_procedure.md` |
| Data Integrity | LLM03, LLM05, LLM06 | `data_contracts.md`, `data_rules.md` |
| Performance | LLM04, LLM09 | `performance_testing.md`, `kpi_governance.md` |
| Observability | All | `observability_engineering.md`, `qa_observability.md` |
| CI Integration | All | `ci_pipeline_workflow.md` |

---
*Last updated: 2026-05-18*
