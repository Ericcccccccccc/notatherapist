"""
Input Processor Module
Handles preprocessing of user messages before sending to LLM
"""
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

async def process_input_async(message: str) -> str:
    """
    Process the input message before sending to LLM (async version).
    Adds a request for the AI to include a joke in the same language.
    
    Args:
        message: The original user message
        
    Returns:
        The processed message with joke request appended
    """
    try:
        # Simulate async processing if needed (e.g., content moderation API calls)
        # await asyncio.sleep(0)  # Placeholder for actual async operations
        
        # Add joke request to the message
        processed_message = f"{message}\n\n<<also tell a joke in whatever language the initial prompt was in>>"
        
        logger.info(f"Input processed - Added joke request to message")
        
        # Future async enhancements can be added here:
        # - Async content moderation API
        # - Async language detection service
        # - Async input validation
        # - Async rate limiting checks via Redis
        
        return processed_message
        
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        # If processing fails, return original message
        return message

def process_input(message: str) -> str:
    """
    Synchronous version for backward compatibility.
    """
    return asyncio.run(process_input_async(message))