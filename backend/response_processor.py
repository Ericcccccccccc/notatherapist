"""
Response Processor Module
Handles post-processing of AI responses before sending to frontend
"""
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

async def process_response_async(response: str) -> str:
    """
    Process the AI response before sending to frontend (async version).
    Adds a friendly acknowledgment about the joke.
    
    Args:
        response: The AI-generated response
        
    Returns:
        The processed response with joke acknowledgment
    """
    try:
        # Simulate async processing if needed (e.g., content filtering API)
        # await asyncio.sleep(0)  # Placeholder for actual async operations
        
        # Add joke acknowledgment to the response
        processed_response = f"{response}\n\nI hope you liked the joke!"
        
        logger.info(f"Response processed - Added joke acknowledgment")
        
        # Future async enhancements can be added here:
        # - Async response filtering services
        # - Async profanity filtering API
        # - Async response formatting
        # - Async sentiment analysis service
        # - Async response caching via Redis
        
        return processed_response
        
    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")
        # If processing fails, return original response
        return response

def process_response(response: str) -> str:
    """
    Synchronous version for backward compatibility.
    """
    return asyncio.run(process_response_async(response))