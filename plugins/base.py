"""
Base Plugin Class
All cryptographic operation plugins inherit from this
"""

from abc import ABC, abstractmethod


class CryptoPlugin(ABC):
    """
    Abstract base class for all crypto plugins
    """
    
    def __init__(self):
        self.name = "BasePlugin"
        self.description = ""
    
    @abstractmethod
    def can_handle(self, operation_type):
        """
        Check if this plugin can handle the given operation type
        
        Args:
            operation_type: str like "generate_key", "create_csr", etc.
        
        Returns:
            bool
        """
        pass
    
    @abstractmethod
    def execute(self, params):
        """
        Execute the cryptographic operation
        
        Args:
            params: dict with operation-specific parameters
        
        Returns:
            dict with results (file paths, fingerprints, etc.)
        """
        pass
    
    def validate_params(self, params, required_keys):
        """
        Helper to validate required parameters
        """
        missing = [key for key in required_keys if key not in params]
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")