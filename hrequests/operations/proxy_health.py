'''
Proxy Auto-Healer
~~~~~~~~~~~~~~~~~

Continuously monitors the health of proxies and automatically purges or 
replaces non-functional or blacklisted IPs.
'''

import hrequests
import threading
import time
from typing import List, Optional

class ProxyAutoHealer:
    def __init__(self, proxy_list: List[str], test_url: str = 'https://httpbin.org/ip'):
        self.proxies = proxy_list
        self.test_url = test_url
        self.active_proxies = proxy_list.copy()
        self.is_running = False
        self._thread = None

    def probe_proxy(self, proxy: str) -> bool:
        '''
        Tests a single proxy for connectivity and speed.
        '''
        try:
            resp = hrequests.get(self.test_url, proxy=proxy, timeout=5)
            return resp.status_code == 200
        except:
            return False

    def heal(self):
        '''
        Iterates through the proxy list and removes failing ones.
        '''
        healed_list = []
        for proxy in self.proxies:
            if self.probe_proxy(proxy):
                healed_list.append(proxy)
            else:
                print(f"Purging dead proxy: {proxy}")
        
        self.active_proxies = healed_list
        print(f"Heal complete. {len(self.active_proxies)}/{len(self.proxies)} proxies active.")

    def start_monitoring(self, interval: int = 300):
        '''
        Starts a background thread to heal proxies at regular intervals.
        '''
        self.is_running = True
        def monitor():
            while self.is_running:
                self.heal()
                time.sleep(interval)
        
        self._thread = threading.Thread(target=monitor, daemon=True)
        self._thread.start()
        print("Proxy monitoring started in background.")

    def stop_monitoring(self):
        self.is_running = False
        if self._thread:
            self._thread.join()
