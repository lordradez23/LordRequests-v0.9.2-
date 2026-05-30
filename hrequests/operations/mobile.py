'''
Mobile Identity Spoofer
~~~~~~~~~~~~~~~~~~~~~~~

Coordinated Android/iOS identity simulation for high-fidelity mobile scraping.
'''

import random
from typing import Dict

class MobileSpoofer:
    '''
    Generates coordinated mobile headers and environment signals.
    '''
    ANDROID_UA = "Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/UD1A.230805.019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.66 Mobile Safari/537.36"
    IOS_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"

    @staticmethod
    def get_mobile_headers(platform: str = 'android') -> Dict[str, str]:
        '''
        Returns a set of consistent mobile request headers.
        '''
        if platform.lower() == 'ios':
            return {
                "User-Agent": MobileSpoofer.IOS_UA,
                "Accept-Language": "en-US,en;q=0.9",
                "X-Requested-With": "com.apple.mobilesafari"
            }
        
        return {
            "User-Agent": MobileSpoofer.ANDROID_UA,
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "com.android.chrome",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"'
        }

    @staticmethod
    def get_touch_bypass_script() -> str:
        '''
        Injects JS to simulate touch support in a non-touch environment.
        '''
        return """
        (function() {
            window.ontouchstart = null;
            navigator.maxTouchPoints = 5;
        })();
        """
