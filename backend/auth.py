"""
Authentication Module
Handles user authentication and session management
"""
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import secrets
import logging

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)  # Generate a random secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory session store (for simple implementation)
# In production, use Redis or a database
sessions: Dict[str, dict] = {}

class LoginRequest(BaseModel):
    name: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    name: str
    token: str
    message: str

class AuthCheckResponse(BaseModel):
    authenticated: bool
    name: Optional[str] = None

def validate_login(name: str, password: str) -> bool:
    """
    Validate login credentials.
    Returns True if name is not empty and password is "password"
    """
    # Strip whitespace and enforce max length
    name = name.strip()[:32]
    password = password.strip()[:32]
    
    if not name or not password:
        return False
    
    # Check if password is exactly "password"
    return password == "password"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def authenticate_user(name: str, password: str) -> Optional[dict]:
    """
    Authenticate a user with name and password.
    Returns user info if successful, None otherwise.
    """
    # Strip and validate inputs
    name = name.strip()[:32]
    password = password.strip()[:32]
    
    if not name or not password:
        logger.warning(f"Login attempt with empty credentials")
        return None
    
    if password.lower() != "password":
        logger.warning(f"Login attempt with incorrect password for user: {name}")
        return None
    
    # Create user session
    user_info = {
        "name": name,
        "login_time": datetime.utcnow().isoformat()
    }
    
    logger.info(f"User authenticated successfully: {name}")
    return user_info

def create_session(user_info: dict) -> str:
    """Create a session and return session token"""
    token = create_access_token(data={"sub": user_info["name"]})
    sessions[token] = user_info
    return token

def get_session(token: str) -> Optional[dict]:
    """Get session info from token"""
    # First verify the token is valid
    payload = verify_token(token)
    if not payload:
        return None
    
    # Check if session exists
    if token in sessions:
        return sessions[token]
    
    # If token is valid but session doesn't exist, create one
    # This handles server restarts
    user_info = {
        "name": payload.get("sub"),
        "login_time": datetime.utcnow().isoformat()
    }
    sessions[token] = user_info
    return user_info

def remove_session(token: str):
    """Remove a session"""
    if token in sessions:
        del sessions[token]