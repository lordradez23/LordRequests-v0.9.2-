'''
Advanced Image Forensics
~~~~~~~~~~~~~~~~~~~~~~~~

OCR extraction and EXIF metadata scrubbing for harvested assets.
'''

import os
from typing import Dict, Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

class ImageForensics:
    '''
    Tools for scrubbing and analyzing image data.
    '''
    @staticmethod
    def scrub_metadata(image_path: str, output_path: Optional[str] = None) -> str:
        '''
        Removes EXIF and other metadata from an image.
        '''
        if not PIL_AVAILABLE:
            raise ImportError("Pillow (PIL) is required for metadata scrubbing.")
            
        output_path = output_path or image_path
        img = Image.open(image_path)
        data = list(img.getdata())
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.putdata(data)
        image_without_exif.save(output_path)
        return output_path

    @staticmethod
    def extract_text(image_path: str) -> str:
        '''
        Performs OCR to extract text from an image.
        '''
        if not OCR_AVAILABLE:
            return "OCR Error: 'pytesseract' and Tesseract-OCR engine are required."
            
        try:
            return pytesseract.image_to_string(Image.open(image_path))
        except Exception as e:
            return f"OCR Error: {str(e)}"

    @staticmethod
    def get_info(image_path: str) -> Dict:
        '''
        Returns basic image info (size, format, mode).
        '''
        if not PIL_AVAILABLE:
            return {"error": "Pillow not installed"}
            
        img = Image.open(image_path)
        return {
            "size": img.size,
            "format": img.format,
            "mode": img.mode,
            "filename": os.path.basename(image_path)
        }
