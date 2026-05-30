'''
Detection Radar
~~~~~~~~~~~~~~~

Passive scanning of HTML for known anti-bot and tracking scripts.
'''

from typing import List, Dict
import re

class DetectionRadar:
    '''
    Identifies if a target site is using specific bot detection systems.
    '''
    SIGNATURES = {
        "Cloudflare": ["/cdn-cgi/challenge-platform/", "cf-browser-verification"],
        "DataDome": ["dd-captcha", "dd.collect.js"],
        "Akamai": ["akamai-bmp", "ak.privatemode"],
        "PerimeterX": ["perimeterx.js", "px-client"],
        "Google reCAPTCHA": ["google.com/recaptcha", "grecaptcha"]
    }

    def scan_html(self, html: str) -> Dict[str, bool]:
        '''
        Scans the provided HTML for anti-bot signatures.
        '''
        findings = {}
        for system, sigs in self.SIGNATURES.items():
            findings[system] = any(sig in html for sig in sigs)
        return findings

    def get_risk_assessment(self, html: str) -> str:
        '''
        Provides a risk assessment based on detected systems.
        '''
        results = self.scan_html(html)
        detected = [k for k, v in results.items() if v]
        
        if not detected:
            return "LOW: No major anti-bot systems detected. Light fingerprinting should suffice."
        
        return f"HIGH: Detected {', '.join(detected)}. Advanced TLS and browser emulation recommended."
