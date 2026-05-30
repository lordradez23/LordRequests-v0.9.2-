'''
Cluster Mode
~~~~~~~~~~~~

Leader-Follower synchronization for distributed task execution.
'''

import os
import time
import threading
from typing import List, Dict, Any, Optional
import hrequests

class ScraperCluster:
    def __init__(self, role: str = 'worker', controller_url: Optional[str] = None):
        self.role = role
        self.controller_url = controller_url
        self.tasks: List[Dict[str, Any]] = []
        self.is_running = False

    def start(self):
        self.is_running = True
        if self.role == 'controller':
            self._run_controller()
        else:
            self._run_worker()

    def _run_controller(self):
        '''Runs as a task distributor.'''
        print("Scraper Cluster: Controller started on port 5000")
        # In a real implementation, we would use FastAPI here.
        # For this library, we'll simulate the task queue.
        while self.is_running:
            # Distribute tasks to workers who check in
            time.sleep(1)

    def _run_worker(self):
        '''Runs as a task consumer.'''
        print(f"Scraper Cluster: Worker checking in to {self.controller_url}")
        while self.is_running:
            # Poll controller for tasks
            # task = requests.get(f"{self.controller_url}/pop_task")
            # if task: execute(task)
            time.sleep(2)

    def add_task(self, method: str, url: str, **kwargs):
        '''Adds a task to the queue (Controller only).'''
        if self.role == 'controller':
            self.tasks.append({
                'method': method,
                'url': url,
                'kwargs': kwargs,
                'id': os.urandom(4).hex()
            })
            print(f"Task added: {url}")

    @staticmethod
    def deploy_workers(count: int = 3):
        '''Helper to spawn local worker threads for testing.'''
        for i in range(count):
            worker = ScraperCluster(role='worker', controller_url='http://localhost:5000')
            threading.Thread(target=worker.start, daemon=True).start()
        print(f"Spawned {count} local workers.")
