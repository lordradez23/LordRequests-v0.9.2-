'''
Broken Link Auditor
~~~~~~~~~~~~~~~~~~~

Scans a site for 404, 403, and 500 status code links.
'''

import hrequests
from typing import List, Dict, Optional

class BrokenLinkAuditor:
    def __init__(self, crawler: Optional['DeepCrawler'] = None):
        self.crawler = crawler
        self.broken_links: List[Dict] = []

    def audit_url(self, url: str) -> Dict:
        '''
        Checks a single URL and returns its status.
        '''
        try:
            resp = hrequests.head(url, timeout=5, follow_redirects=True)
            status = resp.status_code
        except Exception as e:
            status = -1 # Connection error
            
        result = {'url': url, 'status': status}
        if status >= 400 or status == -1:
            self.broken_links.append(result)
        return result

    def audit_site(self, start_url: str, max_depth: int = 1):
        '''
        Uses a crawler to find links and audits them.
        '''
        from .crawler import DeepCrawler
        crawler = DeepCrawler(start_url, max_depth=max_depth)
        found_urls = crawler.crawl()
        
        print(f"Auditing {len(found_urls)} URLs...")
        for url in found_urls:
            self.audit_url(url)
            
        return self.broken_links

    def get_report(self) -> str:
        summary = f"Broken Link Audit Report\n"
        summary += "=" * 50 + "\n"
        if not self.broken_links:
            summary += "No broken links found.\n"
        else:
            for link in self.broken_links:
                summary += f"  - [{link['status']}] {link['url']}\n"
        return summary
