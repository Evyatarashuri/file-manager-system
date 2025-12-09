import json
from app.config.redis import get_redis_client

class IdempotencyKey:
    """Redis-based Idempotency Key for safe, exactly-once processing."""
    def __init__(self, key: str, ttl: int = 300):
        self.key = f"idempotency:{key}"
        self.ttl = ttl
        self.client = get_redis_client()

    def acquire(self) -> bool:
        """Reserve execution — prevents workers from processing same file twice."""
        return bool(self.client.set(self.key, "processing", nx=True, ex=self.ttl))

    def release(self):
        """Remove key manually (used if processing fails)."""
        self.client.delete(self.key)

    def store_result(self, data: dict):
        """Store final indexing result or metadata output."""
        payload = json.dumps(data)
        self.client.set(self.key, payload, ex=self.ttl)

    def get_result(self) -> dict | None:
        """Returns previous result if exists (Idempotent replay)."""
        value = self.client.get(self.key)
        return json.loads(value) if value else None
