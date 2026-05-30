'''
KYC / Fingerprint Stress Tester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analyzes the consistency and stealth of different TLS fingerprints
and browser profiles to identify potential detection vectors.
'''

import hrequests
from typing import Dict, List, Optional
import json

class FingerprintStressTester:
    def __init__(self, target_url: str = 'https://httpbin.org/headers'):
        self.target_url = target_url
        self.fingerprint_data: Dict = {}

    def test_profile(self, browser: str, version: int) -> Dict:
        '''
        Tests a specific browser profile and returns the reflected headers.
        '''
        session = hrequests.Session(browser=browser, version=version)
        resp = session.get(self.target_url)
        if resp.status_code == 200:
            reflected = resp.json().get('headers', {})
            self.fingerprint_data[f"{browser}_{version}"] = reflected
            return reflected
        return {}

    def compare_profiles(self, profiles: List[Dict]) -> Dict:
        '''
        Compares multiple profiles and identifies discrepancies.
        profiles: [{'browser': 'chrome', 'version': 120}, ...]
        '''
        all_headers = {}
        for p in profiles:
            h = self.test_profile(p['browser'], p['version'])
            all_headers[f"{p['browser']}_{p['version']}"] = h
        
        # Analyze discrepancies
        analysis = {'discrepancies': {}, 'unique_headers': {}}
        
        # Find all keys
        all_keys = set()
        for h in all_headers.values():
            all_keys.update(h.keys())
            
        for key in all_keys:
            values = {name: h.get(key) for name, h in all_headers.items()}
            unique_values = set(values.values())
            if len(unique_values) > 1:
                analysis['discrepancies'][key] = values
            else:
                analysis['unique_headers'][key] = list(unique_values)[0]
                
        return analysis

    def get_summary(self, analysis: Dict) -> str:
        '''
        Returns a human-readable summary of the stress test.
        '''
        summary = "Fingerprint Stress Test Analysis\n"
        summary += "=" * 50 + "\n"
        
        disc = analysis.get('discrepancies', {})
        summary += f"Discrepancies Found: {len(disc)}\n"
        for key, vals in disc.items():
            summary += f"  - Header '{key}':\n"
            for profile, val in vals.items():
                summary += f"    * {profile}: {val}\n"
        
        summary += "\nConsistent Headers:\n"
        for key, val in analysis.get('unique_headers', {}).items():
            summary += f"  - {key}: {val}\n"
            
        return summary
