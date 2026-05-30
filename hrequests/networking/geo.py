'''
Geo-Fenced Execution
~~~~~~~~~~~~~~~~~~~~

Regional proxy selection based on target CDN proximity.
'''

from typing import List, Dict, Optional
import hrequests

class GeoOptimizer:
    '''
    Selects the best proxy for a target based on geographic metadata.
    '''
    def __init__(self, proxy_list: List[str]):
        self.proxy_list = proxy_list
        # Simplified mapping of domains to regions
        self.region_map = {
            '.com': 'US',
            '.uk': 'EU',
            '.ng': 'AFR',
            '.cn': 'ASIA',
            '.de': 'EU'
        }

    def infer_region(self, url: str) -> str:
        '''
        Infers the target region from the URL TLD.
        '''
        for tld, region in self.region_map.items():
            if url.endswith(tld) or f"{tld}/" in url:
                return region
        return 'US' # Default

    def select_proxy(self, target_url: str) -> Optional[str]:
        '''
        Selects a proxy from the list that matches the target region.
        In this simplified version, it just picks one that contains the region code in the URL.
        '''
        region = self.infer_region(target_url)
        
        # Real implementation would use an IP-to-Geo database
        # For now, we search for region codes in the proxy URLs
        for proxy in self.proxy_list:
            if region.lower() in proxy.lower():
                return proxy
                
        return self.proxy_list[0] if self.proxy_list else None

    @staticmethod
    def get_public_ip(proxy: Optional[str] = None) -> str:
        '''
        Returns the public IP of the current session or proxy.
        '''
        try:
            resp = hrequests.get("https://api.ipify.org", proxy=proxy)
            return resp.text
        except Exception:
            return "Unknown"
