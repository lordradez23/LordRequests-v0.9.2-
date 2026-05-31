'''
Timezone/Locale Proxy-Sync
~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatically aligns browser context (Timezone, Locale, Geolocation)
with the proxy IP address to maintain identity consistency.
'''

import hrequests
from typing import Dict, Optional

class GeoSync:
    '''
    Detects geo-metadata from a proxy and generates browser configuration.
    '''
    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy
        self.metadata: Dict[str, str] = {}

    def fetch_metadata(self) -> bool:
        '''
        Fetches geolocation metadata from the proxy IP.
        '''
        try:
            # Use ip-api.com (JSON) for speed and detail
            resp = hrequests.get("http://ip-api.com/json/", proxy=self.proxy, timeout=10)
            if resp.status_code == 200:
                self.metadata = resp.json()
                return self.metadata.get('status') == 'success'
        except Exception as e:
            print(f"[GeoSync] Failed to fetch metadata: {e}")
        return False

    def get_browser_config(self) -> Dict[str, any]:
        '''
        Generates a dictionary compatible with BrowserSession/Playwright configuration.
        '''
        if not self.metadata:
            if not self.fetch_metadata():
                return {}

        return {
            "timezone_id": self.metadata.get('timezone', 'UTC'),
            "locale": self.metadata.get('countryCode', 'en-US').lower(),
            "geolocation": {
                "latitude": float(self.metadata.get('lat', 0)),
                "longitude": float(self.metadata.get('lon', 0)),
                "accuracy": 100
            },
            "permissions": ["geolocation"]
        }

    def get_headers(self) -> Dict[str, str]:
        '''
        Generates Accept-Language headers based on the proxy location.
        '''
        if not self.metadata:
            self.fetch_metadata()
            
        lang = self.metadata.get('countryCode', 'US').lower()
        return {
            "Accept-Language": f"{lang},en-US;q=0.9,en;q=0.8"
        }
