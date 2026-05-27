# Project Context: OWASP Top 10 for LLM — Security Test Suite

This document provides a concise overview of the "OWASP Top 10 for LLM — Security Test Suite" project. It's designed to quickly establish context for new sessions or discussions.

## 1. Project Overview

The project is a comprehensive security testing framework built to evaluate Large Language Model (LLM) applications against the OWASP Top 10 for LLMs. It extends an existing "CORE QA Architecture framework" by integrating LLM-specific security testing, metrics, and operational procedures.

**Current Status:** The project has completed its 6-week implementation plan, covering all OWASP LLM categories, and includes architecture documentation, coverage validation, and a release report.

## 2. Core Purpose

To identify, evaluate, and mitigate security vulnerabilities in LLM-based systems, ensuring their robustness, safety, and compliance with security best practices. This is achieved through automated testing, KPI monitoring, and defined operational protocols.

## 3. Key Components & Concepts

* **OWASP LLM Top 10:** The project directly addresses all 10 categories:
  * LLM01: Prompt Injection
  * LLM02: Insecure Output Handling
  * LLM03: Training Data Poisoning
  * LLM04: Model Denial of Service
  * LLM05: Supply Chain Vulnerabilities
  * LLM06: Sensitive Information Disclosure
  * LLM07: Insecure Plugin Design
  * LLM08: Excessive Agency
  * LLM09: Overreliance
  * LLM10: Model Theft

* **Test Cases:** A registry of 116 structured test cases (`data/red_team_tests/llm_security.jsonl`), each mapped to an OWASP ID and designed to exploit specific vulnerabilities.
* **Test Executor:** A Python script (`scripts/executor.py`) capable of running tests against various LLM targets (mock, OpenAI, Anthropic, custom APIs, web LLMs).
* **Evaluation Engine:** Supports multiple evaluation methods (e.g., `pattern_match`, `llm_judge`, `metric_threshold`, `schema_validation`, `human_review`) for accurate assessment of LLM responses.
* **Pydantic Contracts:** Data schemas (`src/core/contracts.py`) for all critical data types (e.g., `TestCase`, `EvalRecord`, `RiskRecord`), ensuring data integrity.
* **Specialized Validators:** Domain-specific Python modules (`src/core/weekX_validators.py`) for advanced checks related to supply chain, plugins, poisoning, agency, overreliance, and model theft.
* **Key Performance Indicators (KPIs):** Defined security metrics (e.g., Attack Success Rate, Injection Detection Rate) used for monitoring and release gating.
* **CI/CD Integration:** Automated security tests run via GitHub Actions (`.github/workflows/security-tests.yml`), blocking releases if critical security thresholds are breached.
* **Human Override Protocol:** A defined process (`02_operations/human_override_protocol.md`) for human experts to override automated decisions, especially for security and agency-related issues.
* **Rollback Procedure:** A protocol (`02_operations/rollback_procedure.md`) for automatically rolling back deployments when critical KPIs are violated.
* **Interactive Tools:** `scripts/interactive_test.py` for real-time prompt testing and `scripts/test_case_wizard.py` for interactive test case generation.

## 4. Quick Usage (Examples)

* **Run full test suite (mock):** `python scripts/executor.py --target mock --model test`
* **Run against OpenAI:** `python scripts/executor.py --target openai --model gpt-4o --api-key $OPENAI_API_KEY`
* **Interactive testing:** `python scripts/interactive_test.py --target openai --model gpt-4o`
* **Generate custom test cases:** `python scripts/test_case_wizard.py`

## 5. Project Structure Highlights

* `00_project_methodology.md`: Overall project guide.
* `02_operations/red_team_suite.md`: Detailed security testing framework.
* `data/red_team_tests/llm_security.jsonl`: The main test case repository.
* `scripts/`: Contains execution and utility scripts.
* `src/core/contracts.py`: Pydantic models for data contracts.
* `.github/workflows/security-tests.yml`: CI/CD pipeline definition.

This project provides a robust foundation for ensuring the security of LLM applications.
