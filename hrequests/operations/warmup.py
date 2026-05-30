'''
Account Warm-Up Engine
~~~~~~~~~~~~~~~~~~~~~~

Automated simulation of human browsing to build cookie trust and session longevity.
'''

import time
import random
from typing import List, Optional
import hrequests

class WarmupEngine:
    '''
    Executes a series of 'safe' requests to establish a natural-looking session.
    '''
    def __init__(self, targets: Optional[List[str]] = None):
        self.targets = targets or [
            "https://www.google.com",
            "https://www.wikipedia.org",
            "https://www.bing.com",
            "https://www.reddit.com"
        ]

    def execute_warmup(self, session: hrequests.Session, intensity: int = 5):
        '''
        Performs a sequence of natural-looking requests.
        '''
        print(f"Starting Account Warm-up (Intensity: {intensity})...")
        
        # Pick random subset of targets
        selected = random.sample(self.targets, min(len(self.targets), intensity))
        
        for url in selected:
            print(f"  Browsing {url}...")
            try:
                session.get(url)
                # Random human-like pause
                time.sleep(random.uniform(2, 7))
            except Exception as e:
                print(f"  Warm-up error at {url}: {e}")
        
        print("Warm-up sequence complete.")
