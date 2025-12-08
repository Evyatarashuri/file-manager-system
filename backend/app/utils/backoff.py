import time
import random

def exponential_backoff(retries: int = 3, base_delay: float = 0.5, jitter: float = 0.1):
    """
    Generator that yields exponential delays with jitter.
    """
    for attempt in range(retries):
        delay = base_delay * (2 ** attempt)
        delay += random.uniform(0, jitter)
        yield delay
