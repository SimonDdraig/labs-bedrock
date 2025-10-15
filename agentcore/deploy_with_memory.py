#!/usr/bin/env python3
"""
Deploy agents with memory only on orchestrator
"""
import subprocess
import os

def deploy_agents():
    # 1. Deploy subagents WITHOUT memory
    subagents = [
        'Strands_Agent_KB_Bedrock.py',
        'Strands_Agent_API.py', 
        'Strands_Agent_MCP_CoinGecko.py',
        'Strands_Agent_General.py'
    ]
    
    subagent_arns = {}
    
    for agent_file in subagents:
        agent_name = agent_file.replace('.py', '').replace('Strands_Agent_', '').lower()
        
        # Configure without memory
        subprocess.run([
            'agentcore', 'configure', 
            '-e', agent_file,
            '--disable-memory'  # No memory for subagents
        ])
        
        # Deploy
        subprocess.run(['agentcore', 'launch'])
        
        # Get ARN (you'd extract this from output or config file)
        # subagent_arns[f"{agent_name}_arn"] = "arn:aws:bedrock-agentcore:..."
    
    # 2. Create memory for orchestrator
    from bedrock_agentcore.memory import MemoryClient
    import uuid
    
    memory_client = MemoryClient(region_name='us-west-2')
    
    # Create long-term memory with extraction strategies
    ltm = memory_client.create_memory_and_wait(
        name=f"Orchestrator_Memory_{uuid.uuid4().hex[:8]}",
        strategies=[
            {"userPreferenceMemoryStrategy": {
                "name": "prefs",
                "namespaces": ["/user/preferences"]
            }},
            {"semanticMemoryStrategy": {
                "name": "facts", 
                "namespaces": ["/user/facts"]
            }}
        ],
        event_expiry_days=30
    )
    
    print(f"Memory created: {ltm['id']}")
    
    # 3. Deploy orchestrator WITH memory
    os.environ['MEMORY_ID'] = ltm['id']
    # Set subagent ARNs as environment variables
    for name, arn in subagent_arns.items():
        os.environ[name.upper()] = arn
    
    subprocess.run([
        'agentcore', 'configure',
        '-e', 'orchestrator_agent.py'
        # Memory will be auto-detected from MEMORY_ID env var
    ])
    
    subprocess.run(['agentcore', 'launch'])

if __name__ == "__main__":
    deploy_agents()