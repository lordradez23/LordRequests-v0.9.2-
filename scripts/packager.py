'''
Multi-OS Cross-Packager
~~~~~~~~~~~~~~~~~~~~~~~

One-click bundling of scripts with the appropriate sidecar for all OSs.
'''

import os
import shutil
import zipfile
from typing import List

class CrossPackager:
    '''
    Bundles hrequests and the user script into a portable zip.
    '''
    def __init__(self, script_path: str, output_dir: str = "dist"):
        self.script_path = script_path
        self.output_dir = output_dir

    def package_for_all(self):
        '''
        Creates zip files for Windows, Mac, and Linux.
        '''
        platforms = ['win', 'mac', 'lin']
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for plat in platforms:
            self._create_bundle(plat)

    def _create_bundle(self, platform: str):
        bundle_name = f"lordrequests_bundle_{platform}.zip"
        bundle_path = os.path.join(self.output_dir, bundle_name)
        
        print(f"[Packager] Bundling for {platform} -> {bundle_name}")
        
        with zipfile.ZipFile(bundle_path, 'w') as zipf:
            # Add user script
            zipf.write(self.script_path, os.path.basename(self.script_path))
            
            # Add hrequests library (recursive)
            hreq_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for root, dirs, files in os.walk(os.path.join(hreq_path, 'hrequests')):
                for file in files:
                    if not file.endswith('.pyc'):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, hreq_path)
                        zipf.write(file_path, rel_path)
            
            # Note: In a real implementation, we would download the correct sidecar 
            # for the platform and add it to the zip.
            print(f"[Packager] Added hrequests library to {platform} bundle.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        p = CrossPackager(sys.argv[1])
        p.package_for_all()
