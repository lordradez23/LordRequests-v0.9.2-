'''
Honey-Token Detector
~~~~~~~~~~~~~~~~~~~~

Detection of honeypot links and tracking tokens in scraped content.
'''

import re
from typing import List, Dict

class HoneyTokenDetector:
    '''
    Scans responses for honeypot traps and canary tokens.
    '''
    HONEYPOT_SIGNATURES = [
        r'<a[^>]+style\s*=\s*"[^"]*display\s*:\s*none[^"]*"',   # Hidden links
        r'<input[^>]+type\s*=\s*"hidden"[^>]+name\s*=\s*"(?:honeypot|hp|bot_check)',  # Hidden fields
        r'https?://[^\s"]+canarytokens\.org',  # Canarytokens
        r'https?://[^\s"]+appear\.in/[a-z0-9]{8}',  # Appear.in canary
    ]

    def scan(self, html: str) -> Dict[str, List[str]]:
        '''
        Scans HTML for honeytrap patterns.
        '''
        findings = {}
        for sig in self.HONEYPOT_SIGNATURES:
            matches = re.findall(sig, html, re.IGNORECASE)
            if matches:
                findings[sig[:40]] = matches
        return findings

    def is_clean(self, html: str) -> bool:
        '''Returns True if no honeypot signals are detected.'''
        return len(self.scan(html)) == 0
