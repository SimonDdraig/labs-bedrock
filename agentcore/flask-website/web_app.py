from flask import Flask, render_template, request, jsonify, session
import boto3
import json
import uuid
from certifi import where
from config import AGENT_RUNTIME_ARN, REGION

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure AWS clients
agentcore = boto3.client('bedrock-agentcore', region_name=REGION, verify=where())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Generate or retrieve session ID (minimum 33 chars)
    if 'session_id' not in session:
        session['session_id'] = f"web-session-{uuid.uuid4()}"
    
    try:
        response = agentcore.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            payload=json.dumps({"prompt": user_message}),
            runtimeSessionId=session['session_id']
        )
        
        # Extract response text
        result = ''
        if response.get('contentType') == 'application/json':
            for chunk in response.get('response', []):
                result += chunk.decode('utf-8')
            result = json.loads(result)
        else:
            result = response.get('response', '')
        
        # Format response if it contains metrics
        if isinstance(result, dict) and 'answer' in result:
            formatted = result['answer'].replace('<thinking>', '').replace('</thinking>', '').strip()
            metrics = result.get('metrics', {})
            if metrics:
                formatted += f"\n\n---\n📊 Tokens: {metrics.get('total_tokens', 'N/A')} | ⏱️ Time: {metrics.get('execution_time', 'N/A')} | 🔧 Tools: {', '.join(metrics.get('tools_used', []))}"
            return jsonify({'response': formatted})
        
        return jsonify({'response': str(result)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
