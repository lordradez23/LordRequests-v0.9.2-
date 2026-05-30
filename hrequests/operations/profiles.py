'''
Legendary Profile Library
~~~~~~~~~~~~~~~~~~~~~~~~~

A library of pre-compiled, high-trust JA3 and HTTP/2 fingerprints
optimized for stealth operations.
'''

from typing import Dict, List, Optional

class LegendaryProfiles:
    # High-trust profiles modeled after legitimate browsers
    PROFILES = {
        'iphone_15_safari': {
            'ja3String': '771,4865-4866-4867,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0',
            'h2Settings': {
                'HEADER_TABLE_SIZE': 65536,
                'MAX_CONCURRENT_STREAMS': 1000,
                'INITIAL_WINDOW_SIZE': 6291456,
                'MAX_HEADER_LIST_SIZE': 262144
            },
            'pseudoHeaderOrder': [":method", ":authority", ":scheme", ":path"]
        },
        'win11_edge_pro': {
            'ja3String': '771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0',
            'h2Settings': {
                 "INITIAL_WINDOW_SIZE": 6291456,
                 "MAX_HEADER_LIST_SIZE": 262144
            },
            'pseudoHeaderOrder': [":method", ":path", ":authority", ":scheme"]
        },
        'linux_firefox_stable': {
            'ja3String': '771,4865-4866-4867,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0',
             'h2Settings': {
                'HEADER_TABLE_SIZE': 65536,
                'MAX_CONCURRENT_STREAMS': 100
            },
            'pseudoHeaderOrder': [":method", ":authority", ":scheme", ":path"]
        }
    }

    @classmethod
    def get(cls, name: str) -> Optional[Dict]:
        return cls.PROFILES.get(name)

    @classmethod
    def list_available(cls) -> List[str]:
        return list(cls.PROFILES.keys())
