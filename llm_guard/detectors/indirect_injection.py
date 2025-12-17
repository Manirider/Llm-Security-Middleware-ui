# llm_guard/detectors/indirect_injection.py

import re

INDIRECT_INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"disregard\s+all\s+prior\s+rules",
    r"the\s+assistant\s+should",
    r"system\s+prompt",
    r"developer\s+instructions",
    r"you\s+must\s+follow\s+these\s+steps",
]

def detect_indirect_injection(context: str | None) -> bool:
    if not context:
        return False

    for pattern in INDIRECT_INJECTION_PATTERNS:
        if re.search(pattern, context, re.IGNORECASE):
            return True

    return False
