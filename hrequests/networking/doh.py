'''
DNS-over-HTTPS (DoH)
~~~~~~~~~~~~~~~~~~~

Provides client-side DoH resolution to bypass DNS-based censorship.
'''

import hrequests
from typing import List, Optional

class DoHHandler:
    PROVIDERS = {
        'cloudflare': 'https://cloudflare-dns.com/dns-query',
        'google': 'https://dns.google/dns-query',
        'quad9': 'https://dns.quad9.net/dns-query'
    }

    def __init__(self, provider: str = 'cloudflare'):
        self.endpoint = self.PROVIDERS.get(provider, provider)

    def resolve(self, domain: str, type: str = 'A') -> Optional[List[str]]:
        '''
        Resolves a domain using the selected DoH provider.
        '''
        params = {
            'name': domain,
            'type': type
        }
        headers = {'Accept': 'application/dns-json'}
        
        try:
            resp = hrequests.get(self.endpoint, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                answers = data.get('Answer', [])
                return [a.get('data') for a in answers if 'data' in a]
        except Exception as e:
            print(f"DoH Resolution failed for {domain}: {e}")
            
        return None
