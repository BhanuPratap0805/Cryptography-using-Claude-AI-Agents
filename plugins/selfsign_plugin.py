"""
Self-Signed Certificate Plugin
Creates self-signed certificates using OpenSSL
"""

import subprocess
from plugins.base import CryptoPlugin


class SelfSignPlugin(CryptoPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Self-Sign Certificate Generator"
        self.description = "Creates self-signed certificates"
    
    def can_handle(self, operation_type):
        return operation_type == "self_sign_cert"
    
    def execute(self, params):
        """
        Create self-signed certificate
        
        Params:
            - csr_path: str
            - private_key_path: str
            - output_name: str
            - validity_days: int
        
        Returns:
            - cert_path: str
            - validity_days: int
        """
        self.validate_params(params, ['csr_path', 'private_key_path', 'output_name', 'validity_days'])
        
        csr_path = params['csr_path']
        private_key_path = params['private_key_path']
        output_name = params['output_name']
        validity_days = params['validity_days']
        
        cert_path = f"output/certs/{output_name}.crt"
        
        print(f"📜 Creating self-signed certificate (valid for {validity_days} days)...")
        
        # Generate self-signed certificate
        subprocess.run([
            "openssl", "x509",
            "-req",
            "-in", csr_path,
            "-signkey", private_key_path,
            "-out", cert_path,
            "-days", str(validity_days)
        ], check=True, capture_output=True)
        
        print(f"✅ Certificate created: {cert_path}")
        
        return {
            "cert_path": cert_path,
            "validity_days": validity_days
        }