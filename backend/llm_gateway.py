"""
LLM Gateway Module
Handles communication with Baseten AI service
"""
from openai import AsyncOpenAI, OpenAI
import os
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

# Initialize async Baseten client (lazy initialization)
_async_client: Optional[AsyncOpenAI] = None
_sync_client: Optional[OpenAI] = None

def get_async_client(api_key: str) -> AsyncOpenAI:
    """Get or create async OpenAI client."""
    global _async_client
    if _async_client is None:
        _async_client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://inference.baseten.co/v1"
        )
    return _async_client

def get_sync_client(api_key: str) -> OpenAI:
    """Get or create sync OpenAI client for backward compatibility."""
    global _sync_client
    if _sync_client is None:
        _sync_client = OpenAI(
            api_key=api_key,
            base_url="https://inference.baseten.co/v1"
        )
    return _sync_client

async def get_ai_response_async(message: str, api_key: str) -> str:
    """
    Send message to Baseten AI and get response (async version).
    
    Args:
        message: The processed message to send to AI
        api_key: The Baseten API key
        
    Returns:
        The AI-generated response text
        
    Raises:
        Exception: If API call fails
    """
    try:
        logger.info(f"Sending to AI: {message[:100]}...")
        
        client = get_async_client(api_key)
        
        response = await client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "openai/gpt-oss-120b"),
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
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1000")),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            top_p=1,
            presence_penalty=0,
            frequency_penalty=0,
            timeout=int(os.getenv("LLM_TIMEOUT", "30"))
        )
        
        response_text = response.choices[0].message.content
        
        logger.info(f"Received AI response: {response_text[:100]}...")
        
        return response_text
        
    except Exception as e:
        logger.error(f"Error communicating with AI: {str(e)}")
        raise Exception(f"Failed to get AI response: {str(e)}")

def get_ai_response(message: str) -> str:
    """
    Synchronous version for backward compatibility.
    Uses the API key from environment variable.
    """
    api_key = os.getenv("BASETEN_API_KEY")
    if not api_key:
        raise ValueError("BASETEN_API_KEY environment variable is required")
    
    return asyncio.run(get_ai_response_async(message, api_key))