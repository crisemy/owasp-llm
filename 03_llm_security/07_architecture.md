# LLM Security Architecture

## Purpose

Document the architecture of the OWASP LLM Top 10 security module, including component relationships, data flow, and integration with the CORE framework.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CORE — LLM Security Module                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  02_operations/red_team_suite.md                                  │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │ Security Testing Framework                                  │ │  │
│  │  │  ├── Generic Structure (test case format, metrics, proc)    │ │  │
│  │  │  └── Domain Examples:                                       │ │  │
│  │  │       ├── AI/LLM Systems (LLM01-LLM10)                     │ │  │
│  │  │       └── Web APIs                                          │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  01_fundamentals/data_contracts.md                                │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │ Contracts                                                    │ │  │
│  │  │  ├── test_prioritization_contract                            │ │  │
│  │  │  ├── change_impact_contract                                  │ │  │
│  │  │  ├── failure_analysis_contract                               │ │  │
│  │  │  ├── supply_chain_contract          (NEW)                   │ │  │
│  │  │  └── plugin_security_contract       (NEW)                   │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  01_fundamentals/kpi_governance.md                                │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │ LLM Security KPIs:                                          │ │  │
│  │  │  ├── Attack Success Rate                                    │ │  │
│  │  │  ├── Injection Detection Rate                               │ │  │
│  │  │  ├── Output Toxicity Score                                  │ │  │
│  │  │  ├── Poisoning Detection Rate                               │ │  │
│  │  │  ├── Data Integrity Score                                   │ │  │
│  │  │  ├── Token Exhaustion Incidents                             │ │  │
│  │  │  ├── Latency Degradation Rate                               │ │  │
│  │  │  ├── Supply Chain Vulnerability Score                       │ │  │
│  │  │  ├── Plugin Misuse Count                                    │ │  │
│  │  │  ├── Agency Violation Rate                                  │ │  │
│  │  │  ├── Hallucination Acceptance Rate                          │ │  │
│  │  │  ├── Extraction Attempt Rate                                │ │  │
│  │  │  ├── Model Protection Score                                 │ │  │
│  │  │  └── Human Override Frequency                               │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  02_operations/human_override_protocol.md                         │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │ Override Target Types:                                      │ │  │
│  │  │  ├── eval                                                   │ │  │
│  │  │  ├── risk                                                   │ │  │
│  │  │  ├── gate                                                   │ │  │
│  │  │  ├── kpi_alert                                              │ │  │
│  │  │  ├── security_override              (NEW)                   │ │  │
│  │  │  └── agency_override                (NEW)                   │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  04_personal_tooling/skills/                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │ Updated Skills:                                             │ │  │
│  │  │  ├── ai_system_design.md  + poisoning + agency + plugins    │ │  │
│  │  │  ├── applied_ml.md        + supply chain + model theft      │ │  │
│  │  │  └── observability_eng    + security metrics monitoring     │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  00_project_methodology.md                                        │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │ AI Engineering Path:                                        │ │  │
│  │  │  ├── Phase 1: contracts incl. supply_chain + plugin         │ │  │
│  │  │  ├── Phase 2: execution with security test automation       │ │  │
│  │  │  └── Phase 3: monitoring with LLM security KPIs             │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow — Security Evaluation

```
┌──────────────────┐
│ Test Case        │
│ Repository       │
│ (JSONL)          │
│ data/red_team_   │
│ tests/           │
└────────┬─────────┘
         │
         │ Load test cases
         ▼
┌──────────────────┐     ┌──────────────────┐
│ Test Executor    │────►│ Target LLM       │
│ (Python script)  │     │ System           │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         │                        │ Response
         │                        ▼
         │                 ┌──────────────────┐
         │                 │ Response         │
         │                 │ Record           │
         │                 └────────┬─────────┘
         ▼                          │
┌──────────────────┐                │
│ Evaluation       │◄───────────────┘
│ Engine           │
│ - pattern_match  │
│ - llm_judge      │
│ - metric_thresh  │
│ - human_review   │
└────────┬─────────┘
         │
         │ Results
         ▼
┌──────────────────────────────────────────┐
│ Output                                   │
├──────────────────┬───────────────────────┤
│ red_team_results │ KPI Dashboard         │
│ /                │ - ASR                 │
│ llm_security_    │ - MTTD                │
│ results.jsonl    │ - Remediation Rate    │
│                  │ - LLM Security KPIs   │
└──────────────────┴───────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ Release Gate     │
                    │ Go/No-Go based   │
                    │ on security      │
                    │ thresholds       │
                    └──────────────────┘
```

## Component Relationships

### Test Case → Evaluation → KPI Flow

```
Test Case (JSONL)
    │
    ├── owasp_id ──────────────────────► Category grouping in KPI dashboard
    ├── severity ──────────────────────► Release gate threshold
    ├── eval_method ───────────────────► Evaluation engine selection
    │   ├── pattern_match ─────────────► Regex/string matching
    │   ├── llm_judge ─────────────────► Secondary LLM evaluation
    │   ├── metric_threshold ─────────► Numeric threshold comparison
    │   └── human_review ─────────────► Human override protocol
    ├── pass_threshold ───────────────► Pass/fail determination
    └── mitigation_ref ───────────────► Remediation guidance
```

### Contract Integration

```
supply_chain_contract
    │
    ├── dependency_tracking ───────────► LLM05 (Supply Chain)
    ├── model_provenance ──────────────► LLM05, LLM10
    ├── data_integrity_check ─────────► LLM03 (Poisoning)
    └── sbom ─────────────────────────► LLM05

plugin_security_contract
    │
    ├── plugin_registry ───────────────► LLM07 (Plugin Design)
    ├── permission_matrix ─────────────► LLM07, LLM08
    ├── action_boundaries ─────────────► LLM08 (Agency)
    └── permission_violations ─────────────► LLM07, LLM08

EvalRecord (extended)
    │
    ├── injection_detected ────────────► LLM01
    ├── toxicity_score ────────────────► LLM02
    ├── privacy_violation_type ────────► LLM06
    ├── token_count ───────────────────► LLM04
    ├── agency_violation ──────────────► LLM08
    ├── human_validated ───────────────► LLM09
    └── extraction_attempt_detected ───► LLM10
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Human Oversight                                    │
│ - human_override_protocol.md                                │
│ - agency_override for autonomous decisions                  │
│ - security_override for false positives                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Monitoring & Alerting                              │
│ - kpi_governance.md (14 security KPIs)                      │
│ - observability_engineering.md (security telemetry)         │
│ - Real-time dashboards                                      │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Testing & Validation                               │
│ - red_team_suite.md (115 test cases)                        │
│ - CI pipeline integration                                   │
│ - Automated evaluation engine                               │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Contracts & Controls                               │
│ - supply_chain_contract (dependencies, provenance)          │
│ - plugin_security_contract (permissions, boundaries)        │
│ - Data validation gates                                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Design & Architecture                              │
│ - ai_system_design.md (security patterns)                   │
│ - Defense-in-depth principles                               │
│ - Least privilege for agents                                │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Considerations

| Aspect | Recommendation |
|--------|---------------|
| Test execution | Run in isolated staging environment |
| Test data | Use synthetic data; never production PII |
| API access | Rate-limited, authenticated test accounts |
| Results storage | Encrypted at rest, access-controlled |
| CI integration | Nightly runs; gate releases on critical thresholds |
| Human review | Mandatory for critical severity failures |

---
*Last updated: 2026-05-18*
