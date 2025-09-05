"""
Input Processor Module
Handles preprocessing of user messages before sending to LLM
"""
import logging

logger = logging.getLogger(__name__)

def process_input(message: str) -> str:
    """
    Process the input message before sending to LLM.
    Adds a request for the AI to include a joke in the same language.
    
    Args:
        message: The original user message
        
    Returns:
        The processed message with joke request appended
    """
    try:
        # Add joke request to the message
        processed_message = f"{message}\n\n<<also tell a joke in whatever language the initial prompt was in>>"
        
        logger.info(f"Input processed - Added joke request to message")
        
        # Future enhancements can be added here:
        # - Content moderation
        # - Language detection
        # - Input validation
        # - Rate limiting checks
        
        return processed_message
        
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        # If processing fails, return original message
        return message