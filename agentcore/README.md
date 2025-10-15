# labs-bedrock-agentcore

Currently supported regions:
https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html

- Lab 1
    - Create a knowledge base
    - Ingest documents from S3
    - Query the knowledge base using Bedrock
- Lab 2
    - Demonstrate use of Strands agents
      - Agent which uses the Bedrock knowledge base created in lab 1 (Strands_Agent_KB_Bedrock.py)
      - Agent which calls an API (Strands_Agent_API.py)
      - Agent which calls an MCP (Strands_Agent_MCP_CoinGecko.py)
      - Agent which calls Bedrock ffm (Strands_Agent_General.py)
- Lab 3
  - Deploys the Strands agents using AgentCore

# AgentCore
### AgentCore Runtime
- Runtime provides a secure, serverless and purpose-built hosting environment for deploying and running AI agents or tools
- AgentCore Runtime lets you transform any local agent code to cloud-native deployments with a few lines of code no matter the underlying framework. Works seamlessly with popular frameworks like LangGraph, Strands, and CrewAI
- Runtime works with any Large Language Model, such as models offered by Amazon Bedrock, Anthropic Claude, Google Gemini, and OpenAI
- Runtime lets agents communicate with other agents and tools via Model Context Protocol (MCP).
- Runtime implements consumption-based pricing that charges only for resources actually consumed
- Runtime automatically scales to meet demand, eliminating the need to manage infrastructure or capacity planning
- Deploy:
  - Agents
  - MCP
  - Agents 2 Agents
  - Orchestration agents


### AgentCore Memory
- AgentCore provides a memory feature that allows agents to retain context across interactions.
- Two types of memory:
  - Short-term
    - Short-term memory captures turn-by-turn interactions within a single session. This lets agents maintain immediate context without requiring users to repeat information.
      - Example: When a user asks, "What's the weather like in Seattle?" and follows up with "What about tomorrow?", the agent relies on recent conversation history to understand that "tomorrow" refers to the weather in Seattle.
    - AgentCore MCP Server states this is stored in DynamoDB
  - Long-term
    - Long-term memory automatically extracts and stores key insights from conversations across multiple sessions, including user preferences, important facts, and session summaries — for persistent knowledge retention across multiple sessions.
      - Example: If a customer mentions they prefer window seats during flight booking, the agent stores this preference in long-term memory. In future interactions, the agent can proactively offer window seats, creating a personalized experience.
    - AgentCore MCP Server states this is stored in OpenSearch

### AgentCore Gateway
- Gateway provides an easy and secure way for developers to build, deploy, discover, and connect to tools at scale
- Convert APIs, Lambda functions, and existing services into Model Context Protocol (MCP)-compatible tools and make them available to agents through Gateway endpoints with just a few lines of code
- Gateway acts like an MCP server, providing a single access point for an agent to interact with its tools
- Tool types:
  - OpenAPI specifications
  - Lambda functions
  - Smithy models (Smithy is a language for defining services and SDKs that can be used with AWS services)
  - MCP servers

### AgentCore Identity
- Identity is an identity and credential management service designed specifically for AI agents and automated workloads. 
- It provides secure authentication, authorization, and credential management capabilities that enable agents and tools to access AWS resources and third-party services on behalf of users while helping to maintain strict security controls and audit trails.

### AgentCore Built-in Tools
- Built-in tools to enhance your development and testing experience
- Tools:
  - Code Interpreter
    - A secure environment for executing code and analyzing data. The Amazon Bedrock AgentCore Code Interpreter supports multiple programming languages including Python, TypeScript, and JavaScript, allowing you to process data and perform calculations within the AgentCore environment.
  - Browser Tool
    - A secure, isolated browser environment that allows you to interact with and test web applications while minimizing potential risks to your system, access online resources, and perform web-based tasks.

### AgentCore Observability
- Trace, debug, and monitor AI agents' performance in production environments
- Detailed visualizations of each step in the agent workflow, enabling you to inspect an agent's execution path, audit intermediate outputs, and debug performance bottlenecks and failures
- Real-time visibility into agent operational performance through access to dashboards powered by Amazon CloudWatch and telemetry for key metrics such as session count, latency, duration, token usage, and error rates