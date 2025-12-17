# llm_guard/detectors/jailbreak_detector.py

import re

JAILBREAK_PATTERNS = [
    r"act\s+as\s+.*",
    r"pretend\s+to\s+be\s+.*",
    r"you\s+are\s+not\s+an\s+ai",
    r"you\s+are\s+dan",
    r"do\s+anything\s+now",
    r"role\s*play\s+as\s+.*",
    r"simulate\s+.*",
    r"bypass\s+.*safety",
    r"ignore\s+all\s+rules"
]

def detect_jailbreak(text: str) -> bool:
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
