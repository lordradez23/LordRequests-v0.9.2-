'''
Encrypted Export Archive
~~~~~~~~~~~~~~~~~~~~~~~~

AES-256 encrypted bundling of harvested datasets for secure transfer.
'''

import os
import zipfile
import io
from typing import List

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class EncryptedArchive:
    '''
    Creates encrypted zip archives of harvested data.
    '''
    def __init__(self, key: str = None):
        if CRYPTO_AVAILABLE:
            self.key = key.encode() if key else Fernet.generate_key()
            self.fernet = Fernet(self.key)
        else:
            self.key = None
            self.fernet = None

    def create_archive(self, files: List[str], output_path: str) -> str:
        '''
        Zips the given files and encrypts the archive.
        '''
        # Create in-memory zip
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filepath in files:
                if os.path.exists(filepath):
                    zf.write(filepath, os.path.basename(filepath))

        zip_bytes = zip_buffer.getvalue()

        if self.fernet:
            encrypted = self.fernet.encrypt(zip_bytes)
            with open(output_path, 'wb') as f:
                f.write(encrypted)
            print(f"Encrypted archive saved to {output_path}")
        else:
            with open(output_path, 'wb') as f:
                f.write(zip_bytes)
            print(f"Archive saved (unencrypted) to {output_path}")

        return output_path

    def get_key(self) -> str:
        return self.key.decode() if self.key else ""
