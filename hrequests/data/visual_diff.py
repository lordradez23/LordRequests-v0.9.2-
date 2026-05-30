'''
Visual Change Detection
~~~~~~~~~~~~~~~~~~~~~~~

Tracks visual changes on a page over time using screenshot comparisons.
'''

import hrequests
import os
from typing import Optional

class VisualChangeDetector:
    def __init__(self, url: str, storage_dir: str = 'snapshots'):
        self.url = url
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def capture(self, label: str) -> str:
        '''
        Captures a screenshot of the page and saves it.
        '''
        path = os.path.join(self.storage_dir, f"{label}.png")
        hrequests.render(self.url, mock_human=True).screenshot(path=path)
        return path

    def detect_diff(self, path1: str, path2: str) -> bool:
        '''
        Placeholder for pixel-diffing logic.
        Requires 'pillow' for actual pixel comparison.
        '''
        try:
            from PIL import Image, ImageChops
        except ImportError:
            print("Pillow required for visual diffing.")
            return False

        img1 = Image.open(path1)
        img2 = Image.open(path2)
        
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox():
            print(f"Visual change detected between {path1} and {path2}")
            return True
        return False
