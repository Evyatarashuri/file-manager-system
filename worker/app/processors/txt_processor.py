import re
from app.config.logging import get_logger

logger = get_logger("txt-processor")

class TxtProcessor:
    """Handles text extraction from .txt files with multiple encoding fallback."""

    SUPPORTED_ENCODINGS = ("utf-8", "utf-16", "latin-1", "windows-1255")

    def extract_text(self, raw_bytes: bytes) -> str:
        logger.info(f"WORKER: Extracting TXT — size={len(raw_bytes)} bytes")

        for enc in self.SUPPORTED_ENCODINGS:
            try:
                text = raw_bytes.decode(enc)
                logger.info(f"Decoded TXT using encoding={enc}")
                break
            except UnicodeDecodeError:
                continue
        else:
            logger.warning("Fallback decoding used — latin-1 (lossy)")
            text = raw_bytes.decode("latin-1", errors="ignore")

        # normalize for indexing/search
        text = re.sub(r"\s+", " ", text).strip()
        return text
