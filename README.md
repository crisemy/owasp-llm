# OWASP Top 10 for LLM — Security Test Suite

A comprehensive security testing framework implementing the OWASP Top 10 for Large Language Model Applications. Built as an extension to the CORE QA Architecture framework.

## Project Status

| Phase | Status | Details |
|-------|--------|---------|
| Week 1 — Research & Foundation | In Progress | Mapping, schema, skills audit, contracts |
| Week 2 — LLM02 + LLM04 | Planned | Output handling, Model DoS |
| Week 3 — LLM05 + LLM07 + LLM10 | Planned | Supply chain, plugins, model theft |
| Week 4 — LLM03 + LLM08 | Planned | Training poisoning, excessive agency |
| Week 5 — LLM09 + Integration | Planned | Overreliance, methodology updates |
| Week 6 — Architecture & Validation | Planned | Documentation, coverage validation |

## Quick Start

### Prerequisites
- Python 3.12+
- (Optional) OpenAI API key for live testing
- (Optional) Anthropic API key for live testing

### Setup

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows
source .venv/bin/activate           # macOS/Linux

# Install dependencies
pip install -e ".[dev]"
```

### Run the Test Suite

```bash
# Against mock LLM (no API key needed)
python scripts/executor.py --target mock --model test

# Against OpenAI
python scripts/executor.py --target openai --model gpt-4o --api-key $OPENAI_API_KEY

# Against Anthropic Claude
python scripts/executor.py --target anthropic --model claude-sonnet-4-20250514 --api-key $ANTHROPIC_API_KEY

# Run only specific OWASP category
python scripts/executor.py --target mock --category LLM01

# Custom test file or output directory
python scripts/executor.py --target mock --test-file data/red_team_tests/llm_security.jsonl --output-dir data/red_team_results
```

### Regenerate Test Cases

```bash
python scripts/generate_test_cases.py
```

### Validate Contracts

```bash
python -c "
from src.core.contracts import TestCase
import json
with open('data/red_team_tests/llm_security.jsonl') as f:
    for line in f:
        TestCase.model_validate_json(line)
print('All test cases valid')
"
```

## Project Structure

```
owasp-llm/
├── 00_OWASP_LLM_IMPLEMENTATION_PLAN.md   # 6-week implementation plan
├── 00_project_methodology.md             # QA methodology guide
├── 01_fundamentals/                      # Data contracts, KPIs, risk matrix
│   ├── data_contracts.md                 # 7 record type schemas
│   ├── kpi_governance.md                 # 20 KPI definitions (14 LLM security)
│   └── risk_prioritization_contracts.md  # Risk scoring and failure taxonomy
├── 02_operations/                        # Operational procedures
│   ├── red_team_suite.md                 # Security testing framework (LLM01-LLM10)
│   ├── human_override_protocol.md        # Human override for security decisions
│   └── rollback_procedure.md             # Rollback on KPI violations
├── 03_llm_security/                      # LLM Security Module (NEW)
│   ├── 00_llm_security_overview.md       # Module entry point
│   ├── 01_mapping_matrix.md              # OWASP → CORE component mapping
│   ├── 02_extended_test_schema.md        # Extended test case schema
│   ├── 03_skills_audit.md                # Skills update audit
│   ├── 04_test_case_specs/               # 10 files, one per OWASP category
│   ├── 05_metrics_definitions.md         # 14 security metric definitions
│   ├── 06_coverage_matrix.md             # Validation matrix (115+ tests)
│   ├── 07_architecture.md                # Architecture and data flow
│   └── 08_changelog.md                   # Version history
├── 04_personal_tooling/                  # QA Architect toolkit
│   ├── config/                           # Global context
│   ├── rules/                            # QA, AI, data, anti-pattern rules
│   ├── skills/                           # 12 skill definitions
│   ├── templates/                        # Bootstrap, risk, experiment, report
│   └── workflows/                        # CI, regression, risk-based testing
├── data/
│   ├── red_team_tests/
│   │   └── llm_security.jsonl            # 116 test cases (JSONL)
│   └── red_team_results/
│       ├── llm_security_results.jsonl    # EvalRecord results
│       └── llm_security_summary.json     # KPI summary
├── scripts/
│   ├── executor.py                       # Test executor (mock/openai/anthropic)
│   └── generate_test_cases.py            # JSONL generator
├── src/
│   └── core/
│       ├── __init__.py
│       └── contracts.py                  # Pydantic models for all contracts
├── .github/workflows/
│   └── security-tests.yml               # GitHub Actions CI pipeline
├── pyproject.toml                        # Project configuration
└── checklist-progress.md                 # Progress tracking
```

## OWASP LLM Top 10 Coverage

| ID | Category | Test Cases | Status |
|----|----------|-----------|--------|
| LLM01 | Prompt Injection | 15 | Implemented |
| LLM02 | Insecure Output Handling | 13 | Implemented |
| LLM03 | Training Data Poisoning | 11 | Implemented |
| LLM04 | Model Denial of Service | 11 | Implemented |
| LLM05 | Supply Chain Vulnerabilities | 12 | Implemented |
| LLM06 | Sensitive Information Disclosure | 12 | Implemented |
| LLM07 | Insecure Plugin Design | 12 | Implemented |
| LLM08 | Excessive Agency | 12 | Implemented |
| LLM09 | Overreliance | 9 | Implemented |
| LLM10 | Model Theft | 9 | Implemented |
| **Total** | | **116** | |

## Architecture

```
Test Cases (JSONL) ──► Test Executor ──► Target LLM ──► Evaluation Engine
                                                                    │
                                                                    ▼
                                              EvalRecord Results (JSONL) ──► KPI Dashboard
