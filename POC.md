# Crypto PKI Agent - Proof of Concept

AI-powered cryptographic lifecycle management system using Claude-based agent architecture.

## Architecture

- **Single-Agent Design**: One orchestrator coordinates all operations
- **Policy Enforcement**: Pre-execution validation of cryptographic parameters
- **Plugin System**: Modular tools for crypto operations (OpenSSL-based)
- **Audit Logging**: Complete operation trail in JSON format

## Prerequisites

- Python 3.8+
- OpenSSL installed and in PATH

## Setup

1. Clone repository
2. Create virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Usage

Run the agent:
```bash
python cli.py
```

Generate a certificate:
```
> generate certificate for api.example.com
```

Generate with 3072-bit key:
```
> generate certificate for api.example.com 3072
```

## Project Structure
```
crypto-pki-agent/
├── agent.py                 # Main orchestrator
├── cli.py                   # Command-line interface
├── policy.py                # Policy enforcement
├── audit.py                 # Audit logging
├── plugins/                 # Crypto operation plugins
│   ├── rsa_key_plugin.py    # RSA key generation
│   ├── csr_plugin.py        # CSR creation
│   └── selfsign_plugin.py   # Self-signed certificates
├── policies/                # Policy definitions
│   └── crypto_policies.yaml
└── output/                  # Generated certificates
    ├── keys/
    ├── csrs/
    └── certs/
```

## Security Boundaries

- **Agent (Claude)**: Orchestration, planning, policy enforcement
- **Plugins**: Invoke OpenSSL for actual cryptography
- **Private keys**: Never handled by agent, only by OpenSSL tools

## Policies Enforced

- RSA keys: Minimum 2048 bits
- Certificate validity: Maximum 365 days
- Allowed algorithms: RSA, ECDSA
- Forbidden algorithms: DSA, MD5

## Audit Trail

All operations logged to `audit_log.json` with:
- Timestamp
- Request details
- Policy validation results
- Execution trace
- Final outcome