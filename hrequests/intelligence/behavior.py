'''
Autonomous Behavioral Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Heuristic monitoring to predict and avoid bot detection thresholds.
'''

import time
from collections import deque
from typing import Dict, List

class BehavioralAnalyzer:
    '''
    Monitors request patterns and analyzes response signals for detection risk.
    '''
    def __init__(self, window_size: int = 50):
        self.history = deque(maxlen=window_size)
        self.detection_signals = ['403', '429', 'captcha', 'forbidden', 'challenge']
        self.risk_score = 0.0

    def record_request(self, url: str, status_code: int, response_text: str):
        '''
        Records a completed request and updates risk heuristics.
        '''
        entry = {
            'timestamp': time.time(),
            'url': url,
            'status': str(status_code),
            'signals': [s for s in self.detection_signals if s in response_text.lower() or s == str(status_code)]
        }
        self.history.append(entry)
        self._calculate_risk()

    def _calculate_risk(self):
        '''
        Calculates a risk score (0.0 to 1.0) based on recent failures and patterns.
        '''
        if not self.history:
            self.risk_score = 0.0
            return

        failure_count = sum(1 for e in self.history if e['signals'])
        frequency = len(self.history) / (self.history[-1]['timestamp'] - self.history[0]['timestamp'] + 0.1)
        
        # Risk increases with failures and high frequency
        self.risk_score = min(1.0, (failure_count / len(self.history)) * 2)
        
    def get_recommendation(self) -> str:
        '''
        Provides an action recommendation based on current risk.
        '''
        if self.risk_score > 0.8:
            return "CRITICAL: Immediate Pivot to Browser sessions or high-trust proxies required."
        elif self.risk_score > 0.5:
            return "WARNING: Elevated risk. Increase jitter and randomize User-Agents."
        return "STABLE: Behavioral patterns within safe limits."

    def clear(self):
        self.history.clear()
        self.risk_score = 0.0
