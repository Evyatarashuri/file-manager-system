import re
from app.config.logging import get_logger

logger = get_logger("text-cleaner")


class TextCleaner:
    """Normalizes extracted text for indexing and search."""

    def clean(self, text: str) -> str:
        logger.info("WORKER: Starting text cleaning")

        if not text or not isinstance(text, str):
            logger.warning("Empty or invalid text provided to cleaner")
            return ""

        original_len = len(text)

        # Normalization
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Whitespace cleanup
        text = re.sub(r"\s+", " ", text).strip()

        logger.info(f"Text cleaning finished — reduced to {len(text)} chars from {original_len}")
        return text
