'''
Request Rate Limiter
~~~~~~~~~~~~~~~~~~~~

Provides fine-grained control over request frequency to avoid 
rate-limiting by target servers.
'''

import time
from threading import Lock

class RateLimiter:
    def __init__(self, requests_per_second: float):
        self.interval = 1.0 / requests_per_second
        self.last_request_time = 0
        self._lock = Lock()

    def wait(self):
        '''
        Waits until the next request is allowed according to the rate.
        '''
        with self._lock:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)
            self.last_request_time = time.time()
