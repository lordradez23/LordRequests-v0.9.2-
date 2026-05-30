'''
WebRTC Leak Prevention
~~~~~~~~~~~~~~~~~~~~~~

Spoofing and blocking of WebRTC-based IP leakage.
'''

class WebRTCHandler:
    '''
    Manages WebRTC configurations for browser-based sessions.
    '''
    @staticmethod
    def get_spoof_script(fake_ip: str = "192.168.1.100") -> str:
        '''
        Returns a JavaScript snippet to spoof WebRTC IP enumerations.
        '''
        return f"""
        (function() {{
            const pc = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
            if (pc) {{
                const originalCreateOffer = pc.prototype.createOffer;
                pc.prototype.createOffer = function() {{
                    return originalCreateOffer.apply(this, arguments).then(offer => {{
                        offer.sdp = offer.sdp.replace(/([0-9]{{1,3}}(\\.[0-9]{{1,3}}){{3}})/g, "{fake_ip}");
                        return offer;
                    }});
                }};
            }}
        }})();
        """

    @staticmethod
    def get_block_script() -> str:
        '''
        Returns a JavaScript snippet to completely disable WebRTC.
        '''
        return """
        window.RTCPeerConnection = null;
        window.mozRTCPeerConnection = null;
        window.webkitRTCPeerConnection = null;
        """
