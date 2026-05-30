'''
Proxy Kill-Switch
~~~~~~~~~~~~~~~~~

Monitors proxy connectivity and immediately halts traffic if the 
proxy connection is lost, preventing IP leaks.
'''

import hrequests
from typing import Optional

class ProxyKillSwitch:
    def __init__(self, session: hrequests.Session):
        self.session = session
        self.proxy = session.proxy

    def verify_and_request(self, method: str, url: str, **kwargs) -> Optional[hrequests.response.Response]:
        '''
        Checks if the proxy is still active before performing the request.
        '''
        if not self.proxy:
            raise ValueError("Kill-Switch requires a session with an active proxy.")
            
        # Perform a lightweight ping through the proxy
        try:
            # We use a very low timeout for the check
            hrequests.get('https://httpbin.org/ip', proxy=self.proxy, timeout=3)
        except Exception:
            print(f"!!! KILL-SWITCH TRIGGERED: Proxy {self.proxy} is offline. Halting traffic.")
            return None
            
        return self.session.request(method=method, url=url, **kwargs)
