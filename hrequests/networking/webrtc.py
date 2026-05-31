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
    def get_spoof_script(fake_ip: str = "127.0.0.1") -> str:
        '''
        Returns a JavaScript snippet to spoof WebRTC IP enumerations and device lists.
        '''
        return f"""
        (function() {{
            // Block device enumeration to prevent leak via hardware IDs
            if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {{
                const originalEnumerate = navigator.mediaDevices.enumerateDevices;
                navigator.mediaDevices.enumerateDevices = function() {{
                    return Promise.resolve([
                        {{ kind: 'audioinput', label: 'Internal Microphone', deviceId: 'default' }},
                        {{ kind: 'videoinput', label: 'FaceTime HD Camera', deviceId: 'default' }}
                    ]);
                }};
            }}

            // SDP IP Filtering
            const pc = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
            if (pc) {{
                const originalCreateOffer = pc.prototype.createOffer;
                pc.prototype.createOffer = function() {{
                    return originalCreateOffer.apply(this, arguments).then(offer => {{
                        // Replace any potential real IP with the fake one (or a loopback)
                        offer.sdp = offer.sdp.replace(/([0-9]{{1,3}}(\\.[0-9]{{1,3}}){{3}})/g, "{fake_ip}");
                        return offer;
                    }});
                }};

                const originalCreateAnswer = pc.prototype.createAnswer;
                pc.prototype.createAnswer = function() {{
                    return originalCreateAnswer.apply(this, arguments).then(answer => {{
                        answer.sdp = answer.sdp.replace(/([0-9]{{1,3}}(\\.[0-9]{{1,3}}){{3}})/g, "{fake_ip}");
                        return answer;
                    }});
                }};
            }}
            console.log("[LordRequests] WebRTC Shield Active.");
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
