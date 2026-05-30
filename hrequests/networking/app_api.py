'''
App-API Emulator
~~~~~~~~~~~~~~~~

Emulating mobile application request signatures and handshake patterns.
'''

import hashlib
import hmac
import time
from typing import Dict, Any, Optional

class AppEmulator:
    '''
    Simulates application-level request authentication for mobile APIs.
    '''
    def __init__(self, app_id: str, secret: str):
        self.app_id = app_id
        self.secret = secret

    def sign_request(self, payload: Dict[str, Any]) -> Dict[str, str]:
        '''
        Generates a HMAC-based signature for a request payload.
        '''
        timestamp = str(int(time.time()))
        message = f"{self.app_id}{timestamp}{hashlib.md5(str(payload).encode()).hexdigest()}"
        
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return {
            "X-App-ID": self.app_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature
        }

    @staticmethod
    def get_bundle_headers(bundle_id: str) -> Dict[str, str]:
        '''
        Returns standard headers for a specific application bundle.
        '''
        return {
            "X-Apple-I-Bundle-Id": bundle_id,
            "X-Requested-With": bundle_id
        }
