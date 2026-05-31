'''
Battery Status Spoofing
~~~~~~~~~~~~~~~~~~~~~~~

Mocking of battery levels and charging states to defeat status-based tracking.
'''

import random

class BatterySpoofer:
    '''
    Generates JS to mock navigator.getBattery function.
    '''
    @staticmethod
    def get_battery_script() -> str:
        '''
        Returns JS to spoof battery status details.
        '''
        level = random.uniform(0.1, 1.0)
        charging = random.choice([True, False])
        charging_time = 0 if charging else float('inf')
        discharging_time = float('inf') if charging else random.randint(3600, 14400)

        return f"""
        (function() {{
            if (navigator.getBattery) {{
                const originalGetBattery = navigator.getBattery;
                navigator.getBattery = function() {{
                    return Promise.resolve({{
                        level: {level},
                        charging: {charging},
                        chargingTime: {charging_time},
                        dischargingTime: {discharging_time},
                        addEventListener: function() {{}},
                        removeEventListener: function() {{}},
                        onlevelchange: null,
                        onchargingchange: null,
                        onchargingtimechange: null,
                        ondischargingtimechange: null
                    }});
                }};
            }}
            console.log("[LordRequests] Battery Status Spoofed.");
        }})();
        """
