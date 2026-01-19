"""
Command-Line Interface for Crypto Agent
"""

from agent import CryptoAgent


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🔐 Crypto PKI Agent - Certificate Generator 🔐      ║
║                                                          ║
║     AI-Powered Cryptographic Lifecycle Management       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)


def print_help():
    print("""
Available Commands:
  generate certificate for <domain>     Generate a certificate for domain
  generate certificate for <domain> 3072  Generate with 3072-bit key
  help                                  Show this help message
  exit                                  Exit the agent

Examples:
  > generate certificate for api.example.com
  > generate certificate for app.company.com 3072
    """)


def main():
    print_banner()
    
    # Initialize agent
    agent = CryptoAgent()
    
    print("Type 'help' for commands, 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("🔐 > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if 'certificate' in user_input.lower():
                request = agent.parse_request(user_input)
                result = agent.generate_certificate(request)
            else:
                print("❌ Unknown command. Type 'help' for available commands.\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()