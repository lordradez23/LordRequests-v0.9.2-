'''
SSRF Protection Layer
~~~~~~~~~~~~~~~~~~~~~

Prevention of Server-Side Request Forgery during automated harvesting.
'''

import ipaddress
import socket
from urllib.parse import urlparse
from typing import List, Optional

class SSRFGuard:
    '''
    Validates target URLs to prevent internal resource leakage.
    '''
    INTERNAL_RANGES = [
        '127.0.0.0/8',
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16',
        '169.254.169.254/32', # AWS/Cloud Metadata
        '::1/128'
    ]

    def __init__(self, blocked_ranges: Optional[List[str]] = None):
        self.blocked = [ipaddress.ip_network(r) for r in (blocked_ranges or self.INTERNAL_RANGES)]

    def is_safe(self, url: str) -> bool:
        '''
        Checks if the URL resolves to a public, non-internal IP.
        '''
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            if not hostname: return False
            
            # Resolve IP
            ip = socket.gethostbyname(hostname)
            addr = ipaddress.ip_address(ip)
            
            for network in self.blocked:
                if addr in network:
                    return False
            return True
        except (socket.gaierror, ValueError):
            return False
