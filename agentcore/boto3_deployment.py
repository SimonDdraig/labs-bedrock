#!/usr/bin/env python3
"""
Pure boto3 deployment approach for AgentCore (requires additional setup)
"""
import boto3
import json
import uuid
import base64
import zipfile
import io

class PureBoto3Deployer:
    def __init__(self, region='us-west-2'):
        self.region = region
        self.agentcore_client = boto3.client('bedrock-agentcore', region_name=region)
        self.ecr_client = boto3.client('ecr', region_name=region)
        self.codebuild_client = boto3.client('codebuild', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
    
    def create_agent_runtime(self, agent_name, container_image_uri, execution_role_arn):
        """Create AgentCore Runtime using boto3"""
        try:
            response = self.agentcore_client.create_agent_runtime(
                agentRuntimeName=agent_name,
                containerConfig={
                    'imageUri': container_image_uri,
                    'environmentVariables': {
                        'AWS_REGION': self.region
                    }
                },
                executionRoleArn=execution_role_arn,
                runtimeConfig={
                    'memoryMB': 1024,
                    'timeoutSeconds': 300
                }
            )
            return response['agentRuntimeArn']
        except Exception as e:
            print(f"Failed to create agent runtime: {e}")
            raise
    
    def build_and_push_container(self, agent_code, agent_name, requirements):
        """Build and push container to ECR"""
        # Create ECR repository
        try:
            repo_response = self.ecr_client.create_repository(
                repositoryName=f'bedrock-agentcore-{agent_name}'
            )
            repo_uri = repo_response['repository']['repositoryUri']
        except self.ecr_client.exceptions.RepositoryAlreadyExistsException:
            repo_response = self.ecr_client.describe_repositories(
                repositoryNames=[f'bedrock-agentcore-{agent_name}']
            )
            repo_uri = repo_response['repositories'][0]['repositoryUri']
        
        # Create CodeBuild project for container build
        dockerfile = self._generate_dockerfile(requirements)
        
        build_project = self._create_codebuild_project(agent_name, repo_uri, agent_code, dockerfile)
        
        # Start build
        build_response = self.codebuild_client.start_build(
            projectName=build_project['name']
        )
        
        return f"{repo_uri}:latest"
    
    def deploy_strands_agent(self, agent_file, agent_name, requirements_file=None):
        """Deploy a Strands agent using pure boto3"""
        
        # Read agent code
        with open(agent_file, 'r') as f:
            agent_code = f.read()
        
        # Read requirements
        requirements = []
        if requirements_file and os.path.exists(requirements_file):
            with open(requirements_file, 'r') as f:
                requirements = f.read().splitlines()
        else:
            requirements = ['bedrock-agentcore', 'strands-agents']
        
        # Create execution role
        execution_role_arn = self._create_execution_role(agent_name)
        
        # Build and push container
        container_uri = self.build_and_push_container(agent_code, agent_name, requirements)
        
        # Create agent runtime
        agent_arn = self.create_agent_runtime(agent_name, container_uri, execution_role_arn)
        
        return agent_arn
    
    def invoke_agent(self, agent_arn, prompt):
        """Invoke agent via boto3"""
        payload = json.dumps({"prompt": prompt}).encode()
        
        response = self.agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=agent_arn,
            runtimeSessionId=str(uuid.uuid4()),
            payload=payload,
            qualifier="DEFAULT"
        )
        
        content = []
        for chunk in response.get("response", []):
            content.append(chunk.decode('utf-8'))
        
        return json.loads(''.join(content))
    
    def _generate_dockerfile(self, requirements):
        """Generate Dockerfile for the agent"""
        req_installs = '\n'.join([f'RUN pip install {req}' for req in requirements])
        
        return f"""
FROM public.ecr.aws/lambda/python:3.11-arm64

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY agent.py .

EXPOSE 8080

CMD ["python", "agent.py"]
"""
    
    def _create_execution_role(self, agent_name):
        """Create IAM execution role for the agent"""
        role_name = f"BedrockAgentCore-{agent_name}-Role"
        
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        try:
            role_response = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=f"Execution role for AgentCore agent {agent_name}"
            )
            
            # Attach necessary policies
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonBedrockAgentCoreExecutionRolePolicy'
            )
            
            return role_response['Role']['Arn']
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            role_response = self.iam_client.get_role(RoleName=role_name)
            return role_response['Role']['Arn']
    
    def _create_codebuild_project(self, agent_name, repo_uri, agent_code, dockerfile):
        """Create CodeBuild project for container build"""
        # Implementation would create CodeBuild project
        # This is complex and requires proper buildspec.yml generation
        pass

# Usage example
def main():
    deployer = PureBoto3Deployer()
    
    # Deploy agents
    kb_agent_arn = deployer.deploy_strands_agent('Strands_Agent_KB_Bedrock.py', 'kb-agent')
    api_agent_arn = deployer.deploy_strands_agent('Strands_Agent_API.py', 'api-agent')
    
    # Test invocation
    result = deployer.invoke_agent(kb_agent_arn, "Hello!")
    print(result)

if __name__ == "__main__":
    main()