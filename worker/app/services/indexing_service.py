from app.repositories.firestore_repo import FirestoreRepo
from app.utils.backoff import backoff
from app.utils.circuit_breaker import CircuitBreaker, circuit_breaker
from app.utils.idempotency import IdempotencyKey
import re
from collections import Counter
from app.config.logging import get_logger

logger = get_logger("worker-indexing")

cb = CircuitBreaker(failure_threshold=5, recovery_time=20)

class IndexingService:
    def __init__(self):
        self.firestore = FirestoreRepo()

    # -----------------------------
    # Tokenize & Normalize text
    # -----------------------------
    def tokenize(self, text: str) -> list[str]:
        text = text.lower()
        text = re.sub(r"[^a-zA-Zא-ת0-9\s]", " ", text)
        return [t for t in text.split() if len(t) > 2]

    # -----------------------------
    # Build Searchable Index
    # -----------------------------
    def build_search_index(self, text: str) -> dict:
        tokens = self.tokenize(text)
        freq = Counter(tokens)

        return {
            "terms": tokens,
            "freq": dict(freq),
            "unique_terms": len(freq),
            "total_words": len(tokens),
            "preview": " ".join(tokens[:40])
        }

    # -----------------------------
    # INDEXING — Idempotent + Stable
    # -----------------------------
    # @backoff(max_retries=5)
    # @circuit_breaker(cb)
    def index_file(self, file_id: str, user_id: str, raw_text: str):
        """
        Safe to call multiple times — Redis ensures only 1 worker executes.
        """
        # lock using as an Instance of IdempotencyKey class
        lock = IdempotencyKey(f"index:{file_id}", ttl=600)

        # Try to acquire lock - returns True/False
        acquired = lock.acquire()
        logger.info(f"Redis Lock for {file_id} → acquired={acquired}")

        # Lock NOT acquired → meaning indexing already done or in progress
        if not acquired: # acquired is False
            logger.warning(f"SKIPPED — indexing already in progress for {file_id}")
            stored = lock.get_result()
            logger.info(f"Stored cached index exists? → {bool(stored)}")
            return stored or {"status": "processing"}

       # If we reached here → indexing WILL run - aciquire is True
        logger.info(f"Indexing STARTED for file={file_id}, user={user_id}")

        try:
            # Build tokens & search index
            index = self.build_search_index(raw_text)
            logger.info(f"Index built successfully → words={index.get('total_words')}")

            # Document to write
            index_doc = {
                "indexed": True,
                "user_id ": user_id,
                "search_index": index,
            }

            # Firestore write ⬇⬇⬇ (the step that was likely failing silently)
            logger.info(f"Writing index to Firestore for {file_id}")
            self.firestore.update_file_index(file_id, user_id, index_doc)
            logger.info(f"✔ Firestore write complete for {file_id}")

            # Save cache for skip cases
            lock.store_result(index_doc)
            logger.info(f"Stored idempotency result for {file_id}")

            logger.info(f"Indexing COMPLETED for {file_id}")
            return index_doc
        
        except Exception as e:
            lock.release() # Release lock on failure
            logger.error(f"Index FAILED for {file_id}: {e}", exc_info=True)
            raise # 
