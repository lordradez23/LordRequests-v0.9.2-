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
    DEFAULT_FONTS = [
        "Arial", "Verdana", "Times New Roman", "Courier New", "Georgia",
        "Trebuchet MS", "Impact", "Comic Sans MS", "Tahoma", "Geneva"
    ]

    @staticmethod
    def get_font_script(subset_size: int = 5) -> str:
        '''
        Returns JS to intercept font detection and return a randomized subset.
        '''
        selected = random.sample(FontRandomizer.DEFAULT_FONTS, subset_size)
        return f"""
        (function() {{
            const originalQuery = document.fonts.query;
            if (document.fonts && document.fonts.query) {{
                document.fonts.query = function() {{
                    return Promise.resolve({selected});
                }};
            }}
        }})();
        """
