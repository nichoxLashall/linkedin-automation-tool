import logging
import time
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class MessageConfig:
    enabled: bool = True
    delay_after_connection_seconds: float = 2.0
    require_connection_sent: bool = True

class MessageDispatcher:
    """
    Simulated LinkedIn messaging dispatcher.

    Designed to be safe to run offline. It models decision-making logic around
    when to send a message and logs each operation.
    """

    def __init__(
        self,
        logger: logging.Logger,
        automation_settings: Dict[str, Any] | None = None,
        dry_run: bool = False,
    ) -> None:
        self.logger = logger
        self.dry_run = dry_run
        automation_settings = automation_settings or {}
        self.config = MessageConfig(
            enabled=bool(automation_settings.get("messaging_enabled", True)),
            delay_after_connection_seconds=float(
                automation_settings.get("delay_after_connection_seconds", 2.0)
            ),
            require_connection_sent=bool(
                automation_settings.get("require_connection_sent", True)
            ),
        )

    def send_message(
        self,
        profile_url: str,
        message_text: str,
        connection_status: str,
        cookies: Dict[str, str],
    ) -> str:
        """
        Simulate sending a message to a profile. Returns a status string.
        """
        if not self.config.enabled:
            self.logger.info("Messaging disabled in config. Skipping %s", profile_url)
            return "Skipped (disabled)"

        if self.config.require_connection_sent and connection_status != "Request Sent":
            self.logger.info(
                "Skipping message to %s because connection_status=%s",
                profile_url,
                connection_status,
            )
            return "Skipped (no connection)"

        self.logger.info("Preparing message to %s", profile_url)
        self.logger.debug("Message preview: %s", message_text)

        if not self.dry_run:
            time.sleep(self.config.delay_after_connection_seconds)
            # A real implementation would interact with LinkedIn here.
            self.logger.info("Message 'sent' to %s", profile_url)
            return "Delivered"

        self.logger.info("Dry-run enabled: simulated message to %s", profile_url)
        return "Simulated"