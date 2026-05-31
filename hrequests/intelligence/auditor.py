'''
Broken Link Deep-Auditor.
Goes through a site recursively to find dead links and external references.
'''

import hrequests
from hrequests.parser import HTML
from typing import Set, Dict, List
from urllib.parse import urlparse

class LinkAuditor:
    '''
    Crawls through links to see which ones are actually alive.
    '''
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited: Set[str] = set()
        self.broken: Dict[str, int] = {}
        self.external: Set[str] = set()

    def audit(self, depth: int = 2):
        '''
        Starts the crawl. depth=0 means just the start page.
        '''
        self._check_url(self.start_url, depth)
        return {
            "total_visited": len(self.visited),
            "broken_links": self.broken,
            "external_references": list(self.external)
        }

    def _check_url(self, url: str, depth: int):
        # Don't visit the same page twice or go too deep
        if depth < 0 or url in self.visited:
            return
        
        self.visited.add(url)
        print(f"[Auditor] Checking: {url}")
        
        try:
            resp = hrequests.get(url, timeout=10)
            # 400+ means something is wrong (404, 403, etc)
            if resp.status_code >= 400:
                self.broken[url] = resp.status_code
                return
            
            # If it's an internal link, we'll follow it if we have depth left
            if depth > 0 and urlparse(url).netloc == self.domain:
                links = resp.html.absolute_links
                for link in links:
                    if urlparse(link).netloc != self.domain:
                        self.external.add(link)
                    else:
                        self._check_url(link, depth - 1)
        except Exception:
            self.broken[url] = -1 # Probably a connection timeout or DNS fail
