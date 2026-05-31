'''
Dynamic Plugin Loader
~~~~~~~~~~~~~~~~~~~~~

Hot-loading of hrequests plugins from a specified directory without 
restarting the host application.
'''

import os
import importlib.util
import sys
from typing import Dict, List

class PluginLoader:
    '''
    Finds and loads Python modules from a directory as plugins.
    '''
    def __init__(self, plugin_dir: str):
        self.plugin_dir = plugin_dir
        self.loaded_plugins: Dict[str, any] = {}

    def discover_and_load(self):
        '''
        Scans the directory for .py files and loads them.
        '''
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir, exist_ok=True)
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                plugin_name = filename[:-3]
                self._load_plugin(plugin_name)

    def _load_plugin(self, name: str):
        '''Loads a single plugin by name.'''
        file_path = os.path.join(self.plugin_dir, f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        
        self.loaded_plugins[name] = module
        print(f"[Plugins] Loaded: {name}")

    def call_all(self, function_name: str, *args, **kwargs) -> List[any]:
        '''
        Calls a specific function in all loaded plugins.
        '''
        results = []
        for name, module in self.loaded_plugins.items():
            if hasattr(module, function_name):
                func = getattr(module, function_name)
                results.append(func(*args, **kwargs))
        return results
