'''
UA-Fingerprint Sync
~~~~~~~~~~~~~~~~~~~

Ensures that the User-Agent and TLS fingerprints are technically 
consistent to avoid detection.
'''

import re

class FingerprintSync:
    @staticmethod
    def validate(user_agent: str, tls_identifier: str) -> bool:
        '''
        Checks if the browser name in the UA matches the TLS identifier.
        '''
        ua_lower = user_agent.lower()
        tls_lower = tls_identifier.lower()
        
        # Extract browser from UA using regex
        browser_match = re.search(r'(firefox|chrome|safari|opera|edge)', ua_lower)
        if not browser_match:
            return True # Unknown UA, skip validation
            
        browser = browser_match.group(1)
        
        # Standardize Edge/Chrome (Edge usually identifies as Chrome too)
        if browser == 'edge' and 'chrome' in tls_lower:
            return True
        
        return browser in tls_lower

    @staticmethod
    def get_consistent_ua(tls_identifier: str) -> str:
        '''
        Returns a fallback mock user agent if the current one is inconsistent.
        '''
        if 'firefox' in tls_identifier.lower():
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0"
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
