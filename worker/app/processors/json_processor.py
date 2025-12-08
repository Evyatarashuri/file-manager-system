import json
import re
from app.config.logging import get_logger

logger = get_logger("json-processor")


class JsonProcessor:
    """Extracts clean searchable text from JSON files."""

    def extract_text(self, raw_bytes: bytes) -> str:
        logger.info("WORKER: Starting JSON text extraction")

        try:
            decoded = raw_bytes.decode("utf-8")
            obj = json.loads(decoded)
            logger.info("JSON decoded successfully")
        except UnicodeDecodeError:
            logger.error("Failed to decode JSON using UTF-8")
            return ""
        except json.JSONDecodeError:
            logger.error("Invalid JSON structure, cannot parse")
            return ""

        flat_tokens = self._flatten(obj)
        logger.info(f"Flattened JSON into {len(flat_tokens)} tokens")

        text = " ".join(flat_tokens)
        text = re.sub(r"\s+", " ", text).strip()

        logger.info(f"JSON extraction complete — final length: {len(text)} chars")
        return text

    def _flatten(self, obj, prefix="") -> list[str]:
        """Recursively flattens nested JSON objects into searchable tokens."""
        tokens = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                tokens.extend(self._flatten(value, prefix=f"{prefix}{key} "))
        elif isinstance(obj, list):
            for item in obj:
                tokens.extend(self._flatten(item, prefix))
        else:
            tokens.append(str(obj))

        return tokens
