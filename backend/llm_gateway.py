"""
LLM Gateway Module
Handles communication with Baseten AI service
"""
from openai import OpenAI
import os
import logging

logger = logging.getLogger(__name__)

# Initialize Baseten client
api_key = os.getenv("BASETEN_API_KEY")
if not api_key:
    raise ValueError("BASETEN_API_KEY environment variable is required")

client = OpenAI(
    api_key=api_key,
    base_url="https://inference.baseten.co/v1"
)

def get_ai_response(message: str) -> str:
    """
    Send message to Baseten AI and get response.
    
    Args:
        message: The processed message to send to AI
        
    Returns:
        The AI-generated response text
    """
    try:
        logger.info(f"Sending to AI: {message[:100]}...")
        
        response = client.chat.completions.create(
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