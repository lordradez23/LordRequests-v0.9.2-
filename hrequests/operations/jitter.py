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
        if delay > 0:
            time.sleep(max(0, delay))

class IntelligentJitter(Jitter):
    '''
    Context-aware jitter that adapts to time-of-day habits.
    '''
    HEURISTICS = {
        'workday': {
            'peak_times': [9, 10, 11, 13, 14, 15, 16], # 9am-5pm except lunch
            'slow_times': [12, 17, 18],              # Lunch and end of day
            'base_multiplier': 1.0,
            'slow_multiplier': 2.5
        },
        'nightowl': {
            'peak_times': [22, 23, 0, 1, 2],         # Late night activity
            'slow_times': [10, 11, 12, 13, 14, 15],  # Morning/Afternoon sleep
            'base_multiplier': 0.8,                  # Faster at night
            'slow_multiplier': 3.0
        }
    }

    def __init__(self, persona: str = 'researcher', heuristic: str = 'workday'):
        super().__init__(persona)
        self.heuristic = self.HEURISTICS.get(heuristic, self.HEURISTICS['workday'])

    def get_context_delay(self) -> float:
        '''
        Calculates delay with heuristic modifiers.
        '''
        import datetime
        current_hour = datetime.datetime.now().hour
        
        delay = random.uniform(self.min_delay, self.max_delay)
        
        if current_hour in self.heuristic['peak_times']:
            delay *= self.heuristic['base_multiplier']
        elif current_hour in self.heuristic['slow_times']:
            delay *= self.heuristic['slow_multiplier']
        else:
            delay *= 1.5 # Neutral time
            
        return max(0, delay)

    def wait(self):
        delay = self.get_context_delay()
        if delay > 0:
            time.sleep(delay)
