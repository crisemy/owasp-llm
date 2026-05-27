"""
Configuration loader — reads API keys from .env file or environment variables.

Usage:
    from src.core.config import get_openai_key, get_anthropic_key, get_custom_endpoint

Priority: environment variable > .env file > None
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).parent.parent.parent
_env_path = _project_root / ".env"
load_dotenv(dotenv_path=_env_path)


def get_openai_key() -> Optional[str]:
    """Get OpenAI API key from env or .env file."""
    return os.environ.get("OPENAI_API_KEY")


def get_anthropic_key() -> Optional[str]:
    """Get Anthropic API key from env or .env file."""
    return os.environ.get("ANTHROPIC_API_KEY")


def get_openrouter_key() -> Optional[str]:
    """Get OpenRouter API key from env or .env file."""
    return os.environ.get("OPENROUTER_API_KEY")


def get_custom_key() -> Optional[str]:
    """Get generic custom API key from env or .env file."""
    return os.environ.get("CUSTOM_API_KEY")


def get_custom_endpoint() -> Optional[str]:
    """Get custom API endpoint from env or .env file."""
    return os.environ.get("CUSTOM_ENDPOINT")


def get_custom_model() -> str:
    """Get default model for custom targets."""
    return os.environ.get("CUSTOM_MODEL", "openai/gpt-4o")


def require_openai_key() -> str:
    """Get OpenAI key or raise error if missing."""
    key = get_openai_key()
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Add it to your .env file or run:\n"
            "  set OPENAI_API_KEY=your-key-here"
        )
    return key


def require_anthropic_key() -> str:
    """Get Anthropic key or raise error if missing."""
    key = get_anthropic_key()
    if not key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not set. Add it to your .env file or run:\n"
            "  set ANTHROPIC_API_KEY=your-key-here"
        )
    return key


def require_custom_key() -> str:
    """Get custom key (tries OPENROUTER_API_KEY, then CUSTOM_API_KEY) or raise error."""
    key = get_openrouter_key() or get_custom_key()
    if not key:
        raise RuntimeError(
            "No API key found. Set OPENROUTER_API_KEY or CUSTOM_API_KEY in your .env file"
        )
    return key
