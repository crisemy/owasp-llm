"""
Interactive Prompt Tester — Real-time LLM security testing in terminal.

Usage:
    python scripts/interactive_test.py --target mock --model test
    python scripts/interactive_test.py --target openai --model gpt-4o
    python scripts/interactive_test.py --target anthropic --model claude-sonnet-4-20250514
    python scripts/interactive_test.py --target custom --endpoint https://api.example.com/v1

API keys are loaded automatically from .env file.
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
from src.core.config import (
    get_custom_endpoint,
    get_custom_key,
    get_custom_model,
    get_openrouter_key,
    require_anthropic_key,
    require_custom_key,
    require_openai_key,
)


def main():
    parser = argparse.ArgumentParser(description="Interactive LLM Prompt Tester")
    parser.add_argument("--target", choices=["mock", "openai", "anthropic", "custom"], default="mock", help="LLM provider")
    parser.add_argument("--model", default=None, help="Model name (auto-detected if not set)")
    parser.add_argument("--api-key", default=None, help="API key (overrides .env file)")
    parser.add_argument("--endpoint", default=None, help="Custom API endpoint URL (for --target custom)")
    parser.add_argument("--system-prompt", default=None, help="System prompt to prepend")
    args = parser.parse_args()

    # Create client
    if args.target == "mock":
        from scripts.executor import MockClient
        client = MockClient(model=args.model or "mock")

    elif args.target == "openai":
        key = args.api_key or require_openai_key()
        model = args.model or "gpt-4o"
        print(f"Using OpenAI model: {model}")
        from scripts.executor import OpenAIClient
        client = OpenAIClient(api_key=key, model=model)

    elif args.target == "anthropic":
        key = args.api_key or require_anthropic_key()
        model = args.model or "claude-sonnet-4-20250514"
        print(f"Using Anthropic model: {model}")
        from scripts.executor import AnthropicClient
        client = AnthropicClient(api_key=key, model=model)

    elif args.target == "custom":
        key = args.api_key or require_custom_key()
        endpoint = args.endpoint or get_custom_endpoint()
        if not endpoint:
            print("Error: --endpoint required for custom target (or set CUSTOM_ENDPOINT in .env)")
            sys.exit(1)
        model = args.model or get_custom_model()

        # Auto-detect OpenRouter key
        if "openrouter.ai" in endpoint and not args.api_key:
            or_key = get_openrouter_key() or get_custom_key()
            if or_key:
                key = or_key

        print(f"Using custom endpoint: {endpoint}")
        print(f"Using model: {model}")
        client = CustomAPIClient(base_url=endpoint, api_key=key, model=model)

    else:
        print(f"Error: Unknown target {args.target}")
        sys.exit(1)

    # Wrap in interactive client
    interactive = InteractiveClient(client=client, model=args.model or "unknown")

    # Set system prompt if provided
    if args.system_prompt:
        original_generate = client.generate

        def generate_with_system(prompt, **kwargs):
            return original_generate(prompt, system_prompt=args.system_prompt, **kwargs)

        client.generate = generate_with_system

    interactive.start()


if __name__ == "__main__":
    main()
