'''
Zombie-Node Detection
~~~~~~~~~~~~~~~~~~~~~

Identifying and quarantining unresponsive cluster worker nodes.
'''

import time
from typing import Dict, List, Optional

class ZombieDetector:
    '''
    Monitors cluster nodes for unresponsive (zombie) behavior.
    '''
    def __init__(self, timeout_s: float = 30.0):
        self.timeout = timeout_s
        self.nodes: Dict[str, float] = {}  # node_id -> last_heartbeat

    def register_node(self, node_id: str):
        '''Registers a new node and records its initial heartbeat.'''
        self.nodes[node_id] = time.time()
        print(f"Node {node_id} registered.")

    def heartbeat(self, node_id: str):
        '''Updates the heartbeat timestamp for a given node.'''
        if node_id in self.nodes:
            self.nodes[node_id] = time.time()

    def get_zombie_nodes(self) -> List[str]:
        '''
        Returns a list of node IDs that have not sent a heartbeat in time.
        '''
        now = time.time()
        return [
            node_id for node_id, last_beat in self.nodes.items()
            if (now - last_beat) > self.timeout
        ]

    def quarantine(self, node_id: str) -> bool:
        '''Removes a zombie node from the active pool.'''
        if node_id in self.nodes:
            del self.nodes[node_id]
            print(f"Node {node_id} quarantined.")
            return True
        return False
