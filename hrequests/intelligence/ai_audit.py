'''
AI Provenance Auditor
~~~~~~~~~~~~~~~~~~~~

Identifies if content has been indexed by major web archives or
AI training datasets by querying public indices.
'''

import hrequests
from typing import Dict, Optional

class AIProvenanceAuditor:
    WAYBACK_URL = "https://archive.org/wayback/available"

    def __init__(self, url: str):
        self.url = url
        self.audit_results: Dict = {}

    def check_wayback(self) -> Dict:
        '''
        Checks if the URL is archived in the Wayback Machine.
        '''
        resp = hrequests.get(self.WAYBACK_URL, params={'url': self.url})
        if resp.status_code == 200:
            data = resp.json()
            archived = 'archived_snapshots' in data and bool(data['archived_snapshots'])
            self.audit_results['wayback'] = {
                'archived': archived,
                'snapshot': data.get('archived_snapshots', {}).get('closest', {}) if archived else None
            }
        return self.audit_results['wayback']

    def check_common_crawl(self) -> Dict:
        '''
        Placeholder for Common Crawl Index check.
        In a full implementation, this would query the CDX server.
        '''
        self.audit_results['common_crawl'] = {
            'status': 'Check Not Implemented',
            'note': 'Requires CDX index querying logic.'
        }
        return self.audit_results['common_crawl']

    def run_full_audit(self) -> Dict:
        '''
        Runs all available provenance checks.
        '''
        self.check_wayback()
        self.check_common_crawl()
        return self.audit_results

    def get_summary(self) -> str:
        '''
        Returns a human-readable summary.
        '''
        res = self.audit_results
        summary = f"AI Provenance Audit for: {self.url}\n"
        summary += "-" * 50 + "\n"
        
        wb = res.get('wayback', {})
        summary += f"Wayback Machine: {'FOUND' if wb.get('archived') else 'NOT FOUND'}\n"
        if wb.get('archived'):
            summary += f"  - Latest Snapshot: {wb['snapshot'].get('timestamp')}\n"
            summary += f"  - Archive URL: {wb['snapshot'].get('url')}\n"
            
        cc = res.get('common_crawl', {})
        summary += f"Common Crawl: {cc['status']}\n"
        
        return summary
