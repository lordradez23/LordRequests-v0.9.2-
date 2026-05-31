'''
Timezone/Locale Proxy-Sync.
Matches your browser's timezone and language settings to your proxy IP.
'''

import hrequests
from typing import Dict, Optional

class GeoSync:
    '''
    Finds where our proxy is and makes sure the browser matches that location.
    '''
    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy
        self.metadata: Dict[str, str] = {}

    def fetch_metadata(self) -> bool:
        '''
        Checks the proxy's IP info using ip-api.com.
        '''
        try:
            # We use ip-api.com because it's fast and gives us everything we need
            resp = hrequests.get("http://ip-api.com/json/", proxy=self.proxy, timeout=10)
            if resp.status_code == 200:
                self.metadata = resp.json()
                return self.metadata.get('status') == 'success'
        except Exception as e:
            print(f"[GeoSync] Couldn't grab IP metadata: {e}")
        return False

    def get_browser_config(self) -> Dict[str, any]:
        '''
        Builds a config dict we can just feed into the browser session.
        '''
        if not self.metadata:
            # If we haven't fetched it yet, do it now
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
        Sets the Accept-Language header based on where the proxy is located.
        '''
        if not self.metadata:
            self.fetch_metadata()
            
        lang = self.metadata.get('countryCode', 'US').lower()
        return {
            "Accept-Language": f"{lang},en-US;q=0.9,en;q=0.8"
        }
