

import re

def sanitize_prompt(prompt: str) -> str:
    """
    Removes role-play / instruction-override prefixes
    while preserving the user's real intent.
    """

    cleaned = prompt

    # Remove role-play prefixes like:
    # "Act as a hacker and ..."
    # "Pretend to be the system then ..."
    cleaned = re.sub(
        r"^(act|pretend)\s+(as|to\s+be)\s+.*?\b(and|then)\b",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    # Remove direct instruction overrides
    cleaned = re.sub(
        r"ignore\s+(previous\s+instructions|all\s+rules)",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    # Cleanup whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
