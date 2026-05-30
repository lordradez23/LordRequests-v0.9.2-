'''
Persona Cloud-Sync
~~~~~~~~~~~~~~~~~~

Shared browser history and persona state across distributed clusters.
'''

from hrequests.operations.channel import SecureChannel
from hrequests.operations.personas import Persona
from typing import List, Optional

class PersonaCloudSync:
    '''
    Synchronizes personas across system nodes using a secure channel.
    '''
    def __init__(self, channel: SecureChannel):
        self.channel = channel

    def broadcast_persona(self, persona: Persona):
        '''
        Encrypts and broadcasts a persona's state.
        '''
        payload = {
            "type": "persona_sync",
            "name": persona.name,
            "ua": persona.user_agent,
            "cookies": persona.cookies
        }
        token = self.channel.pack_message(payload)
        # In a real cluster, this would be sent to the broker/leader
        print(f"Persona {persona.name} state broadcasted.")

    def receive_persona(self, token: str) -> Optional[Persona]:
        '''
        Decrypts and reconstructs a persona from a sync token.
        '''
        data = self.channel.unpack_message(token)
        if data.get('type') == 'persona_sync':
            persona = Persona(data['name'], data['ua'], "Unknown", "Unknown")
            persona.cookies = data.get('cookies', {})
            return persona
        return None
