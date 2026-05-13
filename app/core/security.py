from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = getattr(settings, "SECRET_KEY", "super-secret-key-for-lab5")
ALGORITHM = getattr(settings, "ALGORITHM", "HS256")
def hash_password(password: str) -> str:
    return pwd_context.hash(password.encode("utf-8")[:72])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password.encode("utf-8")[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password.encode("utf-8")[:72], hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    
    secret_key = getattr(settings, "SECRET_KEY", "super-secret-key-for-lab5")
    algorithm = getattr(settings, "ALGORITHM", "HS256")
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt