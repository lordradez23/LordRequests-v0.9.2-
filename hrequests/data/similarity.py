'''
Image Similarity Aggregator
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Perceptual hashing (dHash) for clustering and deduplicating harvested images.
'''

from typing import List, Tuple
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class ImageSimilarity:
    '''
    Calculates perceptual hashes for image comparison.
    '''
    @staticmethod
    def calculate_dhash(image_path: str, size: int = 8) -> str:
        '''
        Calculates the Difference Hash (dHash) of an image.
        '''
        if not PIL_AVAILABLE:
            return "Error: Pillow not installed"
            
        try:
            img = Image.open(image_path).convert('L').resize((size + 1, size), Image.Resampling.LANCZOS)
            pixels = list(img.getdata())
            
            diff = []
            for row in range(size):
                for col in range(size):
                    pixel_left = pixels[row * (size + 1) + col]
                    pixel_right = pixels[row * (size + 1) + col + 1]
                    diff.append(pixel_left > pixel_right)
            
            # Convert boolean list to hex string
            decimal_value = 0
            hex_string = []
            for index, value in enumerate(diff):
                if value:
                    decimal_value += 2 ** (index % 8)
                if (index % 8) == 7:
                    hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                    decimal_value = 0
            return "".join(hex_string)
        except Exception as e:
            return f"Hash Error: {str(e)}"

    @staticmethod
    def hamming_distance(hash1: str, hash2: str) -> int:
        '''
        Calculates the Hamming distance between two hex hashes.
        '''
        if len(hash1) != len(hash2):
            return 999
        return sum(bin(int(a, 16) ^ int(b, 16)).count('1') for a, b in zip(hash1, hash2))
