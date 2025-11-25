import json
import os
import requests

def lambda_handler(event, context):
    # Get OAuth token from environment variable
    oauth_token = os.environ.get('OAUTH_TOKEN')
    api_url = os.environ.get('API_URL')
    
    if not oauth_token or not api_url:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Missing OAUTH_TOKEN or API_URL environment variable'})
        }
    
    # Make API request with OAuth token
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        return {
            'statusCode': 200,
            'body': json.dumps(response.json())
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
