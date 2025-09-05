from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Import processing modules
from input_processor import process_input
from llm_gateway import get_ai_response
from response_processor import process_response

app = Flask(__name__)

# Configure CORS with environment variable
cors_origins = os.getenv('CORS_ORIGINS', '*')
if cors_origins != '*':
    cors_origins = cors_origins.split(',')
CORS(app, origins=cors_origins)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint that coordinates the processing pipeline"""
    try:
        # Get request data
        data = request.json
        original_message = data.get('message')
        conversation_id = data.get('conversation_id')
        
        if not original_message:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"Received message: {original_message[:50]}... (conversation: {conversation_id})")
        
        # Step 1: Process input (add joke request)
        processed_message = process_input(original_message)
        logger.info(f"Processed input: {processed_message[:100]}...")
        
        # Step 2: Get AI response
        ai_response = get_ai_response(processed_message)
        logger.info(f"AI response received: {ai_response[:50]}...")
        
        # Step 3: Process response (add joke acknowledgment)
        final_response = process_response(ai_response)
        logger.info(f"Final response: {final_response[:50]}...")
        
        return jsonify({
            'response': final_response,
            'conversation_id': conversation_id or f"conv_{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            'error': 'Failed to process request',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'service': 'backend',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=os.getenv('DEBUG', 'False').lower() == 'true')