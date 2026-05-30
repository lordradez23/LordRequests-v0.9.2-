'''
Vulnerability Scanning Sidecar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Passive security scanning for target site compliance and vulnerabilities.
'''

from typing import Dict, List
import hrequests

class VulnScanner:
    '''
    Analyzes responses for common security misconfigurations and vulnerabilities.
    '''
    def __init__(self):
        self.security_headers = [
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'Referrer-Policy'
        ]

    def scan_headers(self, response: hrequests.Response) -> Dict[str, Any]:
        '''
        Checks for missing or misconfigured security headers.
        '''
        results = {
            "vulnerabilities": [],
            "missing_headers": [],
            "status": "SECURE"
        }
        
        for header in self.security_headers:
            if header not in response.headers:
                results["missing_headers"].append(header)
                
        # Check for server leakage
        server = response.headers.get('Server')
        if server:
            results["vulnerabilities"].append(f"Server header disclosure: {server}")
            
        if results["missing_headers"] or results["vulnerabilities"]:
            results["status"] = "EXPOSED"
            
        return results

    def passive_body_scan(self, text: str) -> List[str]:
        '''
        Scans response body for sensitive patterns (e.g. API keys, internal IPs).
        '''
        findings = []
        # Placeholder for regex checks
        if "eval(" in text:
            findings.append("Potential Unsafe JS Execution (eval)")
        return findings
