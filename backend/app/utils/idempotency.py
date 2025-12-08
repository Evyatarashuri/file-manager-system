from functools import wraps
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse, Response 
from app.repositories.redis_cache import RedisCache
from app.schemas.Idempotency_response import IdempotencyResponse
from typing import Optional, Any

redis_cache = RedisCache()

def idempotent(func):
    """
    Decorator for enforcing idempotency on FastAPI routes using Redis.
    Requires the client to send an 'Idempotency-Key' header.
    """
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        # 1. Get Key from Header
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            # Idempotency is mandatory for this route
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Idempotency-Key header is required."
            )

        # 2. Check Cache
        existing_result: Optional[IdempotencyResponse] = redis_cache.check_or_set_idempotency_key(
            key=idempotency_key, 
            # Temporary value to indicate 'In Process'
            value=IdempotencyResponse(status_code=status.HTTP_202_ACCEPTED, body="Processing", headers={}) 
        )

        if existing_result:
            # 3. Key exists: Return stored result (Idempotent success) or Conflict (In Process)
            if existing_result.status_code == status.HTTP_202_ACCEPTED:
                 # Request is still processing (or failed to save final result)
                 raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Request is already processing."
                )
            
            # Return the previous successful result (Idempotent success)
            raise HTTPException(
                status_code=existing_result.status_code,
                detail=existing_result.body, # In a real app, you would reconstruct the response object
                headers=existing_result.headers
            )

        try:
            # 4. First Request: Execute the function
            response = await func(*args, request=request, **kwargs)
            
            # FIX: Handling the response object correctly.
            # If the route returns a Response object (like JSONResponse), we use its properties.
            # Otherwise, it's a dict/BaseModel, and we use it directly as the body.
            if isinstance(response, (JSONResponse, Response)) or hasattr(response, 'status_code'):
                # Response object (we need to read the body if it exists)
                final_body = await response.body() if hasattr(response, 'body') and response.body is not None else {}
                # The response object body often needs decoding, but we save the raw body first.
                status_code = response.status_code
                headers = dict(response.headers)
            else:
                # Dict or Pydantic BaseModel (The response object *is* the body)
                final_body = response 
                status_code = status.HTTP_201_CREATED # Assuming POST success
                headers = {}
            
            # 5. Store Success Result
            redis_cache.store_idempotency_result(
                key=idempotency_key,
                status_code=status_code,
                body=final_body,
                headers=headers
            )
            return response
        
        except Exception as e:
            # 6. Handle Failure - clean up the key or store failure status
            # For simplicity, let's delete the key on failure so client can retry
            redis_cache.client.delete(idempotency_key)
            raise e
            
    return wrapper