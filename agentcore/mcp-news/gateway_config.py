import os
import json
import requests
from agentcore_gateway import Gateway, Tool

gateway = Gateway()

@gateway.tool(
    name="fetch_news",
    description="Fetch news from external API using OAuth authentication"
)
def fetch_news():
    oauth_token = os.environ.get('OAUTH_TOKEN')
    api_url = os.environ.get('API_URL')
    
    if not oauth_token or not api_url:
        return {"error": "Missing OAUTH_TOKEN or API_URL"}
    
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    gateway.run()
