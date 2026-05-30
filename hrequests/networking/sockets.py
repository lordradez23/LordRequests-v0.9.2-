'''
TCP/UDP Socket Proxying
~~~~~~~~~~~~~~~~~~~~~~

Provides low-level socket communication through SOCKS proxies.
'''

import socket
from typing import Optional, Tuple
from urllib.parse import urlparse

try:
    import socks
    PY_SOCKS_AVAILABLE = True
except ImportError:
    PY_SOCKS_AVAILABLE = False

class SocketBridge:
    '''
    A bridge for creating low-level TCP/UDP connections through proxies.
    '''
    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.proxy_type, self.proxy_addr, self.proxy_port, self.proxy_rdns, self.username, self.password = self._parse_proxy(proxy_url)

    def _parse_proxy(self, url: Optional[str]) -> Tuple:
        if not url:
            return None, None, None, None, None, None
        
        parsed = urlparse(url)
        scheme = parsed.scheme.lower()
        
        if 'socks5' in scheme:
            proxy_type = socks.SOCKS5 if PY_SOCKS_AVAILABLE else 3
        elif 'socks4' in scheme:
            proxy_type = socks.SOCKS4 if PY_SOCKS_AVAILABLE else 2
        elif 'http' in scheme:
            proxy_type = socks.HTTP if PY_SOCKS_AVAILABLE else 1
        else:
            return None, None, None, None, None, None

        return (
            proxy_type,
            parsed.hostname,
            parsed.port,
            True,
            parsed.username,
            parsed.password
        )

    def create_connection(self, dest_host: str, dest_port: int, timeout: int = 10) -> socket.socket:
        '''
        Creates a TCP connection, optionally through a proxy.
        '''
        if not self.proxy_url or not PY_SOCKS_AVAILABLE:
            if self.proxy_url and not PY_SOCKS_AVAILABLE:
                print("Warning: PySocks is not installed. Falling back to direct connection.")
            return socket.create_connection((dest_host, dest_port), timeout=timeout)
            
        s = socks.socksocket()
        s.set_proxy(
            proxy_type=self.proxy_type,
            addr=self.proxy_addr,
            port=self.proxy_port,
            rdns=self.proxy_rdns,
            username=self.username,
            password=self.password
        )
        s.settimeout(timeout)
        s.connect((dest_host, dest_port))
        return s

    def create_udp_socket(self) -> socket.socket:
        '''
        Creates a UDP socket, optionally through a SOCKS5 proxy.
        Note: UDP proxying is only supported by SOCKS5.
        '''
        if not self.proxy_url or not PY_SOCKS_AVAILABLE or self.proxy_type != socks.SOCKS5:
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
        s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
        s.set_proxy(
            proxy_type=self.proxy_type,
            addr=self.proxy_addr,
            port=self.proxy_port,
            rdns=self.proxy_rdns,
            username=self.username,
            password=self.password
        )
        return s
