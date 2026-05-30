'''
Price Fairness Auditor
~~~~~~~~~~~~~~~~~~~~~~

Detects dynamic pricing and regional manipulation by performing
stealthy batch requests across multiple fingerprints and proxies.
'''

from typing import List, Dict, Optional
import hrequests

class PriceAuditor:
    def __init__(self, url: str, item_selector: str):
        self.url = url
        self.item_selector = item_selector
        self.results: List[Dict] = []

    def audit(self, proxies: List[str], browsers: List[str] = ['chrome', 'firefox']):
        '''
        Performs a multi-region/multi-fingerprint audit.
        '''
        reqs = []
        for proxy in proxies:
            for browser in browsers:
                # Create asynchronous requests with different fingerprints
                reqs.append(
                    hrequests.async_get(
                        self.url,
                        browser=browser,
                        proxy=proxy,
                        timeout=15
                    )
                )
        
        # Execute concurrent requests
        responses = hrequests.map(reqs, size=len(reqs))
        
        for resp in responses:
            price = "N/A"
            if resp.status_code == 200:
                element = resp.html.find(self.item_selector, first=True)
                if element:
                    price = element.text.strip()
            
            self.results.append({
                'proxy': resp.proxy,
                'browser': resp.browser,
                'status': resp.status_code,
                'price': price
            })
        
        return self.results

    def detect_manipulation(self) -> bool:
        '''
        Checks if there are significant variations in the price across different requests.
        '''
        prices = [r['price'] for r in self.results if r['price'] != "N/A"]
        if not prices:
            return False
        return len(set(prices)) > 1

    def get_summary(self):
        '''
        Returns a formatted summary of the findings.
        '''
        summary = f"Price Audit for: {self.url}\n"
        summary += "=" * 50 + "\n"
        for res in self.results:
            summary += f"Proxy: {res['proxy']} | Browser: {res['browser']} | Price: {res['price']}\n"
        
        if self.detect_manipulation():
            summary += "\nWARNING: Price manipulation detected!"
        else:
            summary += "\nNo significant price variation detected."
        
        return summary
