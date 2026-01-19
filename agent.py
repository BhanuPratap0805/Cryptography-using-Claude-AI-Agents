"""
Crypto Agent - Main Orchestrator
Coordinates policy enforcement, plugin execution, and audit logging
"""

from plugins.plugin_manager import PluginManager
from policy import policy_engine
from audit import logger
import re


class CryptoAgent:
    def __init__(self):
        print("🤖 Initializing Crypto Agent...")
        self.plugin_manager = PluginManager()
        self.policy_engine = policy_engine
        self.audit_logger = logger
        print("✅ Agent ready\n")
    
    def parse_request(self, user_input):
        """
        Parse natural language request
        
        Example: "generate certificate for api.example.com"
        """
        user_input = user_input.lower().strip()
        
        # Extract domain name
        domain_match = re.search(r'for\s+([a-z0-9.-]+)', user_input)
        if not domain_match:
            raise ValueError("Could not parse domain name. Use format: 'generate certificate for domain.com'")
        
        domain = domain_match.group(1)
        
        # Default parameters
        request = {
            "operation": "generate_certificate",
            "common_name": domain,
            "algorithm": "rsa",
            "key_size": 2048,
            "validity_days": 365
        }
        
        # Check for key size override
        if "3072" in user_input:
            request["key_size"] = 3072
        elif "4096" in user_input:
            request["key_size"] = 4096
        
        return request
    
    def generate_certificate(self, request):
        """
        Main workflow: Generate certificate
        
        Steps:
        1. Validate against policies
        2. Generate RSA key
        3. Create CSR
        4. Create self-signed certificate
        5. Log operation
        """
        print(f"\n{'='*60}")
        print(f"🎯 REQUEST: Generate certificate for {request['common_name']}")
        print(f"{'='*60}\n")
        
        # Step 1: Policy Validation
        print("🔒 Step 1: Policy Validation")
        policy_result = self.policy_engine.validate_request(request)
        
        if not policy_result['approved']:
            print("❌ Policy validation FAILED")
            for violation in policy_result['violations']:
                print(f"   ⚠️  {violation}")
            
            # Log failure
            self.audit_logger.log_operation(
                operation_type="certificate_generation",
                request=request,
                result={"status": "DENIED", "reason": "Policy violations"},
                policy_check=policy_result
            )
            
            return {"status": "DENIED", "violations": policy_result['violations']}
        
        print("✅ Policy validation PASSED")
        if policy_result['warnings']:
            for warning in policy_result['warnings']:
                print(f"   ⚠️  {warning}")
        print()
        
        # Prepare output name
        output_name = request['common_name'].replace('.', '_')
        
        try:
            # Step 2: Generate Key
            print(f"🔑 Step 2: Generate RSA Key")
            key_result = self.plugin_manager.execute_operation("generate_key_rsa", {
                "key_size": request['key_size'],
                "output_name": output_name
            })
            print()
            
            # Step 3: Create CSR
            print(f"📝 Step 3: Create CSR")
            csr_result = self.plugin_manager.execute_operation("create_csr", {
                "private_key_path": key_result['private_key_path'],
                "common_name": request['common_name'],
                "output_name": output_name
            })
            print()
            
            # Step 4: Create Self-Signed Certificate
            print(f"📜 Step 4: Generate Self-Signed Certificate")
            cert_result = self.plugin_manager.execute_operation("self_sign_cert", {
                "csr_path": csr_result['csr_path'],
                "private_key_path": key_result['private_key_path'],
                "output_name": output_name,
                "validity_days": request['validity_days']
            })
            print()
            
            # Step 5: Audit Log
            final_result = {
                "status": "SUCCESS",
                "certificate_path": cert_result['cert_path'],
                "private_key_path": key_result['private_key_path'],
                "common_name": request['common_name'],
                "validity_days": cert_result['validity_days']
            }
            
            self.audit_logger.log_operation(
                operation_type="certificate_generation",
                request=request,
                result=final_result,
                policy_check=policy_result
            )
            
            print(f"\n{'='*60}")
            print(f"✅ CERTIFICATE GENERATED SUCCESSFULLY")
            print(f"{'='*60}")
            print(f"📜 Certificate: {cert_result['cert_path']}")
            print(f"🔑 Private Key: {key_result['private_key_path']}")
            print(f"📅 Valid for: {cert_result['validity_days']} days")
            print(f"{'='*60}\n")
            
            return final_result
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}\n")
            
            error_result = {
                "status": "ERROR",
                "error": str(e)
            }
            
            self.audit_logger.log_operation(
                operation_type="certificate_generation",
                request=request,
                result=error_result,
                policy_check=policy_result
            )
            
            return error_result