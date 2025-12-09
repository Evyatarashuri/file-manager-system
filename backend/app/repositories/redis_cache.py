import json
from redis import Redis
from typing import Optional, Any
from app.config.redis import get_redis_client
from app.schemas.Idempotency_response import IdempotencyResponse

IDEMPOTENCY_TTL_SECONDS = 3600     # 1 hour cache

class RedisCache:
    def __init__(self):
        self.client: Redis = get_redis_client()

    # -----------------------------
    # MAIN FUNCTION — This is the one that failed before
    # -----------------------------
    def check_or_set_idempotency_key(self, key: str, value: IdempotencyResponse) -> Optional[IdempotencyResponse]:
        serialized = json.dumps(value.model_dump()) # Serialize to JSON string to store in Redis (Mandatory)

        # SETNX = set only if not exists (atomic)
        was_set = self.client.set(key, serialized, ex=IDEMPOTENCY_TTL_SECONDS, nx=True)

        if was_set:
            return None  # first request — allow execution

        # Key already exists -> return stored response
        raw = self.client.get(key)
        return IdempotencyResponse(**json.loads(raw)) if raw else None


    # -----------------------------
    # Store final successful result
    # -----------------------------
    def store_idempotency_result(self, key: str, status_code: int, body: Any, headers: dict):
        response = IdempotencyResponse(status_code=status_code, body=body, headers=headers)
        serialized = json.dumps(response.model_dump())
        self.client.set(key, serialized, ex=IDEMPOTENCY_TTL_SECONDS)


    # -----------------------------
    # Optional: Clear
    # -----------------------------
    def delete(self, key: str):
        self.client.delete(key)
