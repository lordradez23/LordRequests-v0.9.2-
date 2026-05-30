'''
Sensitive Data Masking
~~~~~~~~~~~~~~~~~~~~~~

PII protection for harvested data (Emails, Credit Cards, SSNs).
'''

import re
from typing import Dict, List

class DataMasker:
    '''
    Redacts or masks sensitive patterns in text data.
    '''
    PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "credit_card": r'\b(?:\d[ -]*?){13,16}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "ipv4": r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    }

    @staticmethod
    def mask_text(text: str, replacement: str = "[REDACTED]") -> str:
        '''
        Replaces all sensitive patterns in a string with a mask.
        '''
        masked = text
        for name, pattern in DataMasker.PATTERNS.items():
            masked = re.sub(pattern, replacement, masked)
        return masked

    @staticmethod
    def mask_dict(data: Dict) -> Dict:
        '''
        Recursively masks sensitive strings within a dictionary.
        '''
        new_data = {}
        for k, v in data.items():
            if isinstance(v, str):
                new_data[k] = DataMasker.mask_text(v)
            elif isinstance(v, dict):
                new_data[k] = DataMasker.mask_dict(v)
            else:
                new_data[k] = v
        return new_data
