'''
Legal Compliance Auditor
~~~~~~~~~~~~~~~~~~~~~~~~

Audits scraping scope against robots.txt and ToS boundaries.
'''

import hrequests
from urllib.parse import urlparse
from typing import Dict, List

class ComplianceAuditor:
    '''
    Checks target URLs against robots.txt rules and generates audit logs.
    '''
    def __init__(self):
        self.audit_log: List[Dict] = []

    def fetch_robots(self, base_url: str) -> str:
        '''Fetches the robots.txt file from a domain.'''
        parsed = urlparse(base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            resp = hrequests.get(robots_url, timeout=5)
            return resp.text if resp.status_code == 200 else ""
        except Exception:
            return ""

    def is_allowed(self, robots_txt: str, path: str, user_agent: str = "*") -> bool:
        '''
        Basic check if the given path is allowed in robots.txt.
        '''
        disallowed = []
        for line in robots_txt.split('\n'):
            line = line.strip()
            if line.lower().startswith("user-agent:"):
                current_agent = line.split(":", 1)[1].strip()
            elif line.lower().startswith("disallow:") and (current_agent == user_agent or current_agent == "*"):
                rule = line.split(":", 1)[1].strip()
                if rule:
                    disallowed.append(rule)
        return not any(path.startswith(rule) for rule in disallowed)

    def audit(self, url: str) -> Dict:
        '''Runs a full compliance check on a URL.'''
        parsed = urlparse(url)
        robots = self.fetch_robots(url)
        allowed = self.is_allowed(robots, parsed.path)
        result = {"url": url, "allowed": allowed, "robots_fetched": bool(robots)}
        self.audit_log.append(result)
        return result
