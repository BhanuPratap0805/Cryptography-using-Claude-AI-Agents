"""
Policy Enforcement Module
Validates requests against cryptographic policies
"""

import yaml


class PolicyEngine:
    def __init__(self, policy_file="policies/crypto_policies.yaml"):
        with open(policy_file, 'r') as f:
            self.policies = yaml.safe_load(f)
    
    def validate_request(self, request):
        """
        Validate request against policies
        
        Args:
            request: dict with keys like 'algorithm', 'key_size', 'validity_days', etc.
        
        Returns:
            dict: {"approved": bool, "violations": list, "warnings": list}
        """
        violations = []
        warnings = []
        
        # Check algorithm is allowed
        algorithm = request.get('algorithm', 'rsa').lower()
        if algorithm not in self.policies['allowed_algorithms']:
            violations.append(f"Algorithm '{algorithm}' not in allowed list: {self.policies['allowed_algorithms']}")
        
        # Check key size (if applicable)
        if algorithm in self.policies['minimum_key_sizes']:
            min_size = self.policies['minimum_key_sizes'][algorithm]
            actual_size = request.get('key_size', 0)
            
            if actual_size < min_size:
                violations.append(f"{algorithm.upper()} key size must be ≥{min_size} bits, got {actual_size}")
            elif actual_size == min_size:
                warnings.append(f"Using minimum key size {min_size}. Consider larger for better security.")
        
        # Check validity period
        validity_days = request.get('validity_days', 365)
        max_validity = self.policies['maximum_validity_days']
        if validity_days > max_validity:
            violations.append(f"Validity period ({validity_days} days) exceeds maximum ({max_validity} days)")
        
        # Check forbidden algorithms
        if algorithm in self.policies.get('forbidden_algorithms', []):
            violations.append(f"Algorithm '{algorithm}' is explicitly forbidden")
        
        approved = len(violations) == 0
        
        return {
            "approved": approved,
            "violations": violations,
            "warnings": warnings
        }


# Singleton instance
policy_engine = PolicyEngine()