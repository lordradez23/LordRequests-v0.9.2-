'''
ARM-Architecture Proxy Sync
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optimizations and fingerprint adjustments for ARM-based proxy nodes.
'''

from typing import Dict

class ARMProxyBalancer:
    '''
    Manages and identifies ARM-based proxy infrastructure.
    '''
    @staticmethod
    def get_arm_headers() -> Dict[str, str]:
        '''
        Returns headers that align with ARM-based linux environments.
        '''
        return {
            "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "X-Node-Arch": "aarch64",
            "X-Hardware-Model": "Raspberry Pi 4 Model B"
        }

    @staticmethod
    def adjust_concurrency(base_threads: int) -> int:
        '''
        Adjusts thread count for lower-power ARM devices.
        '''
        return max(1, int(base_threads * 0.6))

    @staticmethod
    def is_arm_node(ua: str) -> bool:
        '''
        Checks if a user-agent indicates an ARM node.
        '''
        return "aarch64" in ua or "armv8" in ua or "armv7" in ua
