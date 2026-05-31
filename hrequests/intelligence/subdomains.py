'''
Subdomain Discovery tool.
Finds all the hidden subdomains for a domain using both passive and active methods.
'''

import hrequests
import re
from typing import Set, List
from urllib.parse import urlparse

class SubdomainEnumerator:
    '''
    Crawls around to find any subdomains attached to a main domain.
    '''
    def __init__(self, domain: str):
        self.domain = self._clean_domain(domain)
        self.subdomains: Set[str] = set()

    def _clean_domain(self, domain: str) -> str:
        # Just pull the netloc if they gave us a full URL
        parsed = urlparse(domain)
        return parsed.netloc if parsed.netloc else domain

    def passive_scan(self) -> Set[str]:
        '''
        Checks certificate transparency logs (crt.sh) to find subdomains without touching the target.
        '''
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            resp = hrequests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    # crt.sh can return multiple names in one line or wildcards
                    for sub in name.split('\n'):
                        if '*' not in sub:
                            self.subdomains.add(sub.strip().lower())
        except Exception as e:
            print(f"[Subdomain] crt.sh lookup failed: {e}")
        
        return self.subdomains

    def active_brute_force(self, wordlist: List[str]) -> Set[str]:
        '''
        Tries to ping common subdomains (www, dev, api, etc) to see if they're alive.
        '''
        for word in wordlist:
            sub = f"{word}.{self.domain}"
            try:
                # Fast HEAD request just to see if it pings back
                resp = hrequests.head(f"http://{sub}", timeout=2)
                if resp.ok:
                    self.subdomains.add(sub)
            except Exception:
                # Page doesn't exist or timed out
                continue
        return self.subdomains

    def get_results(self) -> List[str]:
        '''Returns a clean sorted list of everything we found.'''
        return sorted(list(self.subdomains))
