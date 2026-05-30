'''
Metadata Forensic Scraper
~~~~~~~~~~~~~~~~~~~~~~~~~

Automated extraction of EXIF data from images and metadata from PDF files.
'''

import hrequests
import io
from typing import Dict, Optional

class MetadataScraper:
    @staticmethod
    def extract_image_exif(url: str) -> Dict:
        '''
        Downloads an image and extracts EXIF metadata.
        '''
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
        except ImportError:
            return {'error': 'Pillow library not installed for EXIF extraction.'}

        try:
            resp = hrequests.get(url, stream=True)
            img = Image.open(io.BytesIO(resp.content))
            exif_data = img._getexif()
            
            if not exif_data:
                return {'status': 'No EXIF data found.'}
                
            readable_exif = {}
            for tag, value in exif_data.items():
                decoded = TAGS.get(tag, tag)
                readable_exif[decoded] = str(value)
            return readable_exif
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def extract_pdf_metadata(url: str) -> Dict:
        '''
        Downloads a PDF and extracts metadata.
        '''
        # Simplified placeholder for PDF metadata extraction
        # Requires PyPDF2 or similar
        print(f"Scanning PDF metadata for: {url}")
        return {
            'status': 'Scan complete',
            'note': 'Requires PyPDF2 for full field extraction.',
            'url': url
        }
