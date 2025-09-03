from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key="jPodC7PX.km2yvG9icviCMGklMgyrbSyxcVdnr3iY",
    base_url="https://inference.baseten.co/v1"
)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        conversation_id = data.get('conversation_id')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"Received message: {message[:50]}... (conversation: {conversation_id})")
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are NotATherapist, a helpful AI assistant. Be friendly, empathetic, and supportive in your responses."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=1000,
            temperature=0.7,
            top_p=1,
            presence_penalty=0,
            frequency_penalty=0
        )
        
        response_text = response.choices[0].message.content
        
        logger.info(f"Generated response: {response_text[:50]}...")
        
        return jsonify({
            'response': response_text,
            'conversation_id': conversation_id or f"conv_{datetime.now().timestamp()}"
        })
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            'error': 'Failed to process request',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'llm_gateway'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=os.getenv('DEBUG', 'False').lower() == 'true')