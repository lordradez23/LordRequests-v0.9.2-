'''
Traffic Replay Engine
~~~~~~~~~~~~~~~~~~~~~

Records and replays sequences of HTTP requests.
'''

import time
from typing import List, Dict, Any, Optional
import hrequests

class TrafficReplayEngine:
    def __init__(self, session: Optional[hrequests.Session] = None):
        self.session = session or hrequests.Session()
        self.history: List[Dict[str, Any]] = []
        self.is_recording = False

    def start_recording(self):
        '''Starts recording requests.'''
        self.history = []
        self.is_recording = True

    def stop_recording(self):
        '''Stops recording requests.'''
        self.is_recording = False

    def record_request(self, method: str, url: str, **kwargs):
        '''Manually record a request or hook into session.'''
        if self.is_recording:
            self.history.append({
                'method': method,
                'url': url,
                'kwargs': kwargs,
                'timestamp': time.time()
            })

    def replay(self, speed_multiplier: float = 1.0):
        '''Replays the recorded history.'''
        if not self.history:
            return

        start_time = self.history[0]['timestamp']
        
        for i, entry in enumerate(self.history):
            if i > 0:
                # Wait for the relative delay
                delay = (entry['timestamp'] - self.history[i-1]['timestamp']) / speed_multiplier
                if delay > 0:
                    time.sleep(delay)
            
            method = entry['method'].lower()
            func = getattr(self.session, method)
            print(f"Replaying: {method.upper()} {entry['url']}")
            func(entry['url'], **entry['kwargs'])

    def export_script(self, filename: str):
        '''Exports the history as a standalone Python script.'''
        with open(filename, 'w') as f:
            f.write("import hrequests\n")
            f.write("import time\n\n")
            f.write("session = hrequests.Session()\n\n")
            
            for i, entry in enumerate(self.history):
                if i > 0:
                    delay = entry['timestamp'] - self.history[i-1]['timestamp']
                    f.write(f"time.sleep({delay:.4f})\n")
                
                f.write(f"session.{entry['method'].lower()}('{entry['url']}', **{entry['kwargs']})\n")
