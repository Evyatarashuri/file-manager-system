import time

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_time: float = 10.0
    ):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = 0

    def call(self, func, *args, **kwargs):
        # If open → block execution
        if self.state == "OPEN":
            if time.time() - self.last_failure_time < self.recovery_time:
                raise Exception("CircuitBreaker is OPEN")

            # Try again after cooldown
            self.state = "HALF_OPEN"

        try:
            result = func(*args, **kwargs)

            # Success resets the breaker
            self.failure_count = 0
            self.state = "CLOSED"
            return result

        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise
