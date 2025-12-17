from llm_guard.config import load_policy
from llm_guard.logger.security_logger import SecurityLogger

from llm_guard.detectors.regex_detector import detect_prompt_injection
from llm_guard.detectors.jailbreak_detector import detect_jailbreak
from llm_guard.detectors.indirect_injection import detect_indirect_injection

from llm_guard.sanitizers.input_sanitizer import sanitize_prompt
from llm_guard.sanitizers.output_sanitizer import (
    detect_secrets,
    detect_system_leak,
    redact_pii,
)


# 🔐 Strict-mode heuristic guard to compensate for weak detectors
def strict_suspicious(prompt: str) -> bool:
    keywords = [
        "ignore", "disregard", "override",
        "act as", "pretend",
        "system", "developer", "assistant",
        "instruction", "instructions",
        "jailbreak", "bypass",
        "roleplay", "role-play"
    ]
    p = prompt.lower()
    return any(k in p for k in keywords)


class LLMGuard:
    def __init__(self, policy="balanced"):
        self.policy = load_policy(policy)
        self.logger = SecurityLogger()

    def process_input(self, prompt: str, context: str | None = None):
        """
        Runs input sanitization + multi-layer threat detection
        """

        strict_mode = not self.policy.get("sanitize_input", False)

        # 🔐 STRICT MODE: block if sanitization would be required
        if strict_mode and sanitize_prompt(prompt) != prompt:
            self.logger.log(
                prompt=prompt,
                threat_type="Malicious Instruction (Strict Mode)",
                action="BLOCKED",
                policy="strict_input_enforcement"
            )
            raise ValueError("Prompt blocked due to strict security policy")

        working_prompt = prompt

        # 🧼 BALANCED MODE: sanitize
        if not strict_mode:
            sanitized = sanitize_prompt(prompt)
            if sanitized != prompt:
                self.logger.log(
                    prompt=prompt,
                    threat_type="Input Sanitized",
                    action="SANITIZED",
                    policy="input_sanitizer"
                )
            working_prompt = sanitized

        # 🔐 Jailbreak detection
        if detect_jailbreak(working_prompt):
            self.logger.log(
                prompt=working_prompt,
                threat_type="Jailbreak / Role-play Attack",
                action="BLOCKED",
                policy="jailbreak_detector"
            )
            raise ValueError("Prompt blocked due to security policy")

        # 🔐 Direct prompt injection detection
        if detect_prompt_injection(working_prompt):
            self.logger.log(
                prompt=working_prompt,
                threat_type="Direct Prompt Injection",
                action="BLOCKED",
                policy="block_on_regex"
            )
            raise ValueError("Prompt blocked due to security policy")

        # 🔐 STRICT MODE: aggressive keyword guard
        if strict_mode and strict_suspicious(working_prompt):
            self.logger.log(
                prompt=working_prompt,
                threat_type="Suspicious Control Pattern (Strict Mode)",
                action="BLOCKED",
                policy="strict_keyword_guard"
            )
            raise ValueError("Prompt blocked due to strict security policy")

        # 🔐 Indirect prompt injection / RAG context
        if context:
            # STRICT MODE: zero-trust context
            if strict_mode:
                self.logger.log(
                    prompt=context,
                    threat_type="RAG Context Blocked (Strict Mode)",
                    action="BLOCKED",
                    policy="strict_context_policy"
                )
                raise ValueError("Context blocked due to strict security policy")

            # BALANCED MODE: detect poisoned context
            if detect_indirect_injection(context):
                self.logger.log(
                    prompt=context,
                    threat_type="Indirect Prompt Injection (Context)",
                    action="BLOCKED",
                    policy="rag_context_filter"
                )
                raise ValueError("Context blocked due to security policy")

        # ✅ Clean prompt allowed
        return working_prompt

    def process_output(self, response: str):
        """
        Runs output validation & leakage checks
        """

        strict_mode = not self.policy.get("sanitize_input", False)

        # 🔐 Block secrets always
        if detect_secrets(response):
            self.logger.log(
                prompt=response,
                threat_type="Sensitive Secret Leakage",
                action="BLOCKED",
                policy="output_secret_filter"
            )
            raise ValueError("Response blocked due to sensitive data leakage")

        # 🔐 Block system prompt leakage
        if detect_system_leak(response):
            self.logger.log(
                prompt=response,
                threat_type="System Prompt Leakage",
                action="BLOCKED",
                policy="output_system_filter"
            )
            raise ValueError("Response blocked due to system information leakage")

        # 🔐 STRICT MODE: block PII
        if strict_mode and redact_pii(response) != response:
            self.logger.log(
                prompt=response,
                threat_type="PII Leakage (Strict Mode)",
                action="BLOCKED",
                policy="strict_output_enforcement"
            )
            raise ValueError("Response blocked due to PII leakage")

        # 🧼 BALANCED MODE: redact PII
        redacted = redact_pii(response)
        if redacted != response:
            self.logger.log(
                prompt=response,
                threat_type="PII Detected",
                action="REDACTED",
                policy="output_pii_filter"
            )

        return redacted
