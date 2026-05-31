'''
Unified Browser Fingerprinters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Merges Canvas, WebGL, and Audio fingerprints into a single synchronized identity
to defeat cross-attribute correlation in bot detection.
'''

import random
from typing import Dict

class UnifiedFingerprinter:
    '''
    Generates synchronized JS payloads for Canvas, WebGL, and Audio spoofing.
    '''
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
        self.vendor = "LordGraphics Engine"
        self.renderer = f"High-Resolution {random.choice(['Titan', 'Aries', 'Vortex'])} Shader"
        self.noise_factor = random.uniform(0.0001, 0.0005)

    def get_unified_payload(self) -> str:
        '''
        Returns a single combined JS snippet for all fingerprinting surfaces.
        '''
        return f"""
        (function() {{
            // --- Synchronized Canvas Spoofing ---
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function() {{
                const results = originalGetImageData.apply(this, arguments);
                for (let i = 0; i < results.data.length; i += 4) {{
                    results.data[i] = results.data[i] + (Math.random() < 0.5 ? 1 : -1);
                }}
                return results;
            }};

            // --- Synchronized WebGL Spoofing ---
            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return "{self.vendor}"; // UNMASKED_VENDOR_WEBGL
                if (parameter === 37446) return "{self.renderer}"; // UNMASKED_RENDERER_WEBGL
                return originalGetParameter.apply(this, arguments);
            }};

            // --- Synchronized Audio Spoofing ---
            const originalGetChannelData = AudioBuffer.prototype.getChannelData;
            AudioBuffer.prototype.getChannelData = function() {{
                const results = originalGetChannelData.apply(this, arguments);
                for (let i = 0; i < results.length; i++) {{
                    results[i] = results[i] + (Math.random() * {self.noise_factor});
                }}
                return results;
            }};

            console.log("[LordRequests] Unified Fingerprinting Payload Injected.");
        }})();
        """

    def get_config(self) -> Dict[str, str]:
        '''Returns the current identity configuration.'''
        return {
            "vendor": self.vendor,
            "renderer": self.renderer,
            "noise_factor": self.noise_factor
        }
