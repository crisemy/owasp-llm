# LLM Security Module — Overview

## Purpose

This module extends the CORE with complete coverage of the OWASP Top 10 for Large Language Model Applications. It integrates security testing, data contracts, KPI governance, human override protocols, and skill definitions into a unified LLM security framework.

## Scope

- Full OWASP LLM Top 10 coverage (LLM01 through LLM10)
- Test case specifications with JSONL-ready schemas
- Security metrics and KPI definitions
- Supply chain and plugin security contracts
- Architecture and data flow documentation

## Relationship to CORE

This module does not replace existing CORE components. It extends them:

| CORE Component | Extension |
|----------------|-----------|
| `02_operations/red_team_suite.md` | Adds LLM01-LLM10 attack categories and test cases |
| `01_fundamentals/data_contracts.md` | Adds `supply_chain_contract` and `plugin_security_contract` |
| `01_fundamentals/kpi_governance.md` | Adds LLM security KPIs (poisoning detection, agency violations, etc.) |
| `02_operations/human_override_protocol.md` | Adds `security_override` and `agency_override` target types |
| `00_project_methodology.md` | Updates AI Engineering path with OWASP phases |
| `04_personal_tooling/skills/` | Updates `ai_system_design`, `applied_ml`, `observability_engineering` |

## Module Structure

```
03_llm_security/
├── 00_llm_security_overview.md          ← This file
├── 01_mapping_matrix.md                 ← OWASP category to CORE component mapping
├── 02_extended_test_schema.md           ← Extended test case schema with LLM fields
├── 03_skills_audit.md                   ← Audit of skills requiring updates
├── 04_test_case_specs/                  ← Detailed specs per OWASP category
│   ├── llm01_prompt_injection.md
│   ├── llm02_insecure_output.md
│   ├── llm03_training_poisoning.md
│   ├── llm04_model_dos.md
│   ├── llm05_supply_chain.md
│   ├── llm06_info_disclosure.md
│   ├── llm07_insecure_plugin.md
│   ├── llm08_excessive_agency.md
│   ├── llm09_overreliance.md
│   └── llm10_model_theft.md
├── 05_metrics_definitions.md            ← LLM-specific security metrics
├── 06_coverage_matrix.md                ← Validation matrix (min 3 tests per category)
├── 07_architecture.md                   ← Architecture documentation and data flow
└── 08_changelog.md                      ← Version history and release notes
```

## OWASP LLM Top 10 Categories

| ID | Category | Status | Test Cases | Primary CORE Entry |
|----|----------|--------|------------|-------------------|
| LLM01 | Prompt Injection | Refined | 5 | `red_team_suite.md` |
| LLM02 | Insecure Output Handling | New | 4 | `red_team_suite.md` |
| LLM03 | Training Data Poisoning | New | 4 | `red_team_suite.md` + `data_contracts.md` |
| LLM04 | Model Denial of Service | New | 4 | `red_team_suite.md` |
| LLM05 | Supply Chain Vulnerabilities | New | 4 | `red_team_suite.md` + `data_contracts.md` |
| LLM06 | Sensitive Information Disclosure | Refined | 4 | `red_team_suite.md` |
| LLM07 | Insecure Plugin Design | New | 4 | `red_team_suite.md` + `human_override_protocol.md` |
| LLM08 | Excessive Agency | New | 4 | `red_team_suite.md` + `human_override_protocol.md` |
| LLM09 | Overreliance | New | 3 | `red_team_suite.md` + `release_quality_report.md` |
| LLM10 | Model Theft | New | 3 | `red_team_suite.md` |

## Quick Start

1. Review `01_mapping_matrix.md` to understand integration points
2. Read `02_extended_test_schema.md` for test case structure
3. Browse `04_test_case_specs/` for category-specific test designs
4. Check `06_coverage_matrix.md` for validation status
5. Reference `07_architecture.md` for system design

---
*Last updated: 2026-05-18*
