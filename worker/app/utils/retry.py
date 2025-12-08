import time
import functools
import random

def retry(
    retries: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 10,
    jitter: bool = True,
):
    """
    Retry decorator with backoff + jitter for stability in worker processing.
    Used for Firestore, Storage, Pub/Sub publishing + transient errors.
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            delay = base_delay

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    if attempt == retries:
                        raise

                    sleep_time = delay + (random.uniform(0, delay) if jitter else 0)
                    sleep_time = min(sleep_time, max_delay)

                    print(f"⚠ {func.__name__} failed (attempt {attempt}/{retries}). "
                          f"Retrying in {sleep_time:.2f}s | error: {e}")

                    time.sleep(sleep_time)
                    delay *= 2  # exponential

        return inner
    return wrapper
