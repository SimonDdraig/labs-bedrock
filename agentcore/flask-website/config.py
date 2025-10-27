import warnings

# ===== CONFIGURATION =====
# AWS region
REGION = "us-east-1"

# Your AGENT_RUNTIME_ARN
AGENT_RUNTIME_ARN = 'XXXXXXXX'  # Replace with your agent arn

# DO NOT REPLACE THIS ONE - ITS USED TO WARN WHEN YOU HAVE NOT DONE IT ABOVE!!
if AGENT_RUNTIME_ARN == "XXXXXXXX":
    warnings.warn(
        "\n⚠️  =================================\n"
        "\n⚠️  AGENT_RUNTIME_ARN is not configured properly.\n"
        "This is required by your Flask website, edit flask-website/config.py!\n"
        "Find your ARN from lab 3.\n",
        UserWarning,
        stacklevel=2
    )