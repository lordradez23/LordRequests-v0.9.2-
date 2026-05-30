'''
Delta-Data Engine
~~~~~~~~~~~~~~~~~

Comparison logic for identifying changes between scraping runs.
'''

import json
from typing import Dict, Any, List, Optional

class DeltaEngine:
    '''
    Finds the difference between two data sets.
    '''
    @staticmethod
    def compare(old_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Compares two dictionaries and returns the delta.
        '''
        delta = {
            "added": {},
            "modified": {},
            "deleted": []
        }
        
        # Check for added and modified
        for key, val in new_data.items():
            if key not in old_data:
                delta["added"][key] = val
            elif old_data[key] != val:
                delta["modified"][key] = {
                    "from": old_data[key],
                    "to": val
                }
                
        # Check for deleted
        for key in old_data:
            if key not in new_data:
                delta["deleted"].append(key)
                
        return delta

    @staticmethod
    def has_changed(old_data: Dict[str, Any], new_data: Dict[str, Any]) -> bool:
        '''
        Returns True if the data has changed meaningfully.
        '''
        diff = DeltaEngine.compare(old_data, new_data)
        return bool(diff["added"] or diff["modified"] or diff["deleted"])
