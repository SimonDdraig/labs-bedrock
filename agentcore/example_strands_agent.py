#!/usr/bin/env python3
"""
Example Strands agent adapted for AgentCore deployment
"""
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent, tool
import boto3
import os

app = BedrockAgentCoreApp()

# Your existing Strands agent code
@tool
def query_knowledge_base(query: str) -> str:
    """Query Bedrock knowledge base"""
    kb_client = boto3.client('bedrock-agent-runtime')
    # Your KB query logic here
    return f"KB result for: {query}"

@tool  
def call_external_api(endpoint: str) -> str:
    """Call external API"""
    # Your API call logic here
    return f"API result from: {endpoint}"

# Create agent with tools
agent = Agent(
    tools=[query_knowledge_base, call_external_api],
    model="bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)

@app.entrypoint
def invoke(payload):
    """AgentCore entrypoint - required for deployment"""
    user_message = payload.get("prompt", "Hello!")
    
    try:
        result = agent(user_message)
        return {"result": result.message}
    except Exception as e:
        app.logger.error(f"Agent error: {e}")
        return {"error": "An error occurred processing your request"}

if __name__ == "__main__":
    app.run()  # For local testing