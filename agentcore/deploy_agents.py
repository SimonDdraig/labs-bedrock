#!/usr/bin/env python3
"""
Deploy Strands agents to AgentCore and invoke via boto3
"""
import json
import uuid
import boto3
import subprocess
import os
from pathlib import Path

class AgentCoreDeployer:
    def __init__(self, region='us-west-2'):
        self.region = region
        self.client = boto3.client('bedrock-agentcore', region_name=region)
        self.deployed_agents = {}
    
    def deploy_agent(self, agent_file, agent_name, requirements_file=None):
        """Deploy a single Strands agent to AgentCore"""
        print(f"Deploying {agent_name} from {agent_file}")
        
        # Configure the agent
        cmd = [
            'agentcore', 'configure', 
            '-e', agent_file,
            '-r', self.region,
            '--disable-memory'  # Remove if you want memory
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(agent_file).parent)
        if result.returncode != 0:
            raise Exception(f"Configure failed: {result.stderr}")
        
        # Deploy the agent
        cmd = ['agentcore', 'launch']
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(agent_file).parent)
        if result.returncode != 0:
            raise Exception(f"Launch failed: {result.stderr}")
        
        # Extract ARN from output or config file
        config_file = Path(agent_file).parent / '.bedrock_agentcore.yaml'
        if config_file.exists():
            # Parse config to get ARN (simplified - you'd need proper YAML parsing)
            with open(config_file) as f:
                content = f.read()
                # Extract ARN from config (implement proper parsing)
                arn = self._extract_arn_from_config(content)
                self.deployed_agents[agent_name] = arn
        
        print(f"✅ {agent_name} deployed successfully")
        return arn
    
    def deploy_orchestrator(self, orchestrator_file, sub_agent_arns):
        """Deploy the orchestration agent with references to sub-agents"""
        # Update orchestrator with sub-agent ARNs
        self._update_orchestrator_config(orchestrator_file, sub_agent_arns)
        return self.deploy_agent(orchestrator_file, 'orchestrator')
    
    def invoke_agent(self, agent_arn, prompt):
        """Invoke an agent via boto3"""
        payload = json.dumps({"prompt": prompt}).encode()
        
        response = self.client.invoke_agent_runtime(
            agentRuntimeArn=agent_arn,
            runtimeSessionId=str(uuid.uuid4()),
            payload=payload,
            qualifier="DEFAULT"
        )
        
        content = []
        for chunk in response.get("response", []):
            content.append(chunk.decode('utf-8'))
        
        return json.loads(''.join(content))
    
    def _extract_arn_from_config(self, config_content):
        """Extract ARN from config file (implement proper YAML parsing)"""
        # Simplified - implement proper YAML parsing
        lines = config_content.split('\n')
        for line in lines:
            if 'arn:aws:bedrock-agentcore' in line:
                return line.split(':')[-1].strip()
        return None
    
    def _update_orchestrator_config(self, orchestrator_file, sub_agent_arns):
        """Update orchestrator with sub-agent ARNs"""
        # Read orchestrator file and inject ARNs
        # This depends on your orchestrator implementation
        pass

def main():
    deployer = AgentCoreDeployer()
    
    # Deploy individual agents
    agents = {
        'kb_agent': 'Strands_Agent_KB_Bedrock.py',
        'api_agent': 'Strands_Agent_API.py', 
        'mcp_agent': 'Strands_Agent_MCP_CoinGecko.py',
        'general_agent': 'Strands_Agent_General.py'
    }
    
    deployed_arns = {}
    for name, file in agents.items():
        arn = deployer.deploy_agent(file, name)
        deployed_arns[name] = arn
    
    # Deploy orchestrator
    orchestrator_arn = deployer.deploy_orchestrator('orchestrator_agent.py', deployed_arns)
    
    # Test invocation
    result = deployer.invoke_agent(orchestrator_arn, "What's the weather like?")
    print(f"Response: {result}")

if __name__ == "__main__":
    main()