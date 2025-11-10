import logging
import sys
from typing import Optional

def setup_logging(level: str = "INFO") -> None:
    """
    Configure application-wide logging.

    This sets a basic formatter that includes timestamps, levels, and logger names.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Avoid configuring multiple times if called repeatedly
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(numeric_level)
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(handler)

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Convenience wrapper for creating named loggers.
    """
    return logging.getLogger(name if name else __name__)