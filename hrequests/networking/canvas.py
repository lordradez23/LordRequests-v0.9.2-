'''
Canvas/WebGL Noise Injection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hardware fingerprint randomization through graphic operation noise.
'''

class CanvasSpoofer:
    '''
    Injects noise into graphic rendering operations to defeat fingerprinting.
    '''
    @staticmethod
    def get_canvas_script() -> str:
        '''
        Returns a JavaScript snippet to add noise to Canvas rendering.
        '''
        return """
        (function() {
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function() {
                const results = originalGetImageData.apply(this, arguments);
                for (let i = 0; i < results.data.length; i += 4) {
                    results.data[i] = results.data[i] + (Math.random() < 0.5 ? 1 : -1);
                }
                return results;
            };
        })();
        """

    @staticmethod
    def get_webgl_script() -> str:
        '''
        Returns a JavaScript snippet to spoof WebGL parameters.
        '''
        return """
        (function() {
            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return "LordGraphics Inc."; // UNMASKED_VENDOR_WEBGL
                if (parameter === 37446) return "LordRequests High-Fidelity Engine"; // UNMASKED_RENDERER_WEBGL
                return originalGetParameter.apply(this, arguments);
            };
        })();
        """
