import time
from typing import Callable, Any

def retry(times: int = 3, delay: float = 1.0):
    """
    A simple retry decorator that retries a function X times.
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator
