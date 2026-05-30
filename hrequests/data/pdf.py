'''
PDF Forensic Extractor
~~~~~~~~~~~~~~~~~~~~~~

Metadata and text-layer extraction for scraped PDF documents.
'''

from typing import Dict, Any, Optional

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

class PDFExtractor:
    '''
    Analyzes and extracts data from PDF files.
    '''
    @staticmethod
    def get_metadata(file_path: str) -> Dict[str, Any]:
        '''
        Extracts author, creator, and other metadata from a PDF.
        '''
        if not PYPDF_AVAILABLE:
            return {"error": "pypdf library not installed"}
            
        try:
            reader = pypdf.PdfReader(file_path)
            meta = reader.metadata
            return {
                "author": meta.author,
                "creator": meta.creator,
                "producer": meta.producer,
                "subject": meta.subject,
                "title": meta.title,
                "pages": len(reader.pages)
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def extract_text(file_path: str, max_pages: int = 10) -> str:
        '''
        Extracts text from the first N pages of the PDF.
        '''
        if not PYPDF_AVAILABLE:
            return "Library pypdf not installed."
            
        try:
            reader = pypdf.PdfReader(file_path)
            text = ""
            for i in range(min(len(reader.pages), max_pages)):
                text += reader.pages[i].extract_text() + "\n"
            return text
        except Exception as e:
            return f"Extraction error: {str(e)}"
