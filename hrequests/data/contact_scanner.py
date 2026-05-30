'''
Forensic Contact Scanner
~~~~~~~~~~~~~~~~~~~~~~~~

Extracts emails, phone numbers, and social media handles from page content.
'''

import re
import hrequests
from typing import Dict, Set

class ContactScanner:
    # Common RegEx patterns
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_PATTERN = r'\+?[\d\s\-\(\).]{7,20}'
    # Social handles (Twitter/X, IG, etc patterns often start with @ or are in URLs)
    SOCIAL_PATTERN = r'(?:twitter\.com|x\.com|instagram\.com|facebook\.com)/([a-zA-Z0-9._-]+)'

    def __init__(self, text: str):
        self.text = text

    def scan(self) -> Dict[str, Set[str]]:
        '''
        Scans the text for all contact patterns.
        '''
        results = {
            'emails': set(re.findall(self.EMAIL_PATTERN, self.text)),
            'phones': set(re.findall(self.PHONE_PATTERN, self.text)),
            'socials': set(re.findall(self.SOCIAL_PATTERN, self.text))
        }
        
        # Basic cleanup for phones (remove very short numbers)
        results['phones'] = {p.strip() for p in results['phones'] if len(re.sub(r'\D', '', p)) >= 10}
        
        return results

    @classmethod
    def scan_response(cls, response: hrequests.response.Response) -> Dict[str, Set[str]]:
        return cls(response.text).scan()
