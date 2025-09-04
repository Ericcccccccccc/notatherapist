# Mental Health Assistant MVP - notatherapist

Modular mental health application with independent components communicating via HTTP REST APIs.

## Tech Stack
- Frontend: HTML/CSS/JavaScript served by Caddy
- Backend: Python/Flask (unified service on port 5004)
- Database: PostgreSQL 16 (planned)
- Hosting: Ubuntu VM on Oracle Cloud via Docker
- External API: Baseten AI (openai/gpt-oss-120b model)

## File Structure

notatherapist/
├── database/
│   ├── schema.sql
│   └── db_service.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── backend/
│   ├── app.py              # Main Flask application (port 5004)
│   ├── llm_gateway.py      # AI integration module
│   ├── input_processor.py  # Request validation module
│   ├── response_processor.py # Response enhancement module
│   ├── requirements.txt
│   └── Dockerfile
├── log_service/
│   └── logger.py
└── scripts/
   └── (deployment and utility scripts)

## Architecture Flow
1. Frontend → Caddy (reverse proxy)
2. Caddy → Backend API (port 5004)
3. Backend processing pipeline:
   - Input validation and preprocessing
   - LLM communication with Baseten AI
   - Response processing and enhancement
4. Backend → Frontend (JSON response)

## Architecture Decision: Unified Backend Service

**Decision**: Consolidated all backend components into a single Flask application running on port 5004.

**Rationale**:
- **Reduced HTTP overhead**: Eliminated inter-service HTTP calls between input gateway, processor, LLM gateway, and response processor
- **Lower latency**: Direct function calls instead of network requests
- **Simplified deployment**: Single Docker container for entire backend
- **Easier debugging**: All backend logic in one place
- **Resource efficiency**: One Python process instead of multiple

The modules (input_processor, llm_gateway, response_processor) now exist as Python modules within the main Flask app rather than separate services.

## Core Principles
- Modular code organization within unified service
- All database operations go through db_service (when implemented)
- All logging goes through log_service
- Correlation via interaction_id throughout pipeline
- Clear interface contracts between modules
- DRY principle - shared utilities
- Descriptive naming: snake_case for Python, camelCase for JavaScript
- Docker containerization for consistent deployment

## Environment Variables
Backend service configuration:
- BASETEN_API_KEY: API key for Baseten AI
- DB_CONNECTION: PostgreSQL connection string (future)
- PORT: 5004 (backend service port)
- LOG_LEVEL: Application logging level