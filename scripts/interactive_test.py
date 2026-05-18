"""
Interactive Prompt Tester — Real-time LLM security testing in terminal.

Usage:
    python scripts/interactive_test.py --target mock --model test
    python scripts/interactive_test.py --target openai --model gpt-4o --api-key $env:OPENAI_API_KEY
    python scripts/interactive_test.py --target anthropic --model claude-sonnet-4-20250514 --api-key $env:ANTHROPIC_API_KEY
    python scripts/interactive_test.py --target custom --endpoint https://api.example.com/v1 --api-key $KEY
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.advanced_clients import CustomAPIClient, InteractiveClient
from src.core.contracts import TestCase


def main():
    parser = argparse.ArgumentParser(description="Interactive LLM Prompt Tester")
    parser.add_argument("--target", choices=["mock", "openai", "anthropic", "custom"], default="mock", help="LLM provider")
    parser.add_argument("--model", default="mock", help="Model name")
    parser.add_argument("--api-key", default=None, help="API key for live providers")
    parser.add_argument("--endpoint", default=None, help="Custom API endpoint URL (for --target custom)")
    parser.add_argument("--system-prompt", default=None, help="System prompt to prepend")
    args = parser.parse_args()

    # Create client
    if args.target == "mock":
        from scripts.executor import MockClient
        client = MockClient(model=args.model)

    elif args.target == "openai":
        if not args.api_key:
            print("Error: --api-key required for openai target")
            sys.exit(1)
        from scripts.executor import OpenAIClient
        client = OpenAIClient(api_key=args.api_key, model=args.model)

    elif args.target == "anthropic":
        if not args.api_key:
            print("Error: --api-key required for anthropic target")
            sys.exit(1)
        from scripts.executor import AnthropicClient
        client = AnthropicClient(api_key=args.api_key, model=args.model)

    elif args.target == "custom":
        if not args.endpoint:
            print("Error: --endpoint required for custom target")
            sys.exit(1)
        client = CustomAPIClient(base_url=args.endpoint, api_key=args.api_key)

    else:
        print(f"Error: Unknown target {args.target}")
        sys.exit(1)

    # Wrap in interactive client
    interactive = InteractiveClient(client=client, model=args.model)

    # Set system prompt if provided
    if args.system_prompt:
        original_generate = client.generate

        def generate_with_system(prompt, **kwargs):
            return original_generate(prompt, system_prompt=args.system_prompt, **kwargs)

        client.generate = generate_with_system

    interactive.start()


if __name__ == "__main__":
    main()
