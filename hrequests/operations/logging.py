'''
Encrypted Log Storage
~~~~~~~~~~~~~~~~~~~~~

Secure AES-256 equivalent logging for sensitive traffic data.
'''

import os
import json
import base64
from typing import Any, Optional

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class EncryptedLogger:
    def __init__(self, filename: str, key: Optional[str] = None):
        self.filename = filename
        if CRYPTO_AVAILABLE:
            if not key:
                # Generate or load key
                key_file = filename + ".key"
                if os.path.exists(key_file):
                    with open(key_file, 'rb') as f:
                        self.key = f.read()
                else:
                    self.key = Fernet.generate_key()
                    with open(key_file, 'wb') as f:
                        f.write(self.key)
            else:
                self.key = key.encode() if isinstance(key, str) else key
            self.fernet = Fernet(self.key)
        else:
            self.key = None
            self.fernet = None

    def log(self, data: Any):
        '''Logs data securely.'''
        message = json.dumps(data).encode()
        
        if self.fernet:
            encrypted = self.fernet.encrypt(message)
        else:
            # Fallback for when cryptography is not available
            # Note: This is NOT secure, just a placeholder.
            encrypted = base64.b64encode(message)
            print("Warning: cryptography package not found. Logs are only Base64 encoded.")

        with open(self.filename, 'ab') as f:
            f.write(encrypted + b"\n")

    def read_logs(self) -> list:
        '''Decrypts and reads all logs.'''
        if not os.path.exists(self.filename):
            return []
        
        logs = []
        with open(self.filename, 'rb') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    if self.fernet:
                        decrypted = self.fernet.decrypt(line)
                    else:
                        decrypted = base64.b64decode(line)
                    logs.append(json.loads(decrypted))
                except Exception as e:
                    print(f"Error decrypting log line: {e}")
        return logs
