from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Optional
from datetime import datetime
import logging
import os

# Import processing modules
from input_processor import process_input_async
from llm_gateway import get_ai_response_async
from response_processor import process_response_async

# Configuration
class Settings(BaseSettings):
    baseten_api_key: str = Field(..., env="BASETEN_API_KEY")
    cors_origins: str = Field("*", env="CORS_ORIGINS")
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    port: int = Field(5004, env="PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str

# Initialize settings
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    print("Make sure BASETEN_API_KEY is set in environment or .env file")
    raise

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="NotATherapist Backend",
    description="AI-powered mental health companion API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = settings.cors_origins
if cors_origins != "*":
    cors_origins = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that coordinates the processing pipeline.
    
    Args:
        request: ChatRequest containing the message and optional conversation_id
        
    Returns:
        ChatResponse with the AI response and metadata
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Received message: {request.message[:50]}... (conversation: {request.conversation_id})")
        
        # Step 1: Process input (add joke request)
        processed_message = await process_input_async(request.message)
        logger.info(f"Processed input: {processed_message[:100]}...")
        
        # Step 2: Get AI response
        ai_response = await get_ai_response_async(processed_message, settings.baseten_api_key)
        logger.info(f"AI response received: {ai_response[:50]}...")
        
        # Step 3: Process response (add joke acknowledgment)
        final_response = await process_response_async(ai_response)
        logger.info(f"Final response: {final_response[:50]}...")
        
        return ChatResponse(
            response=final_response,
            conversation_id=request.conversation_id or f"conv_{datetime.now().timestamp()}",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process request: {str(e)}"
        )

@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint for monitoring.
    
    Returns:
        HealthResponse with service status
    """
    return HealthResponse(
        status="healthy",
        service="backend",
        timestamp=datetime.now().isoformat()
    )

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Dict with API information and documentation links
    """
    return {
        "name": "NotATherapist Backend API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.port,
        log_level=settings.log_level.lower()
    )