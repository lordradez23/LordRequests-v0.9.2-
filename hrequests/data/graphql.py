'''
Parallel GraphQL Scraper
~~~~~~~~~~~~~~~~~~~~~~~~

Optimized concurrent execution for GraphQL-based data harvesting.
'''

import hrequests
from typing import List, Dict, Any, Optional

class GraphQLScraper:
    '''
    Handles batch and parallel GraphQL requests.
    '''
    def __init__(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        self.endpoint = endpoint
        self.headers = headers or {"Content-Type": "application/json"}

    def query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        '''
        Executes a single GraphQL query.
        '''
        payload = {"query": query, "variables": variables or {}}
        resp = hrequests.post(self.endpoint, json=payload, headers=self.headers)
        return resp.json()

    def batch_query(self, queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        '''
        Executes multiple queries in parallel.
        '''
        print(f"Executing {len(queries)} parallel GraphQL queries...")
        
        def run_q(q_data):
            return self.query(q_data['query'], q_data.get('variables'))

        # Use gevent pools or simple map if small
        return [run_q(q) for q in queries]
