'''
Native Cron Scheduler
~~~~~~~~~~~~~~~~~~~~~

Integrated task scheduling for periodic scraping operations.
'''

import time
import threading
from typing import Callable, List, Optional
import schedule # Requires 'schedule' library, but we can implement a basic one

class Task:
    def __init__(self, name: str, interval: int, func: Callable, *args, **kwargs):
        self.name = name
        self.interval = interval # seconds
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.last_run = 0
        self.is_running = False

class NativeScheduler:
    def __init__(self):
        self.tasks: List[Task] = []
        self._shutdown = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def add_task(self, name: str, interval: int, func: Callable, *args, **kwargs):
        task = Task(name, interval, func, *args, **kwargs)
        self.tasks.append(task)
        print(f"Scheduled task '{name}' every {interval}s")

    def _run(self):
        while not self._shutdown.is_set():
            now = time.time()
            for task in self.tasks:
                if now - task.last_run >= task.interval and not task.is_running:
                    task.is_running = True
                    # Run in a new thread so we don't block the scheduler
                    threading.Thread(target=self._execute_task, args=(task,)).start()
            time.sleep(1)

    def _execute_task(self, task: Task):
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Running scheduled task: {task.name}")
            task.func(*task.args, **task.kwargs)
        except Exception as e:
            print(f"Error in task '{task.name}': {e}")
        finally:
            task.last_run = time.time()
            task.is_running = False

    def start(self):
        if self._thread:
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("Scheduler started.")

    def stop(self):
        self._shutdown.set()
        if self._thread:
            self._thread.join()
            self._thread = None
        print("Scheduler stopped.")
