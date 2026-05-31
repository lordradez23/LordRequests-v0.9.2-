'''
Font Fingerprint Randomizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Discreet shuffling of available system fonts to prevent identification.
'''

import random
from typing import List

class FontRandomizer:
    '''
    Spoofs the list of available fonts in the browser.
    '''
    COMMON_FONTS = {
        'win': ["Segoe UI", "Tahoma", "Calibri", "Cambria", "Consolas", "Courier New", "Georgia", "Impact", "Microsoft Sans Serif"],
        'mac': ["San Francisco", "Helvetica Neue", "Lucida Grande", "AppleGothic", "Monaco", "Optima", "Palatino", "Zapfino"],
        'lin': ["Ubuntu", "DejaVu Sans", "FreeSans", "Liberation Sans", "Roboto", "Noto Sans"]
    }

    @staticmethod
    def get_font_script(os_type: str = 'win') -> str:
        '''
        Returns JS to intercept element sizing (used for font detection) and 
        spoof a randomized set of system fonts.
        '''
        base_fonts = FontRandomizer.COMMON_FONTS.get(os_type, FontRandomizer.COMMON_FONTS['win'])
        selected = random.sample(base_fonts, k=random.randint(4, len(base_fonts)))
        
        return f"""
        (function() {{
            const spoofedFonts = {selected};
            const originalOffsetWidth = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetWidth').get;
            const originalOffsetHeight = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight').get;

            Object.defineProperty(HTMLElement.prototype, 'offsetWidth', {{
                get: function() {{
                    if (this.style.fontFamily && !spoofedFonts.some(f => this.style.fontFamily.includes(f))) {{
                        return originalOffsetWidth.call(this) + (Math.random() * 2);
                    }}
                    return originalOffsetWidth.call(this);
                }}
            }});

            console.log("[LordRequests] Font Randomizer Active for {os_type}. Loaded " + spoofedFonts.length + " fonts.");
        }})();
        """
