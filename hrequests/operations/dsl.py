'''
Dynamic Scraper DSL
~~~~~~~~~~~~~~~~~~~

Domain Specific Language for defining scraping tasks in a declarative format.
'''

import json
import yaml
from typing import Dict, Any, List
import hrequests

class ScraperDSL:
    '''
    Executes tasks based on a YAML/JSON definition.
    '''
    def __init__(self, definition: str, format: str = 'yaml'):
        if format == 'yaml':
            self.task = yaml.safe_load(definition)
        else:
            self.task = json.loads(definition)

    def run(self):
        '''
        Executes the steps defined in the DSL.
        '''
        print(f"Executing DSL Task: {self.task.get('name', 'Unnamed Task')}")
        
        steps = self.task.get('steps', [])
        context = {}
        
        for step in steps:
            action = step.get('action')
            if action == 'get':
                url = step.get('url')
                print(f"  Fetching {url}...")
                resp = hrequests.get(url, **step.get('params', {}))
                context['last_response'] = resp
            elif action == 'extract':
                selector = step.get('selector')
                # Simple placeholder for extraction logic
                print(f"  Extracting with selector: {selector}")
            elif action == 'save':
                filename = step.get('filename')
                print(f"  Saving results to {filename}...")
                
        print("DSL Task completed successfully.")
