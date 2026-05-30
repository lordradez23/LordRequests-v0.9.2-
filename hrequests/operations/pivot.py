'''
Headless Pivot Logic
~~~~~~~~~~~~~~~~~~~~

Automates the transition from lightweight CFFI requests to full 
browser rendering when challenges are detected.
'''

import hrequests
from typing import Optional, Union

class HeadlessPivot:
    @staticmethod
    def execute_with_pivot(
        url: str,
        method: str = 'GET',
        session: Optional[hrequests.Session] = None,
        **kwargs
    ) -> Union[hrequests.response.Response, hrequests.browser.BrowserSession]:
        '''
        Executes a request via the Go engine, and pivots to a BrowserSession
        if a 403 or specific challenge is detected.
        '''
        client = session or hrequests
        
        try:
            resp = client.request(method=method, url=url, **kwargs)
            
            # Check for common challenge indicators
            # 403 is often a WAF block
            # 1020 is Cloudflare access denied
            if resp.status_code in [403, 401, 1020] or 'cloudflare' in resp.text.lower():
                print(f"Challenge detected ({resp.status_code}). Pivoting to BrowserSession...")
                return resp.render(mock_human=True)
            
            return resp
            
        except Exception as e:
            print(f"Request failed: {e}. Pivoting to BrowserSession...")
            # Fallback to browser
            return hrequests.render(url=url, mock_human=True, **kwargs)
