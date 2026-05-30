'''
DPI Evasion Profiler
~~~~~~~~~~~~~~~~~~~~

Configuration suggestor for low-level packet evasion (TTL, Window Size).
'''

from typing import Dict

class DPIProfiler:
    '''
    Suggests TCP/IP stack parameters to match OS-specific network signatures.
    '''
    OS_SIGNATURES = {
        "Windows 10/11": {
            "ttl": 128,
            "window_size": 64240,
            "scale_factor": 8
        },
        "Linux (Ubuntu/Debian)": {
            "ttl": 64,
            "window_size": 29200,
            "scale_factor": 7
        },
        "macOS (Sonoma)": {
            "ttl": 64,
            "window_size": 65535,
            "scale_factor": 3
        }
    }

    @staticmethod
    def get_profile(os_name: str) -> Dict[str, int]:
        '''
        Returns the network profile for a given OS.
        '''
        return DPIProfiler.OS_SIGNATURES.get(os_name, DPIProfiler.OS_SIGNATURES["Windows 10/11"])

    @staticmethod
    def get_evasion_report(os_name: str) -> str:
        '''
        Generates a summary of evasion parameters to be applied at the OS level.
        '''
        p = DPIProfiler.get_profile(os_name)
        return (
            f"--- DPI Evasion Profile: {os_name} ---\n"
            f"Suggested TTL: {p['ttl']}\n"
            f"Suggested TCP Window: {p['window_size']}\n"
            f"Window Scale Factor: {p['scale_factor']}\n"
            "Apply via sysctl (Linux/macOS) or Registry (Windows) for absolute stealth."
        )
