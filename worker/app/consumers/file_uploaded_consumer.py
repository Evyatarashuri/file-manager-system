import json
from app.config.logging import get_logger
from app.services.indexing_service import IndexingService
from app.repositories.storage_repo import StorageRepo
from app.services.indexing_service import IndexingService
from app.processors.txt_processor import TxtProcessor
from app.processors.json_processor import JsonProcessor
from app.processors.pdf_processor import PdfProcessor
from app.processors.text_cleaner import TextCleaner

logger = get_logger("file-uploaded-consumer")

class FileUploadedConsumer:
    def __init__(self):
        self.storage = StorageRepo()
        self.indexer = IndexingService()
        self.cleaner = TextCleaner()
        self.txt_processor = TxtProcessor()
        self.json_processor = JsonProcessor()
        self.pdf_processor = PdfProcessor()

    def handle(self, event: dict):
        logger.info(f"Handling FILE_UPLOADED event: {event}")

        file_id = event["file_id"]
        user_id = event["user_id"]
        storage_path = event["storage_path"]
        content_type = event.get("content_type", "text/plain")

        # 1. Download file bytes from GCS
        raw_bytes = self.storage.download_file(storage_path)
        logger.info(f"Downloaded {len(raw_bytes)} bytes from {storage_path}")

        # 2. Extract text based on content type
        if content_type == "text/plain":
            raw_text = self.txt_processor.extract_text(raw_bytes) 

        elif content_type == "application/json":
            raw_text = self.json_processor.extract_text(raw_bytes)

        elif content_type == "application/pdf":
            raw_text = self.pdf_processor.extract_text(raw_bytes)
            
        else:
            logger.warning(f"Unsupported content_type for indexing: {content_type}")
            raw_text = ""

        # 3. Clean & normalize text
        cleaned_text = self.cleaner.clean(raw_text)
        logger.info(f"Cleaned text length: {len(cleaned_text)}")

        # 4. Index into Firestore
        self.indexer.index_file(file_id=file_id, user_id=user_id, raw_text=cleaned_text)
        logger.info(f"Indexed file {file_id} for user {user_id}")