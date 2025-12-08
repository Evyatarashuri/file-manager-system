from pydantic import BaseModel
from typing import Any, Dict, Optional
import json


class IdempotencyResponse(BaseModel):
    status_code: int
    body: Any
    headers: Dict[str, str] = {}

    def to_json(self) -> str:
        return json.dumps({
            "status_code": self.status_code,
            "body": self.body,
            "headers": self.headers
        })

    @classmethod
    def from_json(cls, data: str) -> Optional["IdempotencyResponse"]:
        if not data:
            return None
        obj = json.loads(data)
        return cls(
            status_code=obj.get("status_code"),
            body=obj.get("body"),
            headers=obj.get("headers", {})
        )
