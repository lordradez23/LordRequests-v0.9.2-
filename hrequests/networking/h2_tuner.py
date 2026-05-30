'''
H2 Priority & Header Order Mapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides optimized HTTP/2 settings and header ordering for 
advanced stealth and performance.
'''

from typing import Dict, List, Optional

class H2Tuner:
    @staticmethod
    def get_stealth_pseudo_headers(browser: str = 'chrome') -> List[str]:
        '''
        Returns the standard pseudo-header order for specific browsers.
        Chrome/Edge: :method, :authority, :scheme, :path
        Firefox: :method, :path, :authority, :scheme
        '''
        browser = browser.lower()
        if 'firefox' in browser:
            return [":method", ":path", ":authority", ":scheme"]
        return [":method", ":authority", ":scheme", ":path"]

    @staticmethod
    def get_h2_settings_preset(browser: str = 'chrome') -> Dict[str, int]:
        '''
        Returns a high-stealth H2 settings map for the Go engine.
        '''
        if 'firefox' in browser.lower():
            return {
                "HEADER_TABLE_SIZE": 65536,
                "MAX_CONCURRENT_STREAMS": 100,
                "INITIAL_WINDOW_SIZE": 131072,
                "MAX_FRAME_SIZE": 16384,
                "MAX_HEADER_LIST_SIZE": 262144
            }
        
        # Chrome default high-stealth
        return {
            "HEADER_TABLE_SIZE": 65536,
            "MAX_CONCURRENT_STREAMS": 1000,
            "INITIAL_WINDOW_SIZE": 6291456,
            "MAX_HEADER_LIST_SIZE": 262144
        }
