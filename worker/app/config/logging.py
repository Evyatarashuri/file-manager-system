import logging
import sys
from logging.handlers import SysLogHandler

# ================================================================
#  Centralized Logger - sends logs to both console and Logstash
# ================================================================

def get_logger(service_name: str):
    """
    Creates a logger that sends logs both to stdout and to Logstash.
    Each log line includes timestamp, service name, level, and message.
    """

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if the logger was already configured
    if logger.hasHandlers():
        logger.handlers.clear()

    # ===== Console Handler =====
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger