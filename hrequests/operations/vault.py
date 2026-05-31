"""
Multi-Profile Identity Vault.
Safe spot to keep our encrypted "Legendary" identities and session profiles.
"""

import json
import base64
from typing import Dict, Optional
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    # We'll handle this later if they actually try to use the vault
    Fernet = None

class IdentityVault:
    '''
    Handles encrypted storage so we don't leak our browser profiles.
    '''
    def __init__(self, vault_path: str, secret_key: str):
        self.vault_path = vault_path
        self.key = self._derive_key(secret_key)
        if Fernet:
            self.cipher = Fernet(self.key)
        else:
            self.cipher = None

    def _derive_key(self, password: str) -> bytes:
        '''Turn a password into a real crypto key.'''
        if not Fernet:
            return b''
        salt = b'lordrequests_salt' # Should probably be random but keeping it simple for now
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def save_identity(self, name: str, profile_data: Dict):
        '''
        Encrypts a profile and sticks it in the vault file.
        '''
        if not self.cipher:
            raise ImportError("You need 'cryptography' installed to use the IdentityVault.")
            
        try:
            with open(self.vault_path, 'r') as f:
                vault = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            vault = {}

        # Encrypt the JSON data before saving
        encrypted_data = self.cipher.encrypt(json.dumps(profile_data).encode()).decode()
        vault[name] = encrypted_data
        
        with open(self.vault_path, 'w') as f:
            json.dump(vault, f)

    def load_identity(self, name: str) -> Optional[Dict]:
        '''
        Pulls a profile from the vault and decrypts it.
        '''
        if not self.cipher:
            raise ImportError("You need 'cryptography' installed to use the IdentityVault.")

        try:
            with open(self.vault_path, 'r') as f:
                vault = json.load(f)
            
            if name in vault:
                # Decrypt and turn back into a dict
                decrypted_bytes = self.cipher.decrypt(vault[name].encode())
                return json.loads(decrypted_bytes.decode())
        except Exception as e:
            print(f"[Vault] Failed to load identity {name}: {e}")
        return None
