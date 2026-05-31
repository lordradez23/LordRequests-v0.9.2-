'''
WebRTC Leak Prevention.
Stops websites from finding your real IP through WebRTC tricks.
'''

class WebRTCHandler:
    '''
    Handles WebRTC spoofing so we don't leak our real IP or hardware IDs.
    '''
    @staticmethod
    def get_spoof_script(fake_ip: str = "127.0.0.1") -> str:
        '''
        Throws a JS snippet at the browser to mask our devices and filter out IPs in SDP.
        '''
        return f"""
        (function() {{
            // Fake the device list so they see generic hardware
            if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {{
                const originalEnumerate = navigator.mediaDevices.enumerateDevices;
                navigator.mediaDevices.enumerateDevices = function() {{
                    return Promise.resolve([
                        {{ kind: 'audioinput', label: 'Internal Microphone', deviceId: 'default' }},
                        {{ kind: 'videoinput', label: 'FaceTime HD Camera', deviceId: 'default' }}
                    ]);
                }};
            }}

            // Intercept createOffer/createAnswer to scrub out any real IPs
            const pc = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
            if (pc) {{
                const originalCreateOffer = pc.prototype.createOffer;
                pc.prototype.createOffer = function() {{
                    return originalCreateOffer.apply(this, arguments).then(offer => {{
                        // Swap out any IP address found in the SDP with our fake one
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
        Kills WebRTC entirely if we just don't want to deal with it.
        '''
        return """
        window.RTCPeerConnection = null;
        window.mozRTCPeerConnection = null;
        window.webkitRTCPeerConnection = null;
        """
