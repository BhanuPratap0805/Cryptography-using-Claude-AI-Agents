"""
RSA Key Generation Plugin
Generates RSA key pairs using OpenSSL
"""

import subprocess
import os
from plugins.base import CryptoPlugin


class RSAKeyPlugin(CryptoPlugin):
    def __init__(self):
        super().__init__()
        self.name = "RSA Key Generator"
        self.description = "Generates RSA key pairs"
    
    def can_handle(self, operation_type):
        return operation_type == "generate_key_rsa"
    
    def execute(self, params):
        """
        Generate RSA key pair
        
        Params:
            - key_size: int (e.g., 2048, 3072, 4096)
            - output_name: str (e.g., "api_example_com")
        
        Returns:
            - private_key_path: str
            - public_key_path: str
            - key_size: int
        """
        self.validate_params(params, ['key_size', 'output_name'])
        
        key_size = params['key_size']
        output_name = params['output_name']
        
        # File paths
        private_key_path = f"output/keys/{output_name}_private.pem"
        public_key_path = f"output/keys/{output_name}_public.pem"
        
        print(f"🔑 Generating {key_size}-bit RSA key pair...")
        
        # Generate private key
        subprocess.run([
            "openssl", "genrsa",
            "-out", private_key_path,
            str(key_size)
        ], check=True, capture_output=True)
        
        # Extract public key
        subprocess.run([
            "openssl", "rsa",
            "-in", private_key_path,
            "-pubout",
            "-out", public_key_path
        ], check=True, capture_output=True)
        
        print(f"✅ RSA key pair generated")
        print(f"   Private key: {private_key_path}")
        print(f"   Public key: {public_key_path}")
        
        return {
            "private_key_path": private_key_path,
            "public_key_path": public_key_path,
            "key_size": key_size,
            "algorithm": "RSA"
        }