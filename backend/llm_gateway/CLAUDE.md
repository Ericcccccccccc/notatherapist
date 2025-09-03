# LLM Gateway Service

## Overview
The LLM Gateway is a microservice that handles communication with the Baseten AI platform to provide conversational AI capabilities for NotATherapist.

## Structure
```
backend/llm_gateway/
├── app.py              # Flask application with chat endpoint
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
└── CLAUDE.md          # This documentation file
```

## API Endpoints

### POST /chat
Processes chat messages and returns AI-generated responses.

**Request Body:**
```json
{
  "message": "User's message",
  "conversation_id": "optional_conversation_id"
}
```

**Response:**
```json
{
  "response": "AI-generated response",
  "conversation_id": "conversation_id"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "llm_gateway"
}
```

## Configuration
- Port: 5004
- Model: openai/gpt-oss-120b (via Baseten)
- API Key: Currently using environment variable BASETEN_API_KEY

## Dependencies
- Flask 3.0.0 - Web framework
- flask-cors 4.0.0 - CORS support
- openai - OpenAI client library for Baseten API
- httpx 0.25.0 - HTTP client (specific version for compatibility)
- gunicorn 21.2.0 - Production WSGI server

## Running Locally
```bash
cd backend/llm_gateway
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Docker Deployment
The service is containerized and runs as part of the docker-compose stack:
```bash
docker compose build llm_gateway
docker compose up llm_gateway
```

## Notes
- The service uses the Baseten API endpoint with OpenAI-compatible interface
- Currently configured with a simple system prompt for NotATherapist persona
- Conversation IDs are passed through but not currently used for context management
- httpx version 0.25.0 is required for compatibility with the OpenAI library