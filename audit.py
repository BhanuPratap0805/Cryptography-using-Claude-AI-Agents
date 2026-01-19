"""
Audit Logging Module
Logs all agent operations to audit_log.json
"""

import json
import os
from datetime import datetime


class AuditLogger:
    def __init__(self, log_file="audit_log.json"):
        self.log_file = log_file
        
        # Create log file if doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_operation(self, operation_type, request, result, policy_check=None):
        """
        Log a cryptographic operation
        
        Args:
            operation_type: "cert_generation", "key_generation", etc.
            request: User's original request
            result: Outcome (success/failure, files generated, etc.)
            policy_check: Policy validation result
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operation": operation_type,
            "request": request,
            "policy_check": policy_check,
            "result": result
        }
        
        # Read existing logs
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        
        # Append new entry
        logs.append(entry)
        
        # Write back
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"📝 Audit log entry created: {entry['timestamp']}")
    
    def get_logs(self, limit=10):
        """Retrieve recent logs"""
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        return logs[-limit:]


# Singleton instance
logger = AuditLogger()