'''
Encrypted Side-Channel
~~~~~~~~~~~~~~~~~~~~~~

Secure communication channel for worker-node metadata sharing.
'''

import json
import base64
from typing import Dict, Any, Optional

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class SecureChannel:
    '''
    Handles encrypted message passing between system components.
    '''
    def __init__(self, key: Optional[str] = None):
        if not CRYPTO_AVAILABLE:
            self.key = None
            self.fernet = None
        else:
            self.key = key.encode() if key else Fernet.generate_key()
            self.fernet = Fernet(self.key)

    def pack_message(self, data: Dict[str, Any]) -> str:
        '''
        Encrypts and encodes a message.
        '''
        message = json.dumps(data).encode()
        if self.fernet:
            return self.fernet.encrypt(message).decode()
        return base64.b64encode(message).decode() # Fallback

    def unpack_message(self, token: str) -> Dict[str, Any]:
        '''
        Decrypts and decodes a message.
        '''
        try:
            if self.fernet:
                decrypted = self.fernet.decrypt(token.encode())
            else:
                decrypted = base64.b64decode(token.encode())
            return json.loads(decrypted)
        except Exception as e:
            return {"error": f"Failed to decrypt message: {str(e)}"}

    def get_key(self) -> str:
        '''Returns the current encryption key.'''
        return self.key.decode() if self.key else ""
