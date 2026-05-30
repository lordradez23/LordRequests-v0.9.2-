'''
Push Notification Listener
~~~~~~~~~~~~~~~~~~~~~~~~~~

Capturing and logging Firebase/OneSignal push signals for mobile workflow analysis.
'''

from typing import Dict, Any, Callable, List

class PushListener:
    '''
    Simulates a mobile app's push notification listener.
    '''
    def __init__(self):
        self.received_notifications: List[Dict[str, Any]] = []

    def mock_receive(self, payload: Dict[str, Any], callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        '''
        Simulates the arrival of a push notification.
        '''
        print(f"Push received: {payload.get('title', 'No Title')}")
        self.received_notifications.append(payload)
        if callback:
            callback(payload)

    def get_otp_from_push(self) -> Optional[str]:
        '''
        Heuristic to find an OTP in the most recent received notification.
        '''
        if not self.received_notifications:
            return None
            
        body = self.received_notifications[-1].get('body', '')
        # Simple regex for 4-6 digit numeric OTP
        import re
        match = re.search(r'\b\d{4,6}\b', body)
        return match.group(0) if match else None
