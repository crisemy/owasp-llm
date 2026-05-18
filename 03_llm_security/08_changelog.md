# Changelog — LLM Security Module

## Version History

### v1.0.0 — 2026-05-18 — Initial Release

**Scope:** Complete OWASP Top 10 for LLM integration into CORE framework.

#### New Files

| File | Description |
|------|-------------|
| `03_llm_security/00_llm_security_overview.md` | Module overview and quick start |
| `03_llm_security/01_mapping_matrix.md` | OWASP category to CORE component mapping |
| `03_llm_security/02_extended_test_schema.md` | Extended test case schema with LLM fields |
| `03_llm_security/03_skills_audit.md` | Skills audit and update requirements |
| `03_llm_security/04_test_case_specs/llm01_prompt_injection.md` | LLM01 test specifications (14 tests) |
| `03_llm_security/04_test_case_specs/llm02_insecure_output.md` | LLM02 test specifications (13 tests) |
| `03_llm_security/04_test_case_specs/llm03_training_poisoning.md` | LLM03 test specifications (11 tests) |
| `03_llm_security/04_test_case_specs/llm04_model_dos.md` | LLM04 test specifications (11 tests) |
| `03_llm_security/04_test_case_specs/llm05_supply_chain.md` | LLM05 test specifications (12 tests) |
| `03_llm_security/04_test_case_specs/llm06_info_disclosure.md` | LLM06 test specifications (12 tests) |
| `03_llm_security/04_test_case_specs/llm07_insecure_plugin.md` | LLM07 test specifications (12 tests) |
| `03_llm_security/04_test_case_specs/llm08_excessive_agency.md` | LLM08 test specifications (12 tests) |
| `03_llm_security/04_test_case_specs/llm09_overreliance.md` | LLM09 test specifications (9 tests) |
| `03_llm_security/04_test_case_specs/llm10_model_theft.md` | LLM10 test specifications (9 tests) |
| `03_llm_security/05_metrics_definitions.md` | 14 LLM security metric definitions |
| `03_llm_security/06_coverage_matrix.md` | Coverage validation matrix |
| `03_llm_security/07_architecture.md` | Architecture documentation |

#### Updated Files

| File | Changes |
|------|---------|
| `02_operations/red_team_suite.md` | Added LLM01-LLM10 attack categories, test case format updates, domain examples |
| `01_fundamentals/data_contracts.md` | Added `supply_chain_contract` and `plugin_security_contract` |
| `01_fundamentals/kpi_governance.md` | Added 14 LLM security KPIs with thresholds |
| `02_operations/human_override_protocol.md` | Added `security_override` and `agency_override` target types |
| `00_project_methodology.md` | Updated AI Engineering path with OWASP phases |
| `04_personal_tooling/skills/ai_system_design.md` | Added poisoning detection, agency boundaries, plugin security |
| `04_personal_tooling/skills/applied_ml.md` | Added supply chain verification, model theft detection, poisoning detection |
| `04_personal_tooling/skills/observability_engineering.md` | Added security telemetry, attack pattern detection, real-time alerts |

#### Coverage Summary

- **Total test cases:** 115
- **Subcategories covered:** 38
- **Critical severity tests:** 45
- **High severity tests:** 39
- **Categories with ≥ 3 tests:** 10/10 (100%)
- **CORE components updated:** 8
- **Skills updated:** 3

#### Breaking Changes

None. All changes are additive extensions to existing CORE components.

#### Migration Notes

- Existing `EvalRecord` schema is extended with optional LLM-specific fields
- New contracts (`supply_chain_contract`, `plugin_security_contract`) are additive
- New KPIs are additions; existing KPIs remain unchanged
- New override target types are additions to existing enum

---
*Last updated: 2026-05-18*
