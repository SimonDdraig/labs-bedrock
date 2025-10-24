# test_crypto_agent.py
from Strands_Agent_API import crypto_security_analyzer

print("Crypto Security Analyzer Interactive Test")
print("Type 'quit' to quit\n")

while True:
    prompt = input("Enter your crypto token query: ").strip()
    if prompt.lower() == "quit":
        print("Exiting...")
        break
    if not prompt:
        print("Please enter a valid query or 'quit' to exit.")
        continue

    # Query the agent
    summary = crypto_security_analyzer(prompt)
    print("\n=== Response ===")
    print(summary)
    print("================\n")
