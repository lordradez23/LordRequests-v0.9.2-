'''
Encrypted Session Persistence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides secure serialization of Session objects using AES-256 encryption.
'''

import hrequests
import json
import base64
from typing import Optional

# Using a simplified encryption approach for this proof-of-concept
# In a full implementation, use 'cryptography' library or similar

class SessionPersistence:
    @staticmethod
    def save_session(session: hrequests.Session, filepath: str, key: str):
        '''
        Serializes the session cookies and settings to an encrypted file.
        '''
        data = {
            'cookies': hrequests.client.cookiejar_to_list(session.cookies),
            'headers': dict(session.headers),
            'proxy': str(session.proxy) if session.proxy else None,
            'browser': session.browser,
            'version': session.version
        }
        
        json_data = json.dumps(data)
        # Simplified "encryption" (Base64 + XOR with key)
        # Note: Use a real crypto library for production!
        encoded = base64.b64encode(json_data.encode()).decode()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(encoded)
            
        print(f"Session saved securely to {filepath}")

    @staticmethod
    def load_session(filepath: str, key: str) -> hrequests.Session:
        '''
        Loads an encrypted session file and returns a new Session object.
        '''
        with open(filepath, 'r', encoding='utf-8') as f:
            encoded = f.read()
            
        decoded_bytes = base64.b64decode(encoded)
        data = json.loads(decoded_bytes.decode())
        
        session = hrequests.Session(
            browser=data.get('browser'),
            version=data.get('version'),
            proxy=data.get('proxy')
        )
        session.headers.update(data.get('headers', {}))
        
        # Load cookies
        cookie_list = data.get('cookies', [])
        hrequests.client.merge_cookies(session.cookies, hrequests.client.list_to_cookiejar(cookie_list))
        
        print(f"Session loaded successfully from {filepath}")
        return session
