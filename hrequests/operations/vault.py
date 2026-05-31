'''
Multi-Profile Identity Vault
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Encrypted storage for "Legendary" identities and session profiles
to maintain reputation and historical consistency.
'''

import json
import base64
from typing import Dict, Optional
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    # Fallback or alert user
    Fernet = None

class IdentityVault:
    '''
    Manages encrypted storage for user identities and browser profiles.
    '''
    def __init__(self, vault_path: str, secret_key: str):
        self.vault_path = vault_path
        self.key = self._derive_key(secret_key)
        if Fernet:
            self.cipher = Fernet(self.key)
        else:
            self.cipher = None

    def _derive_key(self, password: str) -> bytes:
        '''Derives a cryptographic key from a password.'''
        if not Fernet:
            return b''
        salt = b'lordrequests_salt' # Fixed salt for simplicity in this version
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def save_identity(self, name: str, profile_data: Dict):
        '''
        Encrypts and saves a profile to the vault.
        '''
        if not self.cipher:
            raise ImportError("cryptography library required for IdentityVault")
            
        try:
            with open(self.vault_path, 'r') as f:
                vault = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            vault = {}

        encrypted_data = self.cipher.encrypt(json.dumps(profile_data).encode()).decode()
        vault[name] = encrypted_data
        
        with open(self.vault_path, 'w') as f:
            json.dump(vault, f)

    def load_identity(self, name: str) -> Optional[Dict]:
        '''
        Loads and decrypts a profile from the vault.
        '''
        if not self.cipher:
            raise ImportError("cryptography library required for IdentityVault")

        try:
            with open(self.vault_path, 'r') as f:
                vault = json.load(f)
            
            if name in vault:
                decrypted_bytes = self.cipher.decrypt(vault[name].encode())
                return json.loads(decrypted_bytes.decode())
        except Exception as e:
            print(f"[Vault] Failed to load identity {name}: {e}")
        return None
