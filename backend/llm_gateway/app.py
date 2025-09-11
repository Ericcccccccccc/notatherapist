from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key="jPodC7PX.km2yvG9icviCMGklMgyrbSyxcVdnr3iY",
    base_url="https://inference.baseten.co/v1"
)

def get_db_connection():
    """Create database connection using Unix socket"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host='/var/run/postgresql',  # Unix socket directory
                database='notatherapist_db',
                user='notatherapist',
                password=os.getenv('POSTGRES_PASSWORD', 'secure_password_here'),
                cursor_factory=RealDictCursor
            )
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to database after {max_retries} attempts: {str(e)}")
                raise

def save_input_to_db(input_text, conversation_id=None):
    """Save user input to the database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO input_table (input, conversation_id) 
            VALUES (%s, %s)
            RETURNING id, created_at
            """,
            (input_text, conversation_id)
        )
        
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"Saved input to database with ID: {result['id']}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to save input to database: {str(e)}")
        # Don't fail the request if database save fails
        return None

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        conversation_id = data.get('conversation_id')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"Received message: {message[:50]}... (conversation: {conversation_id})")
        
        # Save input to database before processing
        db_result = save_input_to_db(message, conversation_id)
        
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
            'conversation_id': conversation_id or f"conv_{datetime.now().timestamp()}",
            'input_saved': db_result is not None,
            'input_id': db_result['id'] if db_result else None
        })
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            'error': 'Failed to process request',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint with database connectivity check"""
    health_status = {
        'status': 'healthy',
        'service': 'llm_gateway',
        'database': 'unknown'
    }
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['database'] = f'disconnected: {str(e)}'
        health_status['status'] = 'degraded'
    
    return jsonify(health_status), 200 if health_status['status'] == 'healthy' else 503

@app.route('/inputs', methods=['GET'])
def get_inputs():
    """Retrieve recent inputs from the database"""
    try:
        limit = request.args.get('limit', 10, type=int)
        conversation_id = request.args.get('conversation_id')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        if conversation_id:
            cur.execute(
                """
                SELECT id, input, conversation_id, created_at, processed
                FROM input_table 
                WHERE conversation_id = %s
                ORDER BY created_at DESC 
                LIMIT %s
                """,
                (conversation_id, limit)
            )
        else:
            cur.execute(
                """
                SELECT id, input, conversation_id, created_at, processed
                FROM input_table 
                ORDER BY created_at DESC 
                LIMIT %s
                """,
                (limit,)
            )
        
        results = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert datetime objects to strings for JSON serialization
        for result in results:
            if result['created_at']:
                result['created_at'] = result['created_at'].isoformat()
        
        return jsonify({
            'inputs': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Failed to retrieve inputs: {str(e)}")
        return jsonify({'error': 'Failed to retrieve inputs', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=os.getenv('DEBUG', 'False').lower() == 'true')