import time, random, functools, logging

log = logging.getLogger("backoff")

def backoff(
    max_retries=5,
    base_delay=0.25,
    max_delay=8,
    jitter=True,
    retry_exceptions=(Exception,)  # only retry specific errors
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except retry_exceptions as e:
                    if attempt == max_retries:
                        log.error(f"{func.__name__} failed after {attempt} attempts", exc_info=e)
                        raise

                    sleep = delay + (random.random()*delay if jitter else 0)
                    sleep = min(sleep, max_delay)

                    log.warning(
                        f"{func.__name__} failed attempt={attempt}/{max_retries} "
                        f"retrying in {sleep:.2f}s"
                    )

                    time.sleep(sleep)
                    delay *= 2

        return wrapper
    return decorator
