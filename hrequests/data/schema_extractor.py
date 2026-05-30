'''
Schema.org Extractor
~~~~~~~~~~~~~~~~~~~~

Extracts structured data (JSON-LD and Microdata) from web pages.
'''

import hrequests
import json
from typing import List, Dict

class SchemaExtractor:
    def __init__(self, response: hrequests.response.Response):
        self.response = response
        self.html = response.html

    def extract_json_ld(self) -> List[Dict]:
        '''
        Finds all script[type="application/ld+json"] elements and parses them.
        '''
        schemas = []
        for script in self.html.find('script[type="application/ld+json"]'):
            try:
                data = json.loads(script.text)
                if isinstance(data, list):
                    schemas.extend(data)
                else:
                    schemas.append(data)
            except json.JSONDecodeError:
                continue
        return schemas

    def extract_microdata(self) -> List[Dict]:
        '''
        Placeholder for Microdata extraction. 
        In a full implementation, this would look for 'itemscope', 'itemtype', 'itemprop'.
        '''
        print("Scanning Microdata...")
        return [{'status': 'Partial Scan complete', 'note': 'Requires specialized Microdata parser.'}]

    def get_all_structured_data(self) -> Dict:
        return {
            'json_ld': self.extract_json_ld(),
            'microdata': self.extract_microdata()
        }
