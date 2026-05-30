'''
Session-Identity Generator
~~~~~~~~~~~~~~~~~~~~~~~~~~

Generates realistic fake identities for automated form-filling 
and persona-based browsing.
'''

import random
from typing import Dict

class PersonaGenerator:
    FIRST_NAMES = ['Aiden', 'Sophia', 'Jackson', 'Olivia', 'Lucas', 'Emma', 'Liam', 'Mia']
    LAST_NAMES = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Miller', 'Wilson', 'Moore', 'Anderson']
    DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com']

    @classmethod
    def generate(cls) -> Dict[str, str]:
        '''
        Returns a dictionary containing a complete fake identity.
        '''
        first = random.choice(cls.FIRST_NAMES)
        last = random.choice(cls.LAST_NAMES)
        username = f"{first.lower()}_{last.lower()}{random.randint(10, 99)}"
        domain = random.choice(cls.DOMAINS)
        
        return {
            'first_name': first,
            'last_name': last,
            'full_name': f"{first} {last}",
            'username': username,
            'email': f"{username}@{domain}",
            'bio': f"Digital nomad and {random.choice(['tech', 'coffee', 'travel', 'art'])} enthusiast.",
            'password': f"SafePass!{random.randint(1000, 9999)}"
        }
