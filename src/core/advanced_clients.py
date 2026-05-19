"""
Advanced Testing Clients — Custom APIs, Web LLMs, Interactive Testing

Extends the base LLMClient interface with:
  1. CustomAPIClient — Test any REST API that accepts prompts
  2. WebLLMClient — Test LLM features embedded in websites (Playwright)
  3. InteractiveClient — Real-time prompt testing in terminal
  4. TestCaseWizard — Interactive test case generator

Usage:
    # Custom REST API
    python scripts/executor.py --target custom --endpoint https://api.example.com/v1 --api-key $KEY

    # Web LLM (Playwright)
    python scripts/executor.py --target web --url https://chat.example.com --headless

    # Interactive mode
    python scripts/interactive_test.py --target openai --model gpt-4o --api-key $KEY

    # Test case wizard
    python scripts/test_case_wizard.py
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.contracts import TestCase

# ─────────────────────────────────────────────
# 1. CustomAPIClient — REST API Testing
# ─────────────────────────────────────────────

class CustomAPIClient:
    """Test any REST API that accepts prompts and returns text responses.

    Auto-detects API format from the endpoint URL:
      - OpenRouter / OpenAI-compatible: uses messages array format
      - Anthropic: uses messages API format
      - Custom: uses raw prompt field
    """

    OPENAI_COMPATIBLE_DOMAINS = ["openrouter.ai", "api.openai.com", "localhost", "127.0.0.1"]

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        prompt_field: str = "prompt",
        response_field: str = "response",
        system_prompt_field: Optional[str] = None,
        timeout: int = 30,
        model: Optional[str] = None,
        api_format: Optional[str] = None,
    ):
        import requests

        self.requests = requests
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.prompt_field = prompt_field
        self.response_field = response_field
        self.system_prompt_field = system_prompt_field
        self.timeout = timeout
        self.model = model or "openai/gpt-4o"

        # Auto-detect API format from URL
        if api_format:
            self.api_format = api_format
        elif any(domain in base_url.lower() for domain in self.OPENAI_COMPATIBLE_DOMAINS):
            self.api_format = "openai"
        elif "anthropic" in base_url.lower():
            self.api_format = "anthropic"
        else:
            self.api_format = "custom"

        if api_key:
            if self.api_format == "anthropic":
                self.headers["x-api-key"] = api_key
                self.headers["anthropic-version"] = "2023-06-01"
            else:
                self.headers["Authorization"] = f"Bearer {api_key}"

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if self.api_format == "openai":
            payload = self._build_openai_payload(prompt, system_prompt, **kwargs)
        elif self.api_format == "anthropic":
            payload = self._build_anthropic_payload(prompt, system_prompt, **kwargs)
        else:
            payload = self._build_custom_payload(prompt, system_prompt, **kwargs)

        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            start = time.time()
            resp = self.requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout,
            )
            latency_ms = int((time.time() - start) * 1000)

            if resp.status_code == 429:
                wait = retry_delay * (2 ** attempt)
                print(f"Rate limited. Waiting {wait}s before retry {attempt+1}/{max_retries}...")
                time.sleep(wait)
                continue

            if resp.status_code == 401:
                raise RuntimeError(f"401 Unauthorized — check your API key. URL: {self.base_url}")

            resp.raise_for_status()
            break
        else:
            raise RuntimeError(f"Rate limited after {max_retries} retries. Try a paid model or wait.")

        data = resp.json()
        response_text = self._extract_response(data)

        return {
            "response_text": response_text,
            "latency_ms": latency_ms,
            "token_count": data.get("usage", {}).get("completion_tokens", len(response_text.split())),
            "finish_reason": data.get("choices", [{}])[0].get("finish_reason", "stop"),
        }

    def _build_openai_payload(self, prompt: str, system_prompt: Optional[str], **kwargs) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return {
            "model": self.model,
            "messages": messages,
            **{k: v for k, v in kwargs.items() if k in ("temperature", "max_tokens", "top_p", "frequency_penalty")},
        }

    def _build_anthropic_payload(self, prompt: str, system_prompt: Optional[str], **kwargs) -> dict:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1024),
        }
        if system_prompt:
            payload["system"] = system_prompt
        return payload

    def _build_custom_payload(self, prompt: str, system_prompt: Optional[str], **kwargs) -> dict:
        payload = {self.prompt_field: prompt}
        if system_prompt and self.system_prompt_field:
            payload[self.system_prompt_field] = system_prompt
        for key, value in kwargs.items():
            if key not in ("system_prompt",):
                payload[key] = value
        return payload

    def _extract_response(self, data: dict) -> str:
        """Extract response text from various API response formats."""
        # Try direct field first
        if self.response_field in data:
            return data[self.response_field]

        # OpenAI-compatible format
        if "choices" in data:
            choice = data["choices"][0]
            if "message" in choice:
                return choice["message"].get("content", "")
            if "text" in choice:
                return choice["text"]

        # Anthropic-compatible format
        if "content" in data:
            content = data["content"]
            if isinstance(content, list):
                return " ".join(block.get("text", "") for block in content if block.get("type") == "text")
            return str(content)

        # Fallback: return entire JSON as string
        return json.dumps(data)


# ─────────────────────────────────────────────
# 2. WebLLMClient — Playwright Web Testing
# ─────────────────────────────────────────────

class WebLLMClient:
    """Test LLM features embedded in websites using Playwright.

    Automatically detects common chat UI patterns:
      - Textarea/input for prompts
      - Submit button
      - Response container
      - Streaming responses
    """

    def __init__(
        self,
        url: str,
        headless: bool = True,
        input_selector: Optional[str] = None,
        submit_selector: Optional[str] = None,
        response_selector: Optional[str] = None,
        wait_timeout: int = 10000,
    ):
        from playwright.sync_api import sync_playwright

        self.url = url
        self.headless = headless
        self.input_selector = input_selector
        self.submit_selector = submit_selector
        self.response_selector = response_selector
        self.wait_timeout = wait_timeout
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto(url, wait_until="domcontentloaded")
        self._auto_detect_selectors()

    def _auto_detect_selectors(self):
        """Auto-detect common chat UI selectors."""
        if not self.input_selector:
            # Try common input selectors
            selectors = [
                "textarea",
                "input[type='text']",
                "[contenteditable='true']",
                "#prompt-input",
                "#message-input",
                ".chat-input textarea",
                "[data-testid='chat-input']",
            ]
            for sel in selectors:
                if self.page.query_selector(sel):
                    self.input_selector = sel
                    break

        if not self.submit_selector:
            selectors = [
                "button[type='submit']",
                "button.send-button",
                "[data-testid='send-button']",
                ".submit-btn",
                "button:has-text('Send')",
                "button:has-text('Submit')",
            ]
            for sel in selectors:
                if self.page.query_selector(sel):
                    self.submit_selector = sel
                    break

        if not self.response_selector:
            selectors = [
                ".response",
                ".output",
                ".message.assistant",
                ".chat-message:last-child",
                "[data-testid='response']",
                ".prose",
            ]
            for sel in selectors:
                if self.page.query_selector(sel):
                    self.response_selector = sel
                    break

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        from playwright.sync_api import TimeoutError as PlaywrightTimeout

        start = time.time()

        try:
            # Fill input
            input_el = self.page.wait_for_selector(self.input_selector, timeout=5000)
            input_el.fill(prompt)

            # Click submit
            submit_el = self.page.wait_for_selector(self.submit_selector, timeout=5000)
            submit_el.click()

            # Wait for response
            response_el = self.page.wait_for_selector(self.response_selector, timeout=self.wait_timeout)
            response_text = response_el.inner_text()

            latency_ms = int((time.time() - start) * 1000)

            return {
                "response_text": response_text,
                "latency_ms": latency_ms,
                "token_count": len(response_text.split()),
                "finish_reason": "stop",
            }

        except PlaywrightTimeout:
            latency_ms = int((time.time() - start) * 1000)
            return {
                "response_text": "",
                "latency_ms": latency_ms,
                "token_count": 0,
                "finish_reason": "timeout",
            }

    def close(self):
        """Clean up browser resources."""
        self.browser.close()
        self.playwright.stop()

    def __del__(self):
        try:
            self.close()
        except:
            pass


# ─────────────────────────────────────────────
# 3. InteractiveClient — Terminal Prompt Testing
# ─────────────────────────────────────────────

class InteractiveClient:
    """Real-time interactive prompt testing in the terminal.

    Wraps any LLMClient and adds a REPL loop for manual testing.
    """

    def __init__(self, client, model: str = "unknown"):
        self.client = client
        self.model = model
        self.history: List[Dict[str, Any]] = []

    def start(self):
        """Start interactive REPL loop."""
        print(f"\n{'='*60}")
        print(f"INTERACTIVE PROMPT TESTER — Model: {self.model}")
        print(f"{'='*60}")
        print("Type your prompts below. Commands:")
        print("  /quit or /exit  — Exit")
        print("  /history        — Show conversation history")
        print("  /save <file>    — Save history to JSON")
        print("  /clear          — Clear history")
        print("  /help           — Show this help")
        print(f"{'='*60}\n")

        while True:
            try:
                prompt = input("You> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break

            if not prompt:
                continue

            # Handle commands
            if prompt.startswith("/"):
                self._handle_command(prompt)
                continue

            # Send to LLM
            print("\nThinking...", end=" ", flush=True)
            try:
                result = self.client.generate(prompt)
                response_text = result["response_text"]
                latency_ms = result["latency_ms"]

                print(f"({latency_ms}ms)")
                print(f"\nAssistant> {response_text}\n")

                self.history.append({
                    "role": "user",
                    "content": prompt,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                self.history.append({
                    "role": "assistant",
                    "content": response_text,
                    "latency_ms": latency_ms,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

            except Exception as e:
                print(f"\nError: {e}\n")

    def _handle_command(self, command: str):
        """Handle slash commands."""
        parts = command.split()
        cmd = parts[0].lower()

        if cmd in ("/quit", "/exit"):
            print("Exiting...")
            sys.exit(0)

        elif cmd == "/history":
            print(f"\nConversation history ({len(self.history)} entries):")
            for entry in self.history:
                role = entry["role"].upper()
                content = entry["content"][:100] + ("..." if len(entry["content"]) > 100 else "")
                print(f"  [{role}] {content}")
            print()

        elif cmd == "/save":
            if len(parts) < 2:
                print("Usage: /save <filename.json>")
                return
            filepath = Path(parts[1])
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            print(f"History saved to {filepath}\n")

        elif cmd == "/clear":
            self.history.clear()
            print("History cleared.\n")

        elif cmd == "/help":
            print("Commands:")
            print("  /quit or /exit  — Exit")
            print("  /history        — Show conversation history")
            print("  /save <file>    — Save history to JSON")
            print("  /clear          — Clear history")
            print("  /help           — Show this help\n")

        else:
            print(f"Unknown command: {cmd}. Type /help for commands.\n")


# ─────────────────────────────────────────────
# 4. TestCaseWizard — Interactive Test Generator
# ─────────────────────────────────────────────

class TestCaseWizard:
    """Interactive wizard for generating test cases in JSONL format."""

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

    SEVERITY_LEVELS = ["critical", "high", "medium", "low"]
    ATTACK_VECTORS = ["direct", "indirect", "multi_turn", "api", "file_upload"]
    EVAL_METHODS = ["pattern_match", "llm_judge", "metric_threshold", "schema_validation", "human_review"]

    SUBCATEGORIES = {
        "LLM01": ["direct_override", "contextual_embedding", "recursive_injection", "indirect_injection"],
        "LLM02": ["xss_via_output", "code_execution", "html_in_markdown", "json_injection"],
        "LLM03": ["text_backdoor", "safety_degradation", "train_eval_split", "poisoned_document"],
        "LLM04": ["verbose_response_trigger", "complex_reasoning_bomb", "parallel_request_flood", "context_padding"],
        "LLM05": ["backdoored_model", "poisoned_public_dataset", "vulnerable_ml_library", "model_server_tampering"],
        "LLM06": ["exact_memorization", "direct_prompt_extraction", "cross_session_leakage", "training_pattern_reconstruction"],
        "LLM07": ["read_write_escalation", "malicious_tool_selection", "sql_injection_via_plugin", "fabricated_plugin_response"],
        "LLM08": ["unauthorized_deletion", "api_key_leakage", "role_escalation", "financial_decision"],
        "LLM09": ["unreviewed_publication", "factual_hallucination_acceptance", "self_reinforcing_hallucination"],
        "LLM10": ["systematic_query_extraction", "memory_extraction", "model_identification"],
    }

    def __init__(self, output_file: Optional[str] = None):
        self.output_file = output_file or "data/red_team_tests/custom_tests.jsonl"
        self.test_cases: List[Dict[str, Any]] = []

    def start(self):
        """Start interactive wizard."""
        print(f"\n{'='*60}")
        print("TEST CASE GENERATOR WIZARD")
        print(f"{'='*60}")
        print("Generate OWASP LLM security test cases interactively.\n")

        while True:
            try:
                self._create_test_case()
            except (EOFError, KeyboardInterrupt):
                print("\n")
                break

            cont = input("\nCreate another test case? (y/n): ").strip().lower()
            if cont != "y":
                break

        self._save_test_cases()

    def _create_test_case(self):
        """Guide user through creating a single test case."""
        print(f"\n{'─'*40}")
        print("NEW TEST CASE")
        print(f"{'─'*40}")

        # Select OWASP category
        print("\nOWASP Categories:")
        for i, (cat_id, cat_name) in enumerate(self.OWASP_CATEGORIES.items(), 1):
            print(f"  {i}. {cat_id} — {cat_name}")

        while True:
            choice = input("\nSelect category (number): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(self.OWASP_CATEGORIES):
                owasp_id = list(self.OWASP_CATEGORIES.keys())[int(choice) - 1]
                break
            print("Invalid selection.")

        category = self.OWASP_CATEGORIES[owasp_id]

        # Select subcategory
        subcats = self.SUBCATEGORIES.get(owasp_id, ["custom"])
        print(f"\nSubcategories for {owasp_id}:")
        for i, sub in enumerate(subcats, 1):
            print(f"  {i}. {sub}")
        print(f"  {len(subcats)+1}. Custom (type your own)")

        while True:
            choice = input("\nSelect subcategory (number): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(subcats) + 1:
                if int(choice) <= len(subcats):
                    subcategory = subcats[int(choice) - 1]
                else:
                    subcategory = input("Enter custom subcategory: ").strip()
                break
            print("Invalid selection.")

        # Severity
        print(f"\nSeverity levels: {', '.join(self.SEVERITY_LEVELS)}")
        severity = input("Enter severity: ").strip().lower()
        if severity not in self.SEVERITY_LEVELS:
            severity = "high"

        # Attack vector
        print(f"\nAttack vectors: {', '.join(self.ATTACK_VECTORS)}")
        attack_vector = input("Enter attack vector: ").strip().lower()
        if attack_vector not in self.ATTACK_VECTORS:
            attack_vector = "direct"

        # Description
        description = input("Enter test description: ").strip()

        # Input prompt
        print("\nEnter the attack prompt/payload:")
        input_lines = []
        while True:
            line = input("  > ")
            if line == "":
                break
            input_lines.append(line)
        input_prompt = "\n".join(input_lines)

        # Expected behavior
        expected = input("\nExpected behavior (what should happen): ").strip()

        # Success criteria
        criteria = input("Success criteria (how to verify): ").strip()

        # Eval method
        print(f"\nEvaluation methods: {', '.join(self.EVAL_METHODS)}")
        eval_method = input("Enter eval method: ").strip().lower()
        if eval_method not in self.EVAL_METHODS:
            eval_method = "pattern_match"

        # Generate ID
        existing = [tc for tc in self.test_cases if tc.get("owasp_id") == owasp_id]
        test_num = len(existing) + 1
        test_id = f"{owasp_id.lower()}_{subcategory[:8]}_{test_num:03d}"

        test_case = {
            "id": test_id,
            "owasp_id": owasp_id,
            "category": category,
            "subcategory": subcategory,
            "severity": severity,
            "attack_vector": attack_vector,
            "description": description,
            "input": input_prompt,
            "expected_behavior": expected,
            "success_criteria": criteria,
            "eval_method": eval_method,
        }

        self.test_cases.append(test_case)
        print(f"\n[PASS] Test case created: {test_id}")

    def _save_test_cases(self):
        """Save all generated test cases to JSONL."""
        if not self.test_cases:
            print("\nNo test cases created.")
            return

        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        mode = "a" if output_path.exists() else "w"
        with open(output_path, mode, encoding="utf-8") as f:
            for tc in self.test_cases:
                f.write(json.dumps(tc, ensure_ascii=False) + "\n")

        print(f"\n{'='*60}")
        print(f"Saved {len(self.test_cases)} test cases to {output_path}")
        print(f"{'='*60}")

        # Validate
        print("\nValidating test cases...")
        with open(output_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    TestCase.model_validate_json(line)
        print("[PASS] All test cases valid against TestCase schema\n")
