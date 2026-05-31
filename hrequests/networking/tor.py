'''
Tor-Bridge Integration.
Lets you route all your traffic through the Tor network automatically.
'''

import hrequests
from typing import Optional

class TorBridge:
    def __init__(self, tor_proxy: str = 'socks5h://127.0.0.1:9050'):
        self.tor_proxy = tor_proxy

    def check_connection(self) -> bool:
        '''
        Verifies if the Tor proxy is reachable.
        '''
        try:
            resp = hrequests.get('https://check.torproject.org/', proxy=self.tor_proxy, timeout=10)
            return "Congratulations. This browser is configured to use Tor." in resp.text
        except:
            return False

    def get_session(self) -> hrequests.Session:
        '''
        Returns a session pre-configured to route through Tor.
        '''
        return hrequests.Session(proxy=self.tor_proxy)

    @staticmethod
    def get_tor_identity_reset_url() -> str:
        # Note: Resetting Tor identity usually requires communicating with 
        # the Tor Control Port (9051), not via HTTP.
        return "Tor identity reset requires ControlPort (9051) interaction."
