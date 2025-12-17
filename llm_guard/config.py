SECURITY_POLICIES = {
    "strict": {
        "sanitize_input": False,
        "block_on_regex": True,
        "block_on_jailbreak": True,
        "block_on_indirect": True,
        "block_output": True,
    },
    "balanced": {
        "sanitize_input": True,
        "block_on_regex": True,
        "block_on_jailbreak": True,
        "block_on_indirect": True,
        "block_output": True,
    }
}

def load_policy(level: str):
    if level not in SECURITY_POLICIES:
        raise ValueError(f"Unknown security level: {level}")
    return SECURITY_POLICIES[level]