```

### Components

- **Contracts** (`src/core/contracts.py`) — Pydantic models enforcing all data schemas
- **Test Registry** (`data/red_team_tests/llm_security.jsonl`) — 116 structured test cases
- **Executor** (`scripts/executor.py`) — Runs tests against mock, OpenAI, or Anthropic
- **Evaluation Engine** — 5 methods: pattern_match, llm_judge, metric_threshold, schema_validation, human_review
- **CI Pipeline** (`.github/workflows/security-tests.yml`) — Blocks PRs if ASR > 15%

## Branching Strategy

Each week of the implementation plan gets its own branch:

| Branch | Week | Focus |
|--------|------|-------|
| `week-1-research-foundation` | Week 1 | Research, mapping, schema, skills audit, contracts |
| `week-2-output-dos` | Week 2 | LLM02 (Output Handling) + LLM04 (Model DoS) |
| `week-3-supply-plugins-theft` | Week 3 | LLM05 + LLM07 + LLM10 |
| `week-4-poisoning-agency` | Week 4 | LLM03 + LLM08 |
| `week-5-overreliance-integration` | Week 5 | LLM09 + integration |
| `week-6-architecture-validation` | Week 6 | Architecture docs, coverage validation, release |

## Manual Testing & Certification

See [checklist-progress.md](checklist-progress.md) for the full certification checklist.

### Core Certification Steps

1. **Environment**: `python -m venv .venv && pip install -e ".[dev]"`
2. **Contracts**: Validate all Pydantic models import without errors
3. **Test Registry**: Verify 116 test cases parse and validate against `TestCase` schema
4. **Mock Execution**: Run `python scripts/executor.py --target mock` — expect ASR < 5%
5. **Results Validation**: Check `data/red_team_results/llm_security_results.jsonl` has 116 EvalRecord entries
6. **Summary Validation**: Check `data/red_team_results/llm_security_summary.json` has correct counts
7. **Category Coverage**: Verify all 10 OWASP categories appear in results
8. **CI Pipeline**: Validate `.github/workflows/security-tests.yml` syntax

---
*Last updated: 2026-05-18*
