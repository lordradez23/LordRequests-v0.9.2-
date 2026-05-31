'''
Advanced Rate-Limit Backoff
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Intelligent exponential backoff with jitter for rate-limited responses.
'''

import time
import random
from typing import Callable, Any, TypeVar

T = TypeVar('T')

class RateLimitBackoff:
    '''
    Implements exponential backoff with jitter for 429/503 responses.
    '''
    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0, max_retries: int = 5):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries

    def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        '''
        Executes a function with automatic retry on rate-limit errors.
        '''
        for attempt in range(self.max_retries):
            result = func(*args, **kwargs)
            
            # Check if response indicates rate limiting
            status = getattr(result, 'status_code', 200)
            if status in (429, 503):
                delay = self._calculate_delay(attempt)
                print(f"Rate limited (attempt {attempt + 1}). Waiting {delay:.2f}s...")
                time.sleep(delay)
                continue
                
            return result
            
        print("Max retries reached. Returning last response.")
        return result

    def _calculate_delay(self, attempt: int) -> float:
        '''
        Calculates exponential backoff with full jitter.
        '''
        base = min(self.max_delay, self.base_delay * (2 ** attempt))
        return random.uniform(0, base)  # Full jitter
