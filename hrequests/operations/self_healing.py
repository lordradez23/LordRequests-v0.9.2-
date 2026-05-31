'''
Self-Healing Session Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatically detects stale/broken sessions and recreates them.
'''

import time
from typing import Optional, Callable
import hrequests

class SelfHealingSession:
    '''
    Wraps an hrequests session with automatic recovery logic.
    '''
    def __init__(self, browser: str = 'chrome', max_age_s: int = 300):
        self.browser = browser
        self.max_age_s = max_age_s
        self._session: Optional[hrequests.Session] = None
        self._created_at: float = 0

    def _is_stale(self) -> bool:
        if self._session is None:
            return True
        return (time.time() - self._created_at) > self.max_age_s

    def _heal(self):
        '''Closes old session and spawns a fresh one.'''
        if self._session:
            try:
                self._session.close()
            except Exception:
                pass
        print("Self-healing: spawning new session...")
        self._session = hrequests.Session(browser=self.browser)
        self._created_at = time.time()

    @property
    def session(self) -> hrequests.Session:
        if self._is_stale():
            self._heal()
        return self._session

    def get(self, url: str, **kwargs):
        '''Performs a GET request, auto-healing if the session is stale.'''
        return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs):
        '''Performs a POST request, auto-healing if the session is stale.'''
        return self.session.post(url, **kwargs)
