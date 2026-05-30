'''
Semantic Scraper (LLM-Ready)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bridge for zero-shot data extraction using LLMs.
'''

import json
from typing import Any, Dict, List, Optional

class SemanticExtractor:
    '''
    Prepares and structures scraped content for LLM ingestion.
    '''
    def __init__(self, provider: str = 'openai', api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key

    def prepare_payload(self, html: str, schema: Dict[str, Any]) -> str:
        '''
        Creates a prompt for the LLM to extract data based on a schema.
        '''
        prompt = (
            "Extract the following structured data from the provided HTML content.\n"
            f"Return ONLY a valid JSON object matching this schema: {json.dumps(schema)}\n\n"
            f"HTML Content:\n{html[:5000]}..." # Truncate for token limits
        )
        return prompt

    def parse_response(self, response: str) -> Dict[str, Any]:
        '''
        Cleans and parses the JSON response from the LLM.
        '''
        try:
            # Find JSON block in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(response[start:end])
            return json.loads(response)
        except (json.JSONDecodeError, ValueError):
            return {"error": "Failed to parse LLM response as JSON", "raw": response}

    @staticmethod
    def chunk_html(html: str, max_chars: int = 4000) -> List[str]:
        '''
        Splits large HTML into chunks for LLM context windows.
        '''
        return [html[i:i+max_chars] for i in range(0, len(html), max_chars)]
