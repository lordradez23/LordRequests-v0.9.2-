'''
Touch-Profile Randomizer
~~~~~~~~~~~~~~~~~~~~~~~

Simulation of varied screen-touch coordinates and movement patterns.
'''

import random
from typing import List, Tuple

class TouchSimulator:
    '''
    Generates realistic touch-event paths.
    '''
    def __init__(self, screen_res: Tuple[int, int] = (1080, 1920)):
        self.width, self.height = screen_res

    def generate_tap(self) -> Tuple[int, int]:
        '''Generates a single tap coordinate.'''
        return (random.randint(0, self.width), random.randint(0, self.height))

    def generate_swipe(self, length: int = 5) -> List[Tuple[int, int]]:
        '''
        Generates a sequence of coordinates for a swipe movement.
        '''
        start_x = random.randint(100, self.width - 100)
        start_y = random.randint(100, self.height - 100)
        
        path = [(start_x, start_y)]
        curr_x, curr_y = start_x, start_y
        
        for _ in range(length):
            curr_x += random.randint(-50, 50)
            curr_y += random.randint(100, 300) # Vertical swipe bias
            path.append((curr_x, curr_y))
            
        return path

    @staticmethod
    def get_touch_headers() -> Dict[str, str]:
        '''Returns headers that indicate touch capability.'''
        return {
            "sec-ch-ua-mobile": "?1",
            "Touch-Events": "enabled"
        }
