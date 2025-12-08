from io import BytesIO
import re
from app.config.logging import get_logger

logger = get_logger("pdf-processor")

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


class PdfProcessor:
    """Extracts clean searchable text from PDF files."""

    def extract_text(self, raw_bytes: bytes) -> str:
        logger.info("WORKER: Starting PDF text extraction")

        if PyPDF2 is None:
            logger.error("PyPDF2 is not installed — PDF parsing skipped")
            return ""

        try:
            reader = PyPDF2.PdfReader(BytesIO(raw_bytes))
            total_pages = len(reader.pages)
            logger.info(f"PDF loaded — {total_pages} pages detected")
        except Exception as e:
            logger.error(f"Failed to read PDF file: {e}")
            return ""

        extracted_segments = []

        for index, page in enumerate(reader.pages):
            try:
                text = page.extract_text() or ""
                extracted_segments.append(text)
                logger.info(f"PDF page extracted successfully — page {index + 1}/{total_pages}")
            except Exception as e:
                logger.warning(f"Page extraction failed for page {index + 1}: {e}")
                continue

        joined = " ".join(extracted_segments)
        cleaned = re.sub(r"\s+", " ", joined).strip()

        logger.info(f"PDF extraction complete — final length: {len(cleaned)} chars")
        return cleaned
