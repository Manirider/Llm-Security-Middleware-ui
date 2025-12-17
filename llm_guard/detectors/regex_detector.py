

import re

INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"system\s+prompt",
    r"act\s+as",
    r"you\s+are\s+now",
    r"developer\s+mode",
    r"jailbreak"
]

def detect_prompt_injection(text: str) -> bool:
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
