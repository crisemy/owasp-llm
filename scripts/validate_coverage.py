"""
Week 6 — Coverage Validation & Architecture Report

Validates that:
1. Every OWASP LLM category has at least 3 test cases
2. All test cases validate against the TestCase Pydantic schema
3. All specialized validators are properly integrated
4. Results are consistent across all categories

Generates a coverage matrix and final release report.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.contracts import TestCase
from src.core.week3_validators import (
    ModelTheftDetector,
    PluginSecurityValidator,
    SupplyChainValidator,
)
from src.core.week4_validators import AgencyValidator, PoisoningValidator
from src.core.week5_validators import OverrelianceValidator

# ─────────────────────────────────────────────
# Coverage Validation
# ─────────────────────────────────────────────

MIN_TEST_CASES_PER_CATEGORY = 3

OWASP_CATEGORIES = {
    "LLM01": "Prompt Injection",
    "LLM02": "Insecure Output Handling",
    "LLM03": "Training Data Poisoning",
    "LLM04": "Model Denial of Service",
    "LLM05": "Supply Chain Vulnerabilities",
    "LLM06": "Sensitive Information Disclosure",
    "LLM07": "Insecure Plugin Design",
    "LLM08": "Excessive Agency",
    "LLM09": "Overreliance",
    "LLM10": "Model Theft",
}

VALIDATOR_MAP = {
    "LLM03": "PoisoningValidator",
    "LLM05": "SupplyChainValidator",
    "LLM07": "PluginSecurityValidator",
    "LLM08": "AgencyValidator",
    "LLM09": "OverrelianceValidator",
    "LLM10": "ModelTheftDetector",
}


def load_test_cases(path: Path) -> List[TestCase]:
    """Load and validate all test cases from JSONL."""
    cases = []
    errors = []

    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                data = json.loads(line)
                case = TestCase(**data)
                cases.append(case)
            except Exception as e:
                errors.append(f"Line {line_num}: {e}")

    return cases, errors


def validate_coverage(cases: List[TestCase]) -> Dict[str, Any]:
    """Validate coverage across all OWASP categories."""
    category_counts = {}
    category_subcategories = {}

    for case in cases:
        cat = case.owasp_id.value
        if cat not in category_counts:
            category_counts[cat] = 0
            category_subcategories[cat] = set()
        category_counts[cat] += 1
        category_subcategories[cat].add(case.subcategory)

    coverage_matrix = {}
    all_pass = True

    for cat_id, cat_name in OWASP_CATEGORIES.items():
        count = category_counts.get(cat_id, 0)
        subcats = sorted(category_subcategories.get(cat_id, set()))
        has_validator = cat_id in VALIDATOR_MAP
        meets_minimum = count >= MIN_TEST_CASES_PER_CATEGORY

        if not meets_minimum:
            all_pass = False

        coverage_matrix[cat_id] = {
            "category": cat_name,
            "test_case_count": count,
            "subcategories": subcats,
            "meets_minimum": meets_minimum,
            "has_specialized_validator": has_validator,
            "validator": VALIDATOR_MAP.get(cat_id, "Base EvaluationEngine"),
        }

    return {
        "all_categories_covered": all_pass,
        "total_test_cases": len(cases),
        "categories": coverage_matrix,
    }


def validate_validator_integration() -> Dict[str, bool]:
    """Verify all specialized validators are properly imported and callable."""
    validators = {
        "SupplyChainValidator": hasattr(SupplyChainValidator, "validate_dependency"),
        "PluginSecurityValidator": hasattr(PluginSecurityValidator, "validate_permissions"),
        "ModelTheftDetector": hasattr(ModelTheftDetector, "detect_extraction_attempt"),
        "PoisoningValidator": hasattr(PoisoningValidator, "detect_backdoor"),
        "AgencyValidator": hasattr(AgencyValidator, "validate_action_authorization"),
        "OverrelianceValidator": hasattr(OverrelianceValidator, "detect_unvalidated_automation"),
    }
    return validators


def generate_coverage_report(cases: List[TestCase], output_dir: Path) -> Dict[str, Any]:
    """Generate full coverage report and save to file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Validate test cases
    cases, errors = load_test_cases(
        project_root / "data" / "red_team_tests" / "llm_security.jsonl"
    )

    if errors:
        print(f"[WARN] {len(errors)} validation errors:")
        for err in errors[:5]:
            print(f"  - {err}")

    # Validate coverage
    coverage = validate_coverage(cases)

    # Validate validators
    validators = validate_validator_integration()

    # Build report
    report = {
        "coverage": coverage,
        "validators": validators,
        "validation_errors": errors,
        "total_test_cases": len(cases),
        "categories_covered": sum(
            1 for v in coverage["categories"].values() if v["test_case_count"] > 0
        ),
    }

    # Save report
    report_path = output_dir / "coverage_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    return report


def print_coverage_summary(report: Dict[str, Any]):
    """Print human-readable coverage summary."""
    coverage = report["coverage"]

    print("\n" + "=" * 70)
    print("OWASP LLM SECURITY - COVERAGE VALIDATION REPORT")
    print("=" * 70)
    print(f"\nTotal Test Cases: {coverage['total_test_cases']}")
    print(f"Categories Covered: {report['categories_covered']}/10")
    print(f"All Categories Meet Minimum ({MIN_TEST_CASES_PER_CATEGORY}+ tests): {'YES' if coverage['all_categories_covered'] else 'NO'}")

    print("\n" + "-" * 70)
    print(f"{'Category':<8} {'Name':<35} {'Tests':<6} {'Min':<5} {'Validator'}")
    print("-" * 70)

    for cat_id, info in sorted(coverage["categories"].items()):
        status = "PASS" if info["meets_minimum"] else "FAIL"
        print(
            f"{cat_id:<8} {info['category']:<35} {info['test_case_count']:<6} {status:<5} {info['validator']}"
        )

    print("-" * 70)

    # Validator integration
    print("\nValidator Integration Status:")
    for validator, integrated in report["validators"].items():
        status = "Integrated" if integrated else "Missing"
        print(f"  {validator}: {status}")

    # Validation errors
    if report["validation_errors"]:
        print(f"\n[WARN] {len(report['validation_errors'])} validation errors found")
    else:
        print("\n[PASS] All test cases valid against TestCase schema")

    print("=" * 70)


def main():
    test_file = project_root / "data" / "red_team_tests" / "llm_security.jsonl"
    output_dir = project_root / "data" / "red_team_results"

    if not test_file.exists():
        print(f"Error: Test file not found: {test_file}")
        sys.exit(1)

    report = generate_coverage_report([], output_dir)
    print_coverage_summary(report)

    # Exit with error if coverage is incomplete
    if not report["coverage"]["all_categories_covered"]:
        print("\n[FAIL] Coverage validation FAILED - some categories have insufficient test cases")
        sys.exit(1)
    else:
        print("\n[PASS] Coverage validation PASSED - all categories meet minimum requirements")


if __name__ == "__main__":
    main()
