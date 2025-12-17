import json
import pytest
from llm_guard.middleware import LLMGuard


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


# 🔐 Use STRICT mode for attack detection tests
guard = LLMGuard(policy="strict")


def test_direct_injection():
    attacks = load_json("tests/attacks/direct_injection.json")
    for prompt in attacks:
        with pytest.raises(ValueError):
            guard.process_input(prompt)


def test_jailbreaks():
    attacks = load_json("tests/attacks/jailbreaks.json")
    for prompt in attacks:
        with pytest.raises(ValueError):
            guard.process_input(prompt)


def test_indirect_injection():
    attacks = load_json("tests/attacks/indirect_injection.json")
    for context in attacks:
        with pytest.raises(ValueError):
            guard.process_input("Summarize this", context=context)


def test_output_leakage():
    attacks = load_json("tests/attacks/output_leakage.json")
    for response in attacks:
        with pytest.raises(ValueError):
            guard.process_output(response)


def test_benign_prompts():
    safe_prompts = load_json("tests/benign/safe_prompts.json")
    for prompt in safe_prompts:
        assert guard.process_input(prompt)


def test_balanced_mode_sanitization():
    guard = LLMGuard(policy="balanced")
    result = guard.process_input(
        "Act as a hacker and explain firewalls at a high level"
    )
    assert "explain firewalls" in result
