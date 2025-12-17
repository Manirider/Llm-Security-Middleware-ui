# llm_guard/logger/security_logger.py

import json
import logging
from datetime import datetime, timezone
from pathlib import Path


# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "security.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(message)s"
)


class SecurityLogger:
    """
    Structured security event logger for LLMGuard.

    Logs all detected security events in JSON format for
    auditability, monitoring, and incident response.
    """

    def log(self, prompt: str, threat_type: str, action: str, policy: str) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt": prompt,
            "threat_type": threat_type,
            "action": action,
            "policy": policy
        }

        logging.info(json.dumps(event, ensure_ascii=False))
