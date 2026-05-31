'''
Deep-Web Health Monitor
~~~~~~~~~~~~~~~~~~~~~~~

Specialized health checking for .onion (Tor) and .i2p (I2P) hidden services.
'''

import hrequests
from typing import Dict, List, Optional
import time

class DeepWebMonitor:
    '''
    Monitors availability and latency of hidden services.
    Requires a proxy configured for .onion/.i2p (e.g. Tor or I2P daemon).
    '''
    def __init__(self, proxy: str):
        self.proxy = proxy

    def check_service(self, url: str) -> Dict[str, any]:
        '''
        Checks if a hidden service is reachable and measures latency.
        '''
        start = time.time()
        status = "offline"
        latency = -1
        error = None
        
        try:
            # Onion sites are often slow, use a generous timeout
            resp = hrequests.get(url, proxy=self.proxy, timeout=30)
            latency = (time.time() - start) * 1000 # ms
            if resp.status_code == 200:
                status = "online"
            else:
                status = f"error_{resp.status_code}"
        except Exception as e:
            error = str(e)
            
        return {
            "url": url,
            "status": status,
            "latency_ms": round(latency, 2) if latency > 0 else -1,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "error": error
        }

    def batch_check(self, urls: List[str]) -> List[Dict]:
        return [self.check_service(u) for u in urls]
