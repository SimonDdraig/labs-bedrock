#!/usr/bin/env python3
"""
Create memory resource and get MEMORY_ID
"""
from bedrock_agentcore.memory import MemoryClient
import uuid

# Create memory client
memory_client = MemoryClient(region_name='us-west-2')

# Create memory resource with long-term memory strategies
memory = memory_client.create_memory_and_wait(
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

memory_id = memory['id']
print(f"✅ Memory created!")
print(f"MEMORY_ID: {memory_id}")
print(f"\nSet this environment variable:")
print(f"export MEMORY_ID={memory_id}")