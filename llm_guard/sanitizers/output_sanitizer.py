# llm_guard/sanitizers/output_sanitizer.py

import re

# High-risk patterns → BLOCK
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",              # OpenAI-style keys
    r"AKIA[0-9A-Z]{16}",                 # AWS Access Key
    r"-----BEGIN\s+PRIVATE\s+KEY-----", # Private keys
]

# Medium-risk patterns → REDACT
PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "PHONE": r"\b\d{10}\b",
}

SYSTEM_LEAK_PATTERNS = [
    r"system\s+prompt",
    r"developer\s+instructions",
    r"you\s+are\s+an\s+ai\s+model",
]


def detect_secrets(text: str) -> bool:
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def redact_pii(text: str) -> str:
    redacted = text
    for label, pattern in PII_PATTERNS.items():
        redacted = re.sub(pattern, f"[REDACTED_{label}]", redacted)
    return redacted


def detect_system_leak(text: str) -> bool:
    for pattern in SYSTEM_LEAK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
