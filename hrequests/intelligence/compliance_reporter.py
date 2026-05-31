'''
Automated Compliance Reporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generates summarized reports on robots.txt and ToS compliance for auditing.
'''

from typing import Dict, List
import json
import time

class ComplianceReporter:
    '''
    Aggregates compliance audit results and generates reports.
    '''
    def __init__(self):
        self.audits: List[Dict] = []

    def add_audit_result(self, domain: str, results: Dict):
        '''
        Adds a result from ComplianceAuditor.
        '''
        self.audits.append({
            "domain": domain,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "summary": results
        })

    def generate_json_report(self, filepath: str):
        '''
        Exports full audit history to JSON.
        '''
        with open(filepath, 'w') as f:
            json.dump({
                "report_type": "Compliance Audit",
                "generated_at": time.strftime('%Y-%m-%d %H:%M:%S'),
                "audits": self.audits
            }, f, indent=4)
        print(f"[Compliance] Report generated at {filepath}")

    def generate_markdown_summary(self) -> str:
        '''
        Returns a formatted markdown summary of compliance status.
        '''
        md = ["# LordRequests Compliance Audit Summary\n"]
        for audit in self.audits:
            md.append(f"## Domain: {audit['domain']}")
            md.append(f"- **Time**: {audit['timestamp']}")
            for key, val in audit['summary'].items():
                status = "✅" if val is True else ("❌" if val is False else "⚠️")
                md.append(f"- {key}: {status} ({val})")
            md.append("\n---\n")
        return "\n".join(md)
