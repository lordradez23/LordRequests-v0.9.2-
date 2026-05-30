'''
Auto-Rotating Personas
~~~~~~~~~~~~~~~~~~~~~~

Integrated identity rotation with coordinated headers and fingerprints.
'''

import random
from typing import List, Dict, Any, Optional

class Persona:
    def __init__(self, name: str, user_agent: str, platform: str, screen_res: str):
        self.name = name
        self.user_agent = user_agent
        self.platform = platform
        self.screen_res = screen_res
        self.cookies: Dict[str, str] = {}

class PersonaManager:
    '''
    Manages a pool of high-trust browser personas.
    '''
    def __init__(self):
        self.pool: List[Persona] = []
        self._initialize_default_pool()

    def _initialize_default_pool(self):
        '''Creates a set of standard high-trust personas.'''
        self.pool = [
            Persona("Alex - Chrome/Win", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", "Win32", "1920x1080"),
            Persona("Sarah - Safari/Mac", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15", "MacIntel", "2560x1440"),
            Persona("James - Firefox/Linux", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0", "Linux x86_64", "1366x768")
        ]

    def get_random_persona(self) -> Persona:
        '''Returns a random persona from the pool.'''
        return random.choice(self.pool)

    def add_persona(self, name: str, user_agent: str, platform: str, screen_res: str):
        '''Manually add a custom persona.'''
        self.pool.append(Persona(name, user_agent, platform, screen_res))

    @staticmethod
    def get_coordinated_headers(persona: Persona) -> Dict[str, str]:
        '''
        Returns a set of request headers that are consistent with the persona.
        '''
        return {
            "User-Agent": persona.user_agent,
            "sec-ch-ua-platform": f'"{persona.platform.split()[0]}"',
            "Accept-Language": "en-US,en;q=0.9",
        }
