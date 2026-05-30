'''
Battery/Network API Spoofing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mocking device hardware state and network telemetry.
'''

import random

class TelemetrySpoofer:
    '''
    Injects mock telemetry data into the browser environment.
    '''
    @staticmethod
    def get_battery_script() -> str:
        '''
        Returns JS to spoof the Battery Status API.
        '''
        level = random.uniform(0.1, 1.0)
        charging = random.choice([True, False])
        return f"""
        (function() {{
            const battery = {{
                level: {level},
                charging: {charging},
                chargingTime: 0,
                dischargingTime: Infinity,
                addEventListener: () => {{}}
            }};
            navigator.getBattery = () => Promise.resolve(battery);
        }})();
        """

    @staticmethod
    def get_network_script() -> str:
        '''
        Returns JS to spoof the Network Information API.
        '''
        effective_type = random.choice(['4g', 'wifi', 'ethernet'])
        rtt = random.randint(20, 100)
        return f"""
        (function() {{
            const connection = {{
                effectiveType: '{effective_type}',
                rtt: {rtt},
                downlink: {random.uniform(1, 10)},
                saveData: false,
                addEventListener: () => {{}}
            }};
            navigator.connection = connection;
        }})();
        """
