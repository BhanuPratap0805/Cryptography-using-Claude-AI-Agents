"""
CSR Creation Plugin
Creates Certificate Signing Requests using OpenSSL
"""

import subprocess
import tempfile
import os
from plugins.base import CryptoPlugin


class CSRPlugin(CryptoPlugin):
    def __init__(self):
        super().__init__()
        self.name = "CSR Generator"
        self.description = "Creates Certificate Signing Requests"
    
    def can_handle(self, operation_type):
        return operation_type == "create_csr"
    
    def execute(self, params):
        """
        Create CSR
        
        Params:
            - private_key_path: str
            - common_name: str (domain name)
            - output_name: str
        
        Returns:
            - csr_path: str
            - subject: str
        """
        self.validate_params(params, ['private_key_path', 'common_name', 'output_name'])
        
        private_key_path = params['private_key_path']
        common_name = params['common_name']
        output_name = params['output_name']
        
        csr_path = f"output/csrs/{output_name}.csr"
        
        # Subject for CSR
        subject = f"/C=US/ST=State/L=City/O=Organization/CN={common_name}"
        
        print(f"📝 Creating CSR for {common_name}...")
        
        # Create a config file for OpenSSL (more reliable across platforms)
        config_content = f"""
[req]
distinguished_name = req_distinguished_name
prompt = no

[req_distinguished_name]
C = US
ST = State
L = City
O = Organization
CN = {common_name}
"""
        
        # Write config to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as config_file:
            config_file.write(config_content)
            config_path = config_file.name
        
        try:
            # Generate CSR using config file
            result = subprocess.run([
                "openssl", "req",
                "-new",
                "-key", private_key_path,
                "-out", csr_path,
                "-config", config_path
            ], check=True, capture_output=True, text=True)
            
            print(f"✅ CSR created: {csr_path}")
            
        finally:
            # Clean up config file
            if os.path.exists(config_path):
                os.unlink(config_path)
        
        return {
            "csr_path": csr_path,
            "subject": subject,
            "common_name": common_name
        }