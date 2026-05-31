'''
WAF-Specific Header Tuner
~~~~~~~~~~~~~~~~~~~~~~~~~

Presets for bypassing specific Web Application Firewalls (Cloudflare, Akamai, Imperva).
'''

from typing import Dict

class WAFTuner:
    '''
    Provides header and TLS presets for specific WAF bypass scenarios.
    '''
    PRESETS = {
        'cloudflare': {
            'headers': {
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9'
            },
            'force_http1': False
        },
        'akamai': {
            'headers': {
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            },
            'pseudoHeaderOrder': [":method", ":scheme", ":path", ":authority"]
        }
    }

    @classmethod
    def get_preset(cls, name: str) -> Dict:
        return cls.PRESETS.get(name.lower(), {})

    @classmethod
    def apply_to_session(cls, session, waf_name: str):
        '''
        Applies a WAF preset to an hrequests Session.
        '''
        preset = cls.get_preset(waf_name)
        if not preset:
            return
            
        if 'headers' in preset:
            session.headers.update(preset['headers'])
        if 'force_http1' in preset:
            session.force_http1 = preset['force_http1']
        if 'pseudoHeaderOrder' in preset:
            session.pseudo_header_order = preset['pseudoHeaderOrder']
