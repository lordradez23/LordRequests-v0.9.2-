'''
API Doc Generator
~~~~~~~~~~~~~~~~~

Automatically generate OpenAPI/Swagger documentation from observed requests.
'''

import json
from typing import List, Dict, Any
from urllib.parse import urlparse

class SwaggerGenerator:
    def __init__(self, title: str = "LordRequests Scraped API", version: str = "1.0.0"):
        self.spec = {
            "openapi": "3.0.0",
            "info": {
                "title": title,
                "version": version,
                "description": "Auto-generated documentation from LordRequests traffic."
            },
            "paths": {}
        }

    def add_request(self, method: str, url: str, headers: Dict = None, payload: Any = None):
        parsed = urlparse(url)
        path = parsed.path or "/"
        
        if path not in self.spec["paths"]:
            self.spec["paths"][path] = {}
        
        method = method.lower()
        if method not in self.spec["paths"][path]:
            self.spec["paths"][path][method] = {
                "summary": f"Auto-generated {method.upper()} to {path}",
                "responses": {
                    "200": {
                        "description": "Successful request"
                    }
                }
            }
            
            if payload:
                self.spec["paths"][path][method]["requestBody"] = {
                    "content": {
                        "application/json": {
                            "schema": self._infer_schema(payload)
                        }
                    }
                }

    def _infer_schema(self, obj: Any) -> Dict:
        if isinstance(obj, dict):
            return {
                "type": "object",
                "properties": {k: self._infer_schema(v) for k, v in obj.items()}
            }
        elif isinstance(obj, list):
            return {
                "type": "array",
                "items": self._infer_schema(obj[0]) if obj else {"type": "string"}
            }
        elif isinstance(obj, bool):
            return {"type": "boolean"}
        elif isinstance(obj, int):
            return {"type": "integer"}
        elif isinstance(obj, float):
            return {"type": "number"}
        else:
            return {"type": "string"}

    def export(self, filename: str = "swagger.json"):
        with open(filename, 'w') as f:
            json.dump(self.spec, f, indent=4)
        print(f"Swagger spec exported to {filename}")
