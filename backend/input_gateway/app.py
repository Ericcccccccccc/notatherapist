from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'input_gateway'}), 200

@app.route('/input', methods=['POST'])
def receive_input():
    """
    Receives input from frontend and routes to appropriate processor
    """
    try:
        data = request.json
        # TODO: Implement input routing logic
        logger.info(f"Received input: {data}")
        
        return jsonify({
            'status': 'received',
            'message': 'Input gateway placeholder - not yet implemented'
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)