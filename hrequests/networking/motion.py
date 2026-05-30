'''
Accelerator/Gyro Telemetry
~~~~~~~~~~~~~~~~~~~~~~~~~~

Spoofing device rotation and movement data for high-fidelity mobile simulation.
'''

import random

class MotionSpoofer:
    '''
    Injects mock motion and orientation data into the browser environment.
    '''
    @staticmethod
    def get_orientation_script() -> str:
        '''
        Returns JS to spoof DeviceOrientation events.
        '''
        alpha = random.uniform(0, 360)
        beta = random.uniform(-180, 180)
        gamma = random.uniform(-90, 90)
        return f"""
        (function() {{
            const event = new DeviceOrientationEvent('deviceorientation', {{
                alpha: {alpha},
                beta: {beta},
                gamma: {gamma},
                absolute: true
            }});
            window.dispatchEvent(event);
        }})();
        """

    @staticmethod
    def get_motion_script() -> str:
        '''
        Returns JS to spoof DeviceMotionEvent data.
        '''
        accel = random.uniform(0.1, 2.0)
        return f"""
        (function() {{
            const event = new DeviceMotionEvent('devicemotion', {{
                acceleration: {{x: {accel}, y: {accel}, z: {accel}}},
                accelerationIncludingGravity: {{x: {accel}, y: {accel+9.8}, z: {accel}}},
                rotationRate: {{alpha: 0, beta: 0, gamma: 0}},
                interval: 16
            }});
            window.dispatchEvent(event);
        }})();
        """
