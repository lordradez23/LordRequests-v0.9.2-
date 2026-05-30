'''
Plugin System Foundation
~~~~~~~~~~~~~~~~~~~~~~~~

Support for community-built extension modules.
'''

import importlib
import pkgutil
from typing import Dict, Any, List

class PluginManager:
    _plugins: Dict[str, Any] = {}

    @classmethod
    def load_plugins(cls):
        '''Discovers and loads plugins from the plugins directory.'''
        import hrequests.plugins as plugin_pkg
        for _, name, is_pkg in pkgutil.iter_modules(plugin_pkg.__path__, plugin_pkg.__name__ + "."):
            try:
                module = importlib.import_module(name)
                plugin_name = name.split(".")[-1]
                cls._plugins[plugin_name] = module
                print(f"Loaded plugin: {plugin_name}")
                
                # Check for 'on_load' hook
                if hasattr(module, 'on_load'):
                    module.on_load()
            except Exception as e:
                print(f"Failed to load plugin {name}: {e}")

    @classmethod
    def get_plugin(cls, name: str) -> Any:
        return cls._plugins.get(name)

    @classmethod
    def list_plugins(cls) -> List[str]:
        return list(cls._plugins.keys())

# Auto-load plugins when requested
def register_plugin(name: str, instance: Any):
    PluginManager._plugins[name] = instance
