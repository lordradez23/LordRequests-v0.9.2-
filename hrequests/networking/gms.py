'''
GMS/Firebase Spoofing
~~~~~~~~~~~~~~~~~~~~

Simulated integration with Google Mobile Services and Firebase signals.
'''

import random
import string
from typing import Dict

class GMSSpoofer:
    '''
    Generates mock identifiers for GMS and Firebase services.
    '''
    @staticmethod
    def generate_fcm_token() -> str:
        '''
        Generates a token format similar to Firebase Cloud Messaging.
        '''
        prefix = "f" + "".join(random.choices(string.ascii_letters + string.digits, k=11))
        body = "".join(random.choices(string.ascii_letters + string.digits + "_-", k=140))
        return f"{prefix}:{body}"

    @staticmethod
    def get_gms_headers() -> Dict[str, str]:
        '''
        Returns common headers included by GMS-enabled applications.
        '''
        android_id = "".join(random.choices("0123456789abcdef", k=16))
        return {
            "X-Android-ID": android_id,
            "X-Android-GMS": "1",
            "X-Google-GMS-Version": "234414044"
        }

    @staticmethod
    def get_firebase_config() -> Dict[str, str]:
        '''
        Returns a mock Firebase installation config.
        '''
        return {
            "installationId": "".join(random.choices(string.ascii_letters + string.digits, k=22)),
            "authToken": "".join(random.choices(string.ascii_letters + string.digits, k=128))
        }
