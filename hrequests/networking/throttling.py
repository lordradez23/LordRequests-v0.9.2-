'''
Traffic Throttling Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bandwidth limits and latency simulation per request to mimic different connection types.
'''

import time
import random
from typing import Dict, Tuple

class Throttler:
    '''
    Simulates different network connection speeds.
    '''
    PROFILES = {
        'dialup': {'latency': (200, 500), 'kbps': (56, 64)},
        'lte': {'latency': (20, 50), 'kbps': (10000, 50000)},
        'dsl': {'latency': (50, 100), 'kbps': (1000, 5000)},
        'fiber': {'latency': (1, 10), 'kbps': (100000, 1000000)}
    }

    def __init__(self, profile_name: str = 'lte'):
        self.profile = self.PROFILES.get(profile_name.lower(), self.PROFILES['lte'])

    def apply_latency(self):
        '''
        Simulates network latency.
        '''
        lat = random.uniform(*self.profile['latency'])
        time.sleep(lat / 1000.0)

    def throttle_data(self, data_size_bytes: int):
        '''
        Calculates and applies sleep to match the target kbps.
        '''
        target_kbps = random.uniform(*self.profile['kbps'])
        # (Size in bits) / (bits per second) = seconds
        seconds_required = (data_size_bytes * 8) / (target_kbps * 1000)
        
        if seconds_required > 0.01:
            time.sleep(seconds_required)

    @classmethod
    def wrap_request(cls, func, profile_name: str, *args, **kwargs):
        '''
        Wraps a request function with throttling logic.
        '''
        t = cls(profile_name)
        t.apply_latency()
        
        start = time.time()
        resp = func(*args, **kwargs)
        duration = time.time() - start
        
        # If the request was too fast for the profile, sleep more
        t.throttle_data(len(resp.content))
        
        return resp
