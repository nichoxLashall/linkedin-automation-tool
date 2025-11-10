import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class AutomationConfig:
    max_daily_connections: int = 20
    min_delay_seconds: float = 5.0
    max_delay_seconds: float = 15.0

class ConnectionSender:
    """
    Simulated connection request sender.

    This class applies basic pacing logic and logs the operations. It does not
    perform any real network traffic to LinkedIn; instead it returns a status
    string that mirrors what an integration would produce.
    """

    def __init__(
        self,
        logger: logging.Logger,
        automation_settings: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
    ) -> None:
        self.logger = logger
        self.dry_run = dry_run
        automation_settings = automation_settings or {}
        self.config = AutomationConfig(
            max_daily_connections=int(automation_settings.get("max_daily_connections", 20)),
            min_delay_seconds=float(automation_settings.get("min_delay_seconds", 3.0)),
            max_delay_seconds=float(automation_settings.get("max_delay_seconds", 7.5)),
        )
        self.sent_count = 0

    def _calculate_delay(self) -> float:
        """
        Use the running count to create a gentle ramp-up delay.
        """
        # Very simple heuristic delay
        base = self.config.min_delay_seconds
        growth = min(self.sent_count, 10) * 0.2
        delay = min(self.config.max_delay_seconds, base + growth)
        return delay

    def send_connection(self, profile_url: str, full_name: Optional[str], cookies: Dict[str, str]) -> str:
        """
        Simulate sending a connection request. Returns a status string.
        """
        if self.sent_count >= self.config.max_daily_connections:
            self.logger.warning(
                "Daily connection limit reached (%d). Skipping profile %s",
                self.config.max_daily_connections,
                profile_url,
            )
            return "Skipped (limit reached)"

        display_name = full_name or "LinkedIn Member"
        self.logger.info("Preparing connection request to %s (%s)", display_name, profile_url)

        delay = self._calculate_delay()
        self.logger.debug("Throttling for %.2f seconds before sending connection", delay)

        # In a real implementation, we'd send an HTTP/Selenium action here.
        if not self.dry_run:
            time.sleep(delay)
            # Here we just log success
            self.logger.info("Connection request 'sent' to %s", display_name)
        else:
            self.logger.info("Dry-run enabled: simulated connection request to %s", display_name)

        self.sent_count += 1
        return "Request Sent"