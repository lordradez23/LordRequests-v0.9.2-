'''
Honeypot Filter
~~~~~~~~~~~~~~~

Scans the DOM for hidden elements and links used to detect bots.
'''

import hrequests
from typing import List

class HoneypotFilter:
    def __init__(self, response: hrequests.response.Response):
        self.response = response
        self.html = response.html

    def find_honeypots(self) -> List:
        '''
        Identifies elements that are likely honeypots.
        '''
        honeypots = []
        
        # Look for links that are hidden via CSS
        # Note: This is an approximation as we don't have full CSS computed styles here
        # But we can check for common patterns in 'style' attributes.
        
        selectors = [
            'a[style*="display:none"]',
            'a[style*="visibility:hidden"]',
            'a[style*="opacity:0"]',
            'a[style*="width:0"]',
            'a[style*="height:0"]',
            'div[style*="display:none"] a',
            '.hidden a',
            '#hidden a'
        ]
        
        for selector in selectors:
            elements = self.html.tree.css(selector)
            honeypots.extend(elements)
            
        return honeypots

    def sanitize(self):
        '''
        Decomposes all identified honeypot elements from the tree.
        '''
        honeypots = self.find_honeypots()
        for el in honeypots:
            el.decompose()
        
        print(f"Removed {len(honeypots)} potential honeypots from the DOM.")
