'''
The "Ghost" Mode Protocol.
Basically a big red button that turns on all our stealth toys at once 
so we don't get caught during heavy operations.
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
    Combines every stealth module into one "Ghost Mode" profile.
    '''
    @staticmethod
    def get_stealth_scripts(os_type: str = 'win') -> List[str]:
        '''
        Gathers all the JS payloads we need to keep the browser invisible.
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
        Actually sticks the ghost mode scripts into the session and sets up jitter.
        '''
        scripts = GhostProtocol.get_stealth_scripts()
        for script in scripts:
            browser_session.execute_script(script)
        
        # Add some human-like timing so we aren't behaving like a bot
        browser_session.jitter = IntelligentJitter(persona=persona)
        print("[LordRequests] Ghost Mode Protocol: ENGAGED.")
