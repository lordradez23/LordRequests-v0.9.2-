'''
Global Supply-Chain Watchdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitors product availability and inventory levels across multiple
regions and proxies to identify hoarding or artificial shortages.
'''

import hrequests
from typing import List, Dict, Optional

class SupplyWatchdog:
    def __init__(self, item_url: str, availability_selector: str):
        self.item_url = item_url
        self.availability_selector = availability_selector
        self.snapshots: List[Dict] = []

    def check_availability(self, proxies: List[str]) -> List[Dict]:
        '''
        Checks availability across different proxies (regions).
        '''
        reqs = [
            hrequests.async_get(self.item_url, proxy=proxy, timeout=10)
            for proxy in proxies
        ]
        
        responses = hrequests.map(reqs, size=len(reqs))
        
        current_snapshots = []
        for resp in responses:
            is_available = False
            status_text = "Unknown"
            
            if resp.status_code == 200:
                element = resp.html.find(self.availability_selector, first=True)
                if element:
                    status_text = element.text.strip().lower()
                    # Heuristics for availability
                    is_available = "in stock" in status_text or "available" in status_text
            
            snapshot = {
                'proxy': resp.proxy,
                'status_code': resp.status_code,
                'status_text': status_text,
                'is_available': is_available
            }
            current_snapshots.append(snapshot)
            self.snapshots.append(snapshot)
            
        return current_snapshots

    def detect_hoarding(self) -> bool:
        '''
        Returns True if the product is available in some regions but not others,
        suggesting potential geographic hoarding or artificial shortage.
        '''
        availabilities = [s['is_available'] for s in self.snapshots]
        if not availabilities:
            return False
        return any(availabilities) and not all(availabilities)

    def get_summary(self) -> str:
        '''
        Returns a human-readable summary of the supply status.
        '''
        summary = f"Supply-Chain Watch: {self.item_url}\n"
        summary += "-" * 50 + "\n"
        
        for s in self.snapshots:
            summary += f"Region (Proxy): {s['proxy']} | Available: {'YES' if s['is_available'] else 'NO'} ({s['status_text']})\n"
            
        if self.detect_hoarding():
            summary += "\nALERT: Genetic hoarding or artificial shortage detected across regions."
        else:
            summary += "\nSupply appears consistent across monitored regions."
            
        return summary
