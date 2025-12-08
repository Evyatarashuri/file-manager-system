import time
import functools

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_time: int = 30  # seconds to half-open
    ):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"    # CLOSED → OPEN → HALF_OPEN

    def allow_request(self) -> bool:
        if self.state == "OPEN":
            if (time.time() - self.last_failure_time) >= self.recovery_time:
                self.state = "HALF_OPEN"
                return True
            return False

        return True

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()

        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            print("Circuit Breaker OPEN — service temporarily blocked")

def circuit_breaker(cb: CircuitBreaker):
    """ Decorator to wrap functions with circuit breaker protection """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):

            if not cb.allow_request():
                raise RuntimeError("⚠ CircuitBreaker BLOCKED request")

            try:
                result = func(*args, **kwargs)
                cb.record_success()
                return result

            except Exception as e:
                cb.record_failure()
                raise

        return inner
    return wrapper
