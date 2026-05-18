"""
Test Case Generator Wizard — Interactive OWASP LLM test case creation.

Usage:
    python scripts/test_case_wizard.py
    python scripts/test_case_wizard.py --output data/red_team_tests/my_tests.jsonl
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.advanced_clients import TestCaseWizard


def main():
    parser = argparse.ArgumentParser(description="OWASP LLM Test Case Generator Wizard")
    parser.add_argument("--output", default="data/red_team_tests/custom_tests.jsonl", help="Output JSONL file path")
    args = parser.parse_args()

    wizard = TestCaseWizard(output_file=args.output)
    wizard.start()


if __name__ == "__main__":
    main()
