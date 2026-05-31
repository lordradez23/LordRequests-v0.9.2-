'''
Unified Browser Fingerprinting.
Merges Canvas, WebGL, and Audio spoofing into one sync'd up identity 
so we don't get flagged for mismatched attributes.
'''

import random
from typing import Dict

class UnifiedFingerprinter:
    '''
    Handles the JS generation for our "identity" across different browser APIs.
    '''
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
        self.vendor = "LordGraphics Engine"
        self.renderer = f"High-Resolution {random.choice(['Titan', 'Aries', 'Vortex'])} Shader"
        self.noise_factor = random.uniform(0.0001, 0.0005)

    def get_unified_payload(self) -> str:
        '''
        Throws all the spoofing logic into a single JS blob we can inject.
        '''
        return f"""
        (function() {{
            // --- Fake Canvas data ---
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function() {{
                const results = originalGetImageData.apply(this, arguments);
                for (let i = 0; i < results.data.length; i += 4) {{
                    results.data[i] = results.data[i] + (Math.random() < 0.5 ? 1 : -1);
                }}
                return results;
            }};

            // --- Fake WebGL vendor/renderer ---
            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return "{self.vendor}"; // UNMASKED_VENDOR_WEBGL
                if (parameter === 37446) return "{self.renderer}"; // UNMASKED_RENDERER_WEBGL
                return originalGetParameter.apply(this, arguments);
            }};

            // --- Tiny noise in audio to throw off fingerprinting ---
            const originalGetChannelData = AudioBuffer.prototype.getChannelData;
            AudioBuffer.prototype.getChannelData = function() {{
                const results = originalGetChannelData.apply(this, arguments);
                for (let i = 0; i < results.length; i++) {{
                    results[i] = results[i] + (Math.random() * {self.noise_factor});
                }}
                return results;
            }};

            console.log("[LordRequests] Fingerprinting payload injected.");
        }})();
        """

    def get_config(self) -> Dict[str, str]:
        '''Just returns what we're currently spoofing.'''
        return {
            "vendor": self.vendor,
            "renderer": self.renderer,
            "noise_factor": self.noise_factor
        }
