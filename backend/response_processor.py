"""
Response Processor Module
Handles post-processing of AI responses before sending to frontend
"""
import logging

logger = logging.getLogger(__name__)

def process_response(response: str) -> str:
    """
    Process the AI response before sending to frontend.
    Adds a friendly acknowledgment about the joke.
    
    Args:
        response: The AI-generated response
        
    Returns:
        The processed response with joke acknowledgment
    """
    try:
        # Add joke acknowledgment to the response
        processed_response = f"{response}\n\nI hope you liked the joke!"
        
        logger.info(f"Response processed - Added joke acknowledgment")
        
        # Future enhancements can be added here:
        # - Response filtering
        # - Profanity filtering
        # - Response formatting
        # - Sentiment analysis
        # - Response caching
        
        return processed_response
        
    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")
        # If processing fails, return original response
        return response