'''
Deep-Link Crawler
~~~~~~~~~~~~~~~~~

Provides recursive crawling capabilities with depth and domain control.
'''

import hrequests
from urllib.parse import urljoin, urlparse
from typing import Set, List, Optional

class DeepCrawler:
    def __init__(self, start_url: str, max_depth: int = 2, same_domain: bool = True):
        self.start_url = start_url
        self.max_depth = max_depth
        self.same_domain = same_domain
        self.domain = urlparse(start_url).netloc
        self.visited: Set[str] = set()
        self.queue: List[tuple] = [(start_url, 0)] # (url, current_depth)

    def crawl(self) -> Set[str]:
        '''
        Executes the recursive crawl and returns the set of all found URLs.
        '''
        while self.queue:
            url, depth = self.queue.pop(0)
            
            if url in self.visited or depth > self.max_depth:
                continue
                
            self.visited.add(url)
            print(f"Crawling ({depth}): {url}")
            
            try:
                resp = hrequests.get(url, timeout=10)
                if resp.status_code == 200:
                    self._extract_links(resp, depth)
            except Exception as e:
                print(f"Failed to crawl {url}: {e}")
                
        return self.visited

    def _extract_links(self, resp: hrequests.response.Response, current_depth: int):
        '''
        Extracts all absolute links from a response and adds them to the queue.
        '''
        links = resp.html.find('a')
        for link in links:
            href = link.attrs.get('href')
            if not href:
                continue
                
            absolute_url = urljoin(resp.url, href)
            # Clean url (remove fragments)
            absolute_url = absolute_url.split('#')[0]
            
            if self.same_domain and urlparse(absolute_url).netloc != self.domain:
                continue
                
            if absolute_url not in self.visited:
                self.queue.append((absolute_url, current_depth + 1))
