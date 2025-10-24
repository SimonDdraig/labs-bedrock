import warnings
# ===== MODEL SELECTION STRATEGY PER AGENT =====
# Different agents perform distinct tasks, each with unique requirements.
# Match models to agent roles based on specific needs:
#
# Premium Models (e.g., Claude-3-7-Sonnet):
#   - Complex reasoning tasks (policy interpretation, strategic analysis)
#   - High-stakes decision making requiring maximum accuracy
#
# Fast/Economical Models (e.g., Claude-3-Haiku, Nova-micro):
#   - Simple retrieval and routing tasks
#   - Basic classification and filtering
#   - High-volume, low-complexity operations
#
# High-Context Models (e.g., Claude-3-5-Sonnet, Nova-pro):
#   - Long document analysis and summarization
#   - Multi-document synthesis
#   - Extended conversation history
#
# Structured-Output Models (JSON-optimized):
#   - Data extraction and transformation
#   - API response formatting
#   - Structured data generation
#
# Safety-First Models (enhanced controls):
#   - PII and sensitive data handling
#   - Compliance-critical operations
#   - Customer-facing interactions requiring guardrails
#
# Rationale: Optimize across multiple dimensions—accuracy, latency, cost,
# context length, and safety—by selecting the right tool for each job
# rather than using a one-size-fits-all approach.

# ===== CONFIGURATION =====
# Inference model to use
# We standardize on this model for all agents including the orchestration agent
#INFERENCE_MODEL = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
INFERENCE_MODEL = "amazon.nova-pro-v1:0"

# AWS region
REGION = "us-east-1"

# Your Bedrock Knowledge Base ID
# REPLACE THIS WITH YOURS
KB_ID = "XXXXXXXX"

# DO NOT REPLACE THIS ONE - ITS USED TO WARN WHEN YOU HAVE NOT DONE IT ABOVE!!
if KB_ID == "XXXXXXXX":
    warnings.warn(
        "\n⚠️  =================================\n"
        "\n⚠️  KB_ID is not configured properly.\n"
        "Please set your Bedrock Knowledge Base ID in config.py!\n"
        "Find your Bedrock Knowledge Base ID from a previous lab or in your console.\n"
        "You can continue to use this agent, but any prompts routed to use the knowledge base will fail.\n",
        UserWarning,
        stacklevel=2
    )