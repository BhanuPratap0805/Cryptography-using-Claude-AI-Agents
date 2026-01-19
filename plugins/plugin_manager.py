"""
Plugin Manager
Discovers and manages crypto plugins
"""

from plugins.rsa_key_plugin import RSAKeyPlugin
from plugins.csr_plugin import CSRPlugin
from plugins.selfsign_plugin import SelfSignPlugin


class PluginManager:
    def __init__(self):
        self.plugins = []
        self.load_plugins()
    
    def load_plugins(self):
        """Load all available plugins"""
        self.plugins.append(RSAKeyPlugin())
        self.plugins.append(CSRPlugin())
        self.plugins.append(SelfSignPlugin())
        
        print(f"✅ Loaded {len(self.plugins)} plugins:")
        for plugin in self.plugins:
            print(f"   - {plugin.name}")
    
    def find_plugin(self, operation_type):
        """
        Find plugin that can handle this operation
        
        Args:
            operation_type: str like "generate_key"
        
        Returns:
            CryptoPlugin instance or None
        """
        for plugin in self.plugins:
            if plugin.can_handle(operation_type):
                return plugin
        return None
    
    def execute_operation(self, operation_type, params):
        """
        Find appropriate plugin and execute operation
        
        Args:
            operation_type: str
            params: dict
        
        Returns:
            dict with results
        """
        plugin = self.find_plugin(operation_type)
        
        if not plugin:
            raise ValueError(f"No plugin found for operation: {operation_type}")
        
        print(f"🔧 Using plugin: {plugin.name}")
        return plugin.execute(params)