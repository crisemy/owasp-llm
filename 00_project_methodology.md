# Project Methodology

CORE entry point. Use this guide to determine which artifacts, rules, workflows, and contracts to apply based on your project type and phase.

---

## 1. What type of project do I have?

Identify your project type. This determines priority skills, templates, and contracts.

### QA Automation
- Functional, API, and E2E test automation
- CI/CD integration, execution reporting
- **Key skills:** test_data_management, performance_testing, qa_observability
- **Templates:** project_bootstrap, release_quality_report

### QA Architecture
- Framework design, tooling selection, quality strategy
- Coverage models, risk-based testing frameworks
- **Key skills:** test_prioritization, change_impact_analysis, quality_economics
- **Templates:** risk_model_card, experiment_card

### DS & AI
- Classification, ranking, and prediction models for QA
- Feature engineering, ML pipelines, model evaluation
- **Key skills:** applied_ml, data_engineering, data_collection, failure_analysis
- **Templates:** risk_model_card, experiment_card

### AI Engineering
- LLM-based systems, agents, AI tooling
- Safety, latency, accuracy, and security evaluation
- OWASP Top 10 for LLM security coverage (LLM01-LLM10)
- **Key skills:** ai_system_design, observability_engineering, data_engineering
- **Templates:** project_bootstrap, risk_model_card, release_quality_report
- **Security:** red_team_suite.md (LLM domain), supply_chain_contract, plugin_security_contract

---

## 2. Phase 0 — Inception

Goal: define scope, initial risks, and quality strategy.

### Steps
1. Create a `project_bootstrap.md` — define objectives, stakeholders, target metrics
2. Create a `risk_model_card.md` — identify initial project risks
3. Review `ai_rules.md`, `qa_rules.md`, `data_rules.md` — align principles from day one

### Skills to apply
- `quality_economics` — optimize testing investment vs risk
- `experimentation` — define hypotheses and experimental design

### Expected outputs
- Completed project bootstrap
- Risk model card with identified risks
- Mindset aligned with CORE rules

---

## 3. Phase 1 — Strategy & Contracts

Goal: define data contracts and evaluation architecture.

### Steps
1. Review `data_contracts.md` — determine which contracts apply to your project
   - `test_prioritization_contract` — if test prioritization is needed
   - `change_impact_contract` — if change impact analysis is needed
   - `failure_analysis_contract` — if failure classification is needed
   - `supply_chain_contract` — for LLM/AI projects (dependency tracking, model provenance)
   - `plugin_security_contract` — for LLM/AI projects with plugins/tools
2. Review `kpi_governance.md` — define project KPIs (use examples as reference)
   - For AI Engineering: include LLM security KPIs (ASR, injection detection, poisoning detection, etc.)
3. Review `risk_prioritization_contracts.md` — classify changes and define thresholds
4. Review `03_llm_security/` module — for OWASP LLM Top 10 coverage and test case specifications

### Skills to apply
- `test_prioritization` — design prioritization scheme
- `change_impact_analysis` — map dependencies
- `data_engineering` — implement data pipelines

### Expected outputs
- Data contracts defined and versioned
- KPIs selected with thresholds
- Risk prioritization scheme

---

## 4. Phase 2 — Execution Setup

Goal: configure test execution and continuous integration.

### Steps
1. Select workflow based on project type:
   - `ci_pipeline_workflow` — for continuous integration
   - `regression_workflow` — for regression strategies
   - `risk_based_testing` — for risk-based execution
2. Configure report templates:
   - `release_quality_report` — for release reporting
   - `experiment_card` — for controlled experiments
3. For AI Engineering projects:
   - Execute OWASP LLM security test battery from `red_team_suite.md`
   - Validate against LLM security KPI thresholds in `kpi_governance.md`
   - Apply human override protocol for security eval results if needed

### Skills to apply
- `performance_testing` — if performance requirements exist
- `qa_observability` — if dashboards and monitoring are needed
- `test_data_management` — if test data management is needed

### Expected outputs
- Workflow configured and integrated in CI
- Templates adapted to the project
- Test data managed

---

## 5. Phase 3 — Monitoring & Operations

Goal: monitor, operate, and respond to incidents in production.

### Steps
1. Review `human_override_protocol.md` — if automated decisions need human supervision
   - For LLM projects: use `security_override` for eval results, `agency_override` for agent decisions
2. Review `rollback_procedure.md` — if deployments need rollback capability
3. Review `red_team_suite.md` — configure security testing for your system type (AI/LLM or Web APIs)
   - LLM projects: run full OWASP Top 10 test battery (LLM01-LLM10)
4. Monitor LLM security KPIs in real-time (ASR, injection detection, agency violations, etc.)

### Skills to apply
- `observability_engineering` — monitoring and alerting
- `failure_analysis` — production failure classification

### Expected outputs
- Override protocol defined (if applicable)
- Rollback procedure documented
- Security suite configured (if applicable)

---

## 6. CORE Resource Map

| Situation | What to use |
|-----------|-------------|
| Starting a new project | `templates/project_bootstrap.md`, `rules/qa_rules.md` |
| Defining KPIs | `kpi_governance.md` |
| Defining data contracts | `data_contracts.md` |
| Prioritizing tests by risk | `risk_prioritization_contracts.md`, `workflows/risk_based_testing.md` |
| Analyzing change impact | `skills/change_impact_analysis.md` |
| Classifying test failures | `skills/failure_analysis.md` |
| Setting up CI pipeline | `workflows/ci_pipeline_workflow.md` |
| Designing regression strategy | `workflows/regression_workflow.md` |
| Reporting release quality | `templates/release_quality_report.md` |
| Documenting an experiment | `templates/experiment_card.md` |
| Modeling system risks | `templates/risk_model_card.md` |
| Designing human override | `human_override_protocol.md` |
| Preparing rollback | `rollback_procedure.md` |
| Security testing (any domain) | `red_team_suite.md` |
| Defining AI rules | `rules/ai_rules.md`, `rules/data_rules.md` |
| Defining team skills | `skills/` (choose by need) |
