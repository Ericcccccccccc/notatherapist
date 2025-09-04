# NotATherapist

An AI-powered conversational companion web application built with a microservices architecture and deployed on Oracle Cloud.

## 🏗️ Architecture Overview

NotATherapist uses a streamlined architecture with a unified backend service to minimize HTTP overhead:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Frontend   │────▶│     Caddy    │────▶│  Backend Service │
│   (Static)   │     │   (Reverse   │     │   (Flask API)    │
│              │     │    Proxy)    │     │    Port 5004     │
└──────────────┘     └──────────────┘     └──────────────────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │  Baseten AI  │
                                            │   (GPT-OSS)  │
                                            └──────────────┘
```

### Backend Service Components:
- **LLM Gateway**: Handles AI communication with Baseten
- **Input Processor**: Validates and preprocesses messages
- **Response Processor**: Enhances and filters AI responses

All components run within a single Flask application on port 5004 to reduce latency and complexity.

## 📁 Project Structure

```
notatherapist/
├── frontend/                 # Web interface
│   ├── index.html           # Main HTML page
│   ├── style.css            # Styling
│   ├── app.js               # Client-side JavaScript
│   ├── Caddyfile            # Web server configuration
│   └── Dockerfile           # Container configuration
│
├── backend/                  # Unified backend service
│   ├── app.py               # Main Flask application (port 5004)
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Container configuration
│   ├── llm_gateway.py       # AI integration module
│   ├── input_processor.py   # Request preprocessing module
│   └── response_processor.py # Response enhancement module
│
├── docker-compose.yml        # Multi-container orchestration
├── deploy.sh                # Deployment automation script
└── README.md                # This file
```

## 🛠️ Technology Stack

### Frontend
- **HTML/CSS/JavaScript** - Vanilla web technologies for simplicity
- **Caddy** - Modern web server with automatic HTTPS
- **Docker** - Containerization for consistent deployment

### Backend
- **Python/Flask** - Unified API service on port 5004
- **Baseten AI** - LLM provider (OpenAI-compatible API)
- **Gunicorn** - Production WSGI server
- **Docker** - Service containerization

### Infrastructure
- **Oracle Cloud** - Ubuntu VM hosting
- **Docker Compose** - Multi-container orchestration
- **Let's Encrypt** - Automatic SSL certificates via Caddy

## 🚀 Deployment

### Prerequisites
- Docker and Docker Compose installed locally
- Oracle Cloud Ubuntu instance (or any Linux server)
- Domain name pointed to server IP
- SSH key for server access

### Configuration

1. **Update deployment settings** in `deploy.sh`:
```bash
REMOTE_HOST="170.9.233.1"  # Your server IP
SSH_KEY="$HOME/Documents/tech/notatherapist/oracle-ssh.key"  # Your SSH key path
```

2. **Configure domain** in `frontend/Caddyfile`:
```
notatherapist.com {  # Your domain
    ...
}
```

3. **Set API keys** in `docker-compose.yml`:
```yaml
environment:
  - BASETEN_API_KEY=your_api_key_here
```

### Deploy to Production

```bash
# One-command deployment
./deploy.sh
```

This script will:
1. Build Docker images for all services
2. Transfer images to the server
3. Start all services using Docker Compose
4. Configure automatic HTTPS with Caddy

### Manual Deployment Steps

```bash
# Build images
docker build -t notatherapist-frontend ./frontend
docker build -t notatherapist-backend ./backend

# Save images
docker save notatherapist-frontend notatherapist-backend | gzip > images.tar.gz

# Transfer to server
scp images.tar.gz ubuntu@server:/tmp/
scp docker-compose.yml ubuntu@server:~/

# On server
docker load < /tmp/images.tar.gz
docker-compose up -d
```

## 🔧 Local Development

### Frontend Development
```bash
cd frontend
# Open index.html in browser
# Or use a local server
python3 -m http.server 8000
```

### Backend Development
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Full Stack with Docker Compose
```bash
# Build and run all services
docker-compose up --build

# Services available at:
# Frontend: http://localhost
# Backend API: http://localhost:5004
```

## 📡 API Endpoints

### Backend Service (Port 5004)

**POST /chat**
```json
Request:
{
  "message": "User's message",
  "conversation_id": "optional_conversation_id"
}

Response:
{
  "response": "AI-generated response",
  "conversation_id": "conversation_id",
  "timestamp": "2025-09-03T12:00:00Z"
}
```

**GET /health**
```json
Response:
{
  "status": "healthy",
  "service": "backend",
  "timestamp": "2025-09-03T12:00:00Z"
}
```

## 🔒 Security Considerations

### Network Security
- **Oracle Cloud Security Lists**: Ingress rules for ports 80, 443, and 22
- **Docker Network Isolation**: Services communicate via internal network
- **HTTPS Only**: Automatic redirect from HTTP to HTTPS

### Application Security
- **CORS Configuration**: Restricted to frontend origin
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.
- **API Key Management**: Environment variables (move to secrets manager in production)

### Required Firewall Rules
```
Ingress Rules:
- Port 80: HTTP (for Let's Encrypt validation and redirect)
- Port 443: HTTPS (main application traffic)
- Port 22: SSH (admin access only)
```

## 🚦 Monitoring & Maintenance

### Check Service Status
```bash
# On server
docker ps
docker-compose logs -f

# From local machine
ssh -i ~/path/to/key ubuntu@server 'docker ps'
```

### Update Services
```bash
# Rebuild and redeploy
./deploy.sh

# Or restart specific service
ssh -i key ubuntu@server 'docker-compose restart llm_gateway'
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker logs notatherapist-frontend -f
docker logs notatherapist-backend -f
```

## 🎯 Future Enhancements

### Planned Features
- **Input Processing**: Message validation, rate limiting, and content moderation
- **Response Processing**: Response filtering, enhancement, and streaming support
- **WebSocket Support**: Real-time bidirectional communication
- **Database Integration**: Conversation history and user sessions
- **Cache Layer**: Redis for performance optimization
- **Queue System**: Asynchronous task processing

### Infrastructure Improvements
- Kubernetes deployment for better scaling
- CI/CD pipeline with GitHub Actions
- Monitoring with Prometheus/Grafana
- Centralized logging with ELK stack
- Load balancing for high availability

## 📝 License

[Your License Here]

## 🤝 Contributing

[Contributing guidelines if applicable]

## 📧 Contact

[Your contact information]

---

Built with ❤️ using modern web technologies and deployed on Oracle Cloud.