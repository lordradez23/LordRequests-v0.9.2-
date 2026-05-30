'''
Traffic Shape-Shifting
~~~~~~~~~~~~~~~~~~~~~~

Dynamic alteration of request characteristics to defeat traffic analysis.
'''

import random
import time
from typing import Dict, Optional

class TrafficShaper:
    '''
    Alters the timing and size patterns of outbound requests.
    '''
    def __init__(self, jitter_ms: int = 500):
        self.jitter_ms = jitter_ms

    def inject_jitter(self):
        '''
        Adds a randomized human-like delay before the next request.
        '''
        delay = random.uniform(0.1, self.jitter_ms / 1000.0)
        time.sleep(delay)

    @staticmethod
    def pad_payload(payload: str, target_size: int = 1024) -> str:
        '''
        Pads a payload with whitespace to normalize packet sizes.
        '''
        if len(payload) >= target_size:
            return payload
        return payload + " " * (target_size - len(payload))

    @staticmethod
    def vary_accept_headers() -> Dict[str, str]:
        '''
        Returns varied Accept headers to avoid pattern matching.
        '''
        accepts = [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "text/html,*/*;q=0.9",
        ]
        return {"Accept": random.choice(accepts)}
