'''
Navigator Property Hider
~~~~~~~~~~~~~~~~~~~~~~~

Masking of sensitive navigator properties (webdriver, languages, hardwareConcurrency)
to defeat browser-based bot detection.
'''

import random
from typing import Dict, Optional

class NavigatorHider:
    '''
    Generates JS to mask navigator properties that reveal automation or hardware details.
    '''
    @staticmethod
    def get_navigator_script(os_type: str = 'win') -> str:
        '''
        Returns JS to mask navigator properties.
        '''
        concurrency = random.choice([2, 4, 8, 12, 16])
        memory = random.choice([4, 8, 16, 32])
        platform = {
            'win': 'Win32',
            'mac': 'MacIntel',
            'lin': 'Linux x86_64'
        }.get(os_type, 'Win32')

        return f"""
        (function() {{
            const mask = {{
                webdriver: false,
                hardwareConcurrency: {concurrency},
                deviceMemory: {memory},
                platform: '{platform}',
                languages: ['en-US', 'en'],
                plugins: []
            }};

            for (const [prop, value] of Object.entries(mask)) {{
                Object.defineProperty(navigator, prop, {{
                    get: () => value
                }});
            }}

            // Mask Chrome-specific runtime if present
            if (window.chrome) {{
                window.chrome.runtime = undefined;
            }}

            console.log("[LordRequests] Navigator Properties Masked ({os_type}).");
        }})();
        """
