'''
Screen/Window Resolution Sync
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensuring high-consistency between viewport and hardware screen reports
to defeat resolution-based fingerprinting.
'''

import random
from typing import Dict

class ScreenSync:
    '''
    Generates JS to spoof screen and window dimensions.
    '''
    RESOLUTIONS = [
        (1920, 1080), (1366, 768), (1440, 900), 
        (1536, 864), (2560, 1440), (1280, 720)
    ]

    @staticmethod
    def get_screen_script() -> str:
        '''
        Returns JS to spoof screen and window properties.
        '''
        width, height = random.choice(ScreenSync.RESOLUTIONS)
        avail_width = width
        avail_height = height - 40 # Account for taskbar/menubar
        
        return f"""
        (function() {{
            const screenProps = {{
                width: {width},
                height: {height},
                availWidth: {avail_width},
                availHeight: {avail_height},
                colorDepth: 24,
                pixelDepth: 24
            }};

            for (const [prop, value] of Object.entries(screenProps)) {{
                Object.defineProperty(screen, prop, {{
                    get: () => value
                }});
            }}

            window.innerWidth = {width};
            window.innerHeight = {avail_height};
            window.outerWidth = {width};
            window.outerHeight = {height};

            console.log("[LordRequests] Screen Resolution Synced: {width}x{height}");
        }})();
        """
