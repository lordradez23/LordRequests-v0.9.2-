'''
The "Ghost" Mode Protocol
~~~~~~~~~~~~~~~~~~~~~~~~~

A master switch that enables every stealth feature simultaneously
for maximum invisibility during high-stakes operations.
'''

from hrequests.networking.fingerprints import UnifiedFingerprinter
from hrequests.networking.webrtc import WebRTCHandler
from hrequests.networking.fonts import FontRandomizer
from hrequests.networking.devices import DeviceSpoofer
from hrequests.networking.navigator import NavigatorHider
from hrequests.networking.battery import BatterySpoofer
from hrequests.networking.screen import ScreenSync
from hrequests.operations.jitter import IntelligentJitter
from typing import Dict, List

class GhostProtocol:
    '''
    Orchestrates all stealth modules into a single "Ghost Mode".
    '''
    @staticmethod
    def get_stealth_scripts(os_type: str = 'win') -> List[str]:
        '''
        Returns a list of all JS payloads required for Ghost Mode.
        '''
        scripts = [
            UnifiedFingerprinter().get_unified_payload(),
            WebRTCHandler.get_spoof_script(),
            FontRandomizer.get_font_script(os_type),
            DeviceSpoofer.get_device_script(),
            NavigatorHider.get_navigator_script(os_type),
            BatterySpoofer.get_battery_script(),
            ScreenSync.get_screen_script()
        ]
        return scripts

    @staticmethod
    def enable(browser_session, persona: str = 'researcher'):
        '''
        Applies Ghost Mode to a BrowserSession.
        '''
        scripts = GhostProtocol.get_stealth_scripts()
        for script in scripts:
            browser_session.execute_script(script)
        
        # Apply intelligent jitter
        browser_session.jitter = IntelligentJitter(persona=persona)
        print("[LordRequests] Ghost Mode Protocol: FULLY ENGAGED.")
