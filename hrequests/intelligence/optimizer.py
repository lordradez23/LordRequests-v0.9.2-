'''
Digital Divide Content Optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Strips heavy media, scripts, and styles from web pages to provide
an optimized, low-bandwidth snapshot for disadvantaged regions.
'''

import hrequests
from typing import Optional

class ContentOptimizer:
    def __init__(self, response: hrequests.response.Response):
        self.response = response
        self.html = response.html

    def optimize(self, strip_images: bool = True, strip_scripts: bool = True, strip_styles: bool = True) -> str:
        '''
        Optimizes the content by removing heavy elements.
        Returns the optimized HTML as a string.
        '''
        # Create a copy of the tree if possible, or just work on the current one
        # Note: selectolax nodes can be removed
        
        tags_to_remove = []
        if strip_scripts:
            tags_to_remove.extend(['script', 'noscript'])
        if strip_styles:
            tags_to_remove.extend(['style', 'link[rel="stylesheet"]'])
        if strip_images:
            tags_to_remove.extend(['img', 'video', 'audio', 'source', 'picture'])

        for tag in tags_to_remove:
            for element in self.html.tree.css(tag):
                element.decompose()

        return self.html.tree.body.html

    def get_text_only(self) -> str:
        '''
        Returns only the textual content of the page, formatted.
        '''
        return self.html.text

    def save_optimized(self, path: str):
        '''
        Saves the optimized HTML to a file.
        '''
        optimized_html = self.optimize()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(optimized_html)
        print(f"Optimized version saved to {path}")
