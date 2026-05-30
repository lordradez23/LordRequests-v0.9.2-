'''
Persona Jitter
~~~~~~~~~~~~~~

Implements human-like request timing to mimic specific user personas.
'''

import time
import random

class Jitter:
    PERSONAS = {
        'casual': (1.5, 5.0),    # Slow, readable pace
        'researcher': (0.5, 2.0), # Efficient but human
        'aggressive': (0.1, 0.5), # Fast automated pace
        'bot': (0, 0)             # No jitter
    }

    def __init__(self, persona: str = 'researcher'):
        self.min_delay, self.max_delay = self.PERSONAS.get(persona, self.PERSONAS['researcher'])

    def wait(self):
        '''
        Waits for a random amount of time based on the active persona.
        '''
        if self.max_delay == 0:
            return
        
        delay = random.uniform(self.min_delay, self.max_delay)
        # Add a "micro-jitter" to make it even less predictable
        delay += random.uniform(-0.05, 0.05)
        
        if delay > 0:
            time.sleep(max(0, delay))

    @classmethod
    def apply(cls, persona: str):
        '''
        Helper to wait immediately for a persona.
        '''
        cls(persona).wait()
