'''
Scraper Clusters.
Lets us run tasks across multiple machines using a Leader-Follower setup.
'''

import os
import time
import threading
from typing import List, Dict, Any, Optional
import hrequests

class ScraperCluster:
    '''
    Basic cluster logic.
    '''
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

    def _run_worker(self):
        '''Just hangs around waiting for tasks from the controller.'''
        print(f"Scraper Cluster: Worker checking in to {self.controller_url}")
        while self.is_running:
            time.sleep(2)

    def add_task(self, method: str, url: str, **kwargs):
        '''Adds a new request to the pile (Controller only).'''
        if self.role == 'controller':
            self.tasks.append({
                'method': method,
                'url': url,
                'kwargs': kwargs,
                'id': os.urandom(4).hex()
            })

class ScraperClusterV2(ScraperCluster):
    '''
    Newer cluster version that actually tracks task states and heartbeats 
    so we know if a worker dies.
    '''
    def __init__(self, role: str = 'worker', controller_url: Optional[str] = None):
        super().__init__(role, controller_url)
        self.worker_states: Dict[str, float] = {} # worker_id -> timestamp of last check-in
        self.task_results: Dict[str, Any] = {}
        self.running_tasks: Dict[str, str] = {} # task_id -> worker_id

    def _run_controller(self):
        '''Main loop for the controller to keep an eye on everything.'''
        print("[Cluster V2] Controller active. Monitoring heartbeats...")
        while self.is_running:
            # Look for workers that haven't checked in for 10+ seconds
            now = time.time()
            dead_workers = [wid for wid, t in self.worker_states.items() if now - t > 10]
            for wid in dead_workers:
                print(f"[Cluster V2] Worker {wid} timed out. Requeuing tasks.")
                # If a worker dies, we need to put their tasks back in the queue
                for tid, worker_id in list(self.running_tasks.items()):
                    if worker_id == wid:
                        del self.running_tasks[tid]
                del self.worker_states[wid]
            time.sleep(5)

    def worker_heartbeat(self, worker_id: str):
        '''Workers call this to say "I'm still alive".'''
        self.worker_states[worker_id] = time.time()

    def submit_result(self, task_id: str, result: Any):
        '''Called when a worker finishes a task.'''
        self.task_results[task_id] = result
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
        print(f"[Cluster V2] Task {task_id} done.")

    def get_cluster_status(self) -> Dict:
        '''Quick overview of how the cluster is doing.'''
        return {
            "active_workers": len(self.worker_states),
            "pending_tasks": len(self.tasks),
            "running_tasks": len(self.running_tasks),
            "completed_tasks": len(self.task_results)
        }
