from uuid import uuid4
from app.config.redis import get_redis_client

class RedisLock:
    def __init__(self, key: str, ttl: int = 60):
        self.client = get_redis_client()
        self.key = f"lock:{key}"
        self.ttl = ttl
        self.token = str(uuid4())  # this lock instance owns the lock

    def acquire(self) -> bool:
        return bool(self.client.set(self.key, self.token, ex=self.ttl, nx=True))

    def refresh(self) -> bool:
        return bool(self.client.expire(self.key, self.ttl))

    def release(self):
        # only remove lock if owner matches token
        value = self.client.get(self.key)
        if value and value == self.token:
            self.client.delete(self.key)
