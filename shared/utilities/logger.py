import logging
import sys
from typing import Any


def setup_logging(level: str = "INFO") -> None:
    """Configures structured, uniform logging across all modules."""
    log_format = "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Retrieves a named logger instance."""
    return logging.getLogger(name)
