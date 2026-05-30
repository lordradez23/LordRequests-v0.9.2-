'''
WebView Identity Sync
~~~~~~~~~~~~~~~~~~~~~

Consistency mapping between browser sessions and mobile WebViews.
'''

from hrequests.operations.mobile import MobileSpoofer
from typing import Dict

class WebViewHandler:
    '''
    Manages WebView-specific headers and identifiers.
    '''
    @staticmethod
    def get_sync_headers(platform: str = 'android') -> Dict[str, str]:
        '''
        Returns headers that mimic a native app's WebView container.
        '''
        base = MobileSpoofer.get_mobile_headers(platform)
        if platform.lower() == 'ios':
            base["X-Requested-With"] = "WebKit.WebView"
        else:
            base["X-Requested-With"] = "com.google.android.webview"
            
        return base

    @staticmethod
    def get_javascript_bridge_script() -> str:
        '''
        Injects a mock JS bridge to simulate a native app environment.
        '''
        return """
        (function() {
            window.LordLink = {
                postMessage: (msg) => console.log("WebView Log: " + msg),
                onReceive: (callback) => { window._lordCallback = callback; }
            };
        })();
        """
