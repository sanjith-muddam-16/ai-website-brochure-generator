import time
from threading import Lock

class RateLimiter:
    def __init__(self, min_interval_seconds: float):
        self.min_interval = min_interval_seconds
        self.lock = Lock()
        self.last_call = 0.0

    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call = time.time()
