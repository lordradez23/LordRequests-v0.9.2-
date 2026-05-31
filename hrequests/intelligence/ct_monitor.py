'''
Certificate Transparency Monitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitors CT logs for newly issued certs on target domains.
'''

import hrequests
from typing import List, Dict, Any

class CTMonitor:
    '''
    Query Certificate Transparency logs to detect new SSL certs.
    '''
    CT_API = "https://crt.sh/?q={domain}&output=json"

    def fetch_certs(self, domain: str) -> List[Dict[str, Any]]:
        '''
        Fetches all known certificates for a domain from crt.sh.
        '''
        url = self.CT_API.format(domain=domain)
        print(f"Querying CT logs for: {domain}...")
        try:
            resp = hrequests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"CT fetch error: {e}")
        return []

    def get_subdomains(self, domain: str) -> List[str]:
        '''
        Extracts unique subdomains from CT log entries.
        '''
        certs = self.fetch_certs(domain)
        subdomains = set()
        for cert in certs:
            name = cert.get('name_value', '')
            for sub in name.split('\n'):
                if sub.startswith('*.'):
                    sub = sub[2:]
                subdomains.add(sub.strip())
        return sorted(subdomains)

    def detect_new_certs(self, domain: str, known_count: int) -> bool:
        '''
        Returns True if new certs have been issued since last check.
        '''
        current = self.fetch_certs(domain)
        return len(current) > known_count
