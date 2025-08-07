import time
import requests
from functools import wraps

class RateLimiter:
    def __init__(self, max_requests=60, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    def can_make_request(self):
        now = time.time()
        self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        return len(self.requests) < self.max_requests

    def record_request(self):
        self.requests.append(time.time())

def exponential_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 403 and 'rate limit' in e.response.text.lower():
                        delay = base_delay * (2 ** attempt)
                        print(f"Rate limited. Waiting {delay} seconds...")
                        time.sleep(delay)
                    else:
                        raise
            raise Exception(f"Failed after {max_retries} attempts")
        return wrapper
    return decorator
