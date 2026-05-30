'''
Ad-Fraud Scanner
~~~~~~~~~~~~~~~~

Uses stealth browsing to verify the presence and visibility of digital ads
on a page, helping detect fraud and placement manipulation.
'''

import hrequests
from typing import List, Dict, Optional

class AdFraudScanner:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.scan_results: Dict = {}

    def scan_for_ads(self, ad_selectors: List[str]) -> Dict:
        '''
        Renders the page and checks for the existence of ad elements.
        '''
        resp = hrequests.get(self.target_url)
        with resp.render(mock_human=True) as page:
            for selector in ad_selectors:
                visible = page.isVisible(selector)
                enabled = page.isEnabled(selector)
                
                # Check for hidden placement (e.g. 1x1 iframes)
                # This requires JS evaluation
                dimensions = page.evaluate('''selector => {
                    const el = document.querySelector(selector);
                    if (!el) return null;
                    const rect = el.getBoundingClientRect();
                    return {width: rect.width, height: rect.height};
                }''', selector)

                self.scan_results[selector] = {
                    'visible': visible,
                    'enabled': enabled,
                    'dimensions': dimensions,
                    'is_suspicious': (dimensions and (dimensions['width'] < 5 or dimensions['height'] < 5))
                }
        
        return self.scan_results

    def get_summary(self) -> str:
        '''
        Returns a human-readable summary of the ad scan.
        '''
        summary = f"Ad-Fraud Scan for: {self.target_url}\n"
        summary += "=" * 50 + "\n"
        
        for selector, data in self.scan_results.items():
            summary += f"Selector: {selector}\n"
            summary += f"  - Visible: {'YES' if data['visible'] else 'NO'}\n"
            summary += f"  - Enabled: {'YES' if data['enabled'] else 'NO'}\n"
            if data['dimensions']:
                summary += f"  - Dimensions: {data['dimensions']['width']}x{data['dimensions']['height']}\n"
            if data['is_suspicious']:
                summary += "  - !!! SUSPICIOUS: Extremely small dimensions detected (possible hidden ad fraud) !!!\n"
            summary += "\n"
            
        return summary
