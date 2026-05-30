'''
WebSocket Stream Interceptor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Real-time monitoring and logging of WebSocket traffic.
'''

import time
from typing import Callable, Optional

try:
    import websockets
    import asyncio
    WS_AVAILABLE = True
except ImportError:
    WS_AVAILABLE = False

class WSInterceptor:
    '''
    Connects to a WebSocket stream and intercepts messages.
    '''
    def __init__(self, url: str):
        self.url = url
        self.active = False

    async def listen(self, callback: Callable[[str], None], duration: Optional[int] = None):
        '''
        Listens to the stream and passes messages to the callback.
        '''
        if not WS_AVAILABLE:
            print("WebSocket Error: 'websockets' and 'asyncio' are required.")
            return

        print(f"Connecting to WebSocket: {self.url}")
        start_time = time.time()
        
        async with websockets.connect(self.url) as ws:
            self.active = True
            while self.active:
                if duration and (time.time() - start_time) > duration:
                    break
                
                try:
                    message = await ws.recv()
                    callback(message)
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed by host.")
                    break

    def stop(self):
        self.active = False
