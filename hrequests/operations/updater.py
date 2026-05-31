'''
sidecar-cgo Auto-Updater
~~~~~~~~~~~~~~~~~~~~~~~~

Background checking and updating of the Go sidecar binary.
'''

import hrequests
import os
import hashlib
from typing import Optional

class SidecarUpdater:
    '''
    Checks for sidecar updates on GitHub and downloads the latest version if needed.
    '''
    REPO_URL = "https://api.github.com/repos/HMIDev/hrequests/releases/latest"

    def __init__(self, current_bin_path: str):
        self.bin_path = current_bin_path

    def check_for_updates(self) -> Optional[str]:
        '''
        Checks if a newer version is available.
        '''
        try:
            resp = hrequests.get(self.REPO_URL, timeout=5)
            if resp.status_code == 200:
                latest = resp.json()
                latest_ver = latest.get('tag_name', '')
                # Simplified version check: if current doesn't exist or we want latest
                return latest_ver
        except Exception as e:
            print(f"[Updater] Update check failed: {e}")
        return None

    def download_update(self, download_url: str):
        '''
        Downloads and replaces the current sidecar binary.
        '''
        print(f"[Updater] Downloading sidecar from {download_url}...")
        try:
            resp = hrequests.get(download_url, stream=True)
            if resp.status_code == 200:
                temp_path = self.bin_path + ".tmp"
                with open(temp_path, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Replace current binary
                if os.path.exists(self.bin_path):
                    os.remove(self.bin_path)
                os.rename(temp_path, self.bin_path)
                os.chmod(self.bin_path, 0o755)
                print("[Updater] Sidecar updated successfully.")
        except Exception as e:
            print(f"[Updater] Download failed: {e}")

    @staticmethod
    def get_file_hash(filepath: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
