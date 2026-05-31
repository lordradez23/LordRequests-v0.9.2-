'''
Broken Link Deep-Auditor
~~~~~~~~~~~~~~~~~~~~~~~~

Recursive checker for cross-domain broken link analysis and dead-end detection.
'''

import hrequests
from hrequests.parser import HTML
from typing import Set, Dict, List
from urllib.parse import urlparse

class LinkAuditor:
    '''
    Audits broad sets of links for availability and health.
    '''
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited: Set[str] = set()
        self.broken: Dict[str, int] = {}
        self.external: Set[str] = set()

    def audit(self, depth: int = 2):
        '''
        Recursively audits links up to a specific depth.
        '''
        self._check_url(self.start_url, depth)
        return {
            "total_visited": len(self.visited),
            "broken_links": self.broken,
            "external_references": list(self.external)
        }

    def _check_url(self, url: str, depth: int):
        if depth < 0 or url in self.visited:
            return
        
        self.visited.add(url)
        print(f"[Auditor] Checking: {url}")
        
        try:
            resp = hrequests.get(url, timeout=10)
            if resp.status_code >= 400:
                self.broken[url] = resp.status_code
                return
            
            if depth > 0 and urlparse(url).netloc == self.domain:
                links = resp.html.absolute_links
                for link in links:
                    if urlparse(link).netloc != self.domain:
                        self.external.add(link)
                    else:
                        self._check_url(link, depth - 1)
        except Exception:
            self.broken[url] = -1 # Connection error
