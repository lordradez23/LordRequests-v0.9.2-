'''
API Endpoint Fuzzer
~~~~~~~~~~~~~~~~~~~

Integrated fuzzer for identifying hidden API parameters and testing boundary conditions.
'''

import hrequests
from typing import List, Dict, Any, Optional
import json

class APIFuzzer:
    '''
    Fuzzes API endpoints with various parameters and payloads.
    '''
    def __init__(self, base_url: str, session: Optional[Any] = None):
        self.base_url = base_url
        self.session = session or hrequests.Session()
        self.results: List[Dict] = []

    def fuzz_parameters(self, endpoint: str, param_names: List[str], payloads: List[Any]):
        '''
        Tests multiple payloads across a set of parameter names.
        '''
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        for param in param_names:
            for payload in payloads:
                try:
                    # Test via GET
                    resp = self.session.get(url, params={param: payload}, timeout=5)
                    self._record_result(url, "GET", {param: payload}, resp)
                    
                    # Test via POST (JSON)
                    resp = self.session.post(url, json={param: payload}, timeout=5)
                    self._record_result(url, "POST", {param: payload}, resp)
                except Exception as e:
                    print(f"[Fuzzer] Request failed for {param}={payload}: {e}")

    def _record_result(self, url: str, method: str, data: Dict, resp: hrequests.Response):
        # We look for interesting status codes or significant body length changes
        self.results.append({
            "url": url,
            "method": method,
            "payload": data,
            "status": resp.status_code,
            "size": len(resp.content),
            "is_interesting": resp.status_code not in [404, 403, 400]
        })

    def get_interesting_results(self) -> List[Dict]:
        return [r for r in self.results if r['is_interesting']]
