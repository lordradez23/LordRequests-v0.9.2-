'''
SSL Handshake Inspector
~~~~~~~~~~~~~~~~~~~~~~~

Performs a manual TLS handshake probe to extract detailed 
certificate and protocol information.
'''

import socket
import ssl
from typing import Dict, Optional

class TLSInspector:
    def __init__(self, host: str, port: int = 443):
        self.host = host
        self.port = port

    def inspect(self) -> Dict:
        '''
        Connects to the host and extracts TLS handshake details.
        '''
        context = ssl.create_default_context()
        try:
            with socket.create_connection((self.host, self.port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.host) as ssock:
                    cipher = ssock.cipher()
                    version = ssock.version()
                    cert = ssock.getpeercert()
                    
                    return {
                        'host': self.host,
                        'version': version,
                        'cipher': cipher[0],
                        'bits': cipher[2],
                        'certificate': cert
                    }
        except Exception as e:
            return {'error': str(e)}

    def get_summary(self, data: Dict) -> str:
        if 'error' in data:
            return f"TLS Inspection Error: {data['error']}"
            
        summary = f"TLS Handshake Report: {data['host']}\n"
        summary += "=" * 50 + "\n"
        summary += f"Protocol Version: {data['version']}\n"
        summary += f"Cipher Suite:     {data['cipher']}\n"
        summary += f"Key Strength:     {data['bits']} bits\n"
        
        subject = dict(x[0] for x in data['certificate'].get('subject', []))
        summary += f"Issued To:        {subject.get('commonName', 'Unknown')}\n"
        
        issuer = dict(x[0] for x in data['certificate'].get('issuer', []))
        summary += f"Issued By:        {issuer.get('commonName', 'Unknown')}\n"
        
        return summary
