'''
Subdomain Discovery Sidecar
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Passive and active subdomain enumeration to map target infrastructure.
'''

import hrequests
import re
from typing import Set, List
from urllib.parse import urlparse

class SubdomainEnumerator:
    '''
    Enumerates subdomains for a given root domain.
    '''
    def __init__(self, domain: str):
        self.domain = self._clean_domain(domain)
        self.subdomains: Set[str] = set()

    def _clean_domain(self, domain: str) -> str:
        parsed = urlparse(domain)
        return parsed.netloc if parsed.netloc else domain

    def passive_scan(self) -> Set[str]:
        '''
        Passive enumeration via search engine scraping and certificate transparency logs.
        (Simplified implementation for CTR logs via crt.sh)
        '''
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            resp = hrequests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    # names can be multiple lines or contain wildcards
                    for sub in name.split('\n'):
                        if '*' not in sub:
                            self.subdomains.add(sub.strip().lower())
        except Exception as e:
            print(f"[Subdomain] Passive scan failed: {e}")
        
        return self.subdomains

    def active_brute_force(self, wordlist: List[str]) -> Set[str]:
        '''
        Active enumeration via DNS/HTTP probing.
        '''
        for word in wordlist:
            sub = f"{word}.{self.domain}"
            try:
                # Probe via HTTP HEAD to verify existence
                resp = hrequests.head(f"http://{sub}", timeout=2)
                if resp.ok:
                    self.subdomains.add(sub)
            except Exception:
                continue
        return self.subdomains

    def get_results(self) -> List[str]:
        return sorted(list(self.subdomains))
