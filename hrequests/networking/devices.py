'''
Media Device Spoofing
~~~~~~~~~~~~~~~~~~~~~

Spoofing of hardware device IDs and labels (Camera, Microphone, Speakers)
to prevent identification via device enumeration.
'''

import random
from typing import List, Dict

class DeviceSpoofer:
    '''
    Generates realistic hardware device configurations for browser sessions.
    '''
    DEVICES = {
        'audioinput': [
            "Internal Microphone (Built-in)",
            "Realtek High Definition Audio",
            "Microphone (USB Audio Device)",
            "Logitech USB Headset"
        ],
        'videoinput': [
            "FaceTime HD Camera",
            "Integrated Webcam",
            "USB Video Device",
            "Logitech HD Pro Webcam C920"
        ],
        'audiooutput': [
            "Internal Speakers (Built-in)",
            "Realtek High Definition Audio (Speakers)",
            "Headphones (USB Audio Device)",
            "Dell Professional Sound Bar"
        ]
    }

    @staticmethod
    def get_device_script() -> str:
        '''
        Returns JS to spoof navigator.mediaDevices.enumerateDevices.
        '''
        selected_devices = []
        for kind, labels in DeviceSpoofer.DEVICES.items():
            # Pick 1-2 devices per kind
            for label in random.sample(labels, k=random.randint(1, min(2, len(labels)))):
                device_id = ''.join(random.choices('0123456789abcdef', k=64))
                group_id = ''.join(random.choices('0123456789abcdef', k=64))
                selected_devices.append({
                    "kind": kind,
                    "label": label,
                    "deviceId": device_id,
                    "groupId": group_id
                })

        return f"""
        (function() {{
            if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {{
                const spoofedDevices = {selected_devices};
                navigator.mediaDevices.enumerateDevices = function() {{
                    return Promise.resolve(spoofedDevices);
                }};
            }}
            console.log("[LordRequests] Media Devices Spoofed.");
        }})();
        """
