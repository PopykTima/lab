from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from app.core.config import settings

# Налаштування для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Дістаємо секретні ключі з налаштувань (або використовуємо дефолтні)
SECRET_KEY = getattr(settings, "SECRET_KEY", "super-secret-key-for-lab5")
ALGORITHM = getattr(settings, "ALGORITHM", "HS256")

# Я додав обидві назви функції, бо в users.py ти використовуєш hash_password, 
# а в тестах я бачив get_password_hash. Так працюватиме скрізь!
def hash_password(password: str) -> str:
    # Перетворюємо рядок на байти перед хешуванням, обмежуємо до 72 байтів для bcrypt
    return pwd_context.hash(password.encode("utf-8")[:72])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password.encode("utf-8")[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # При перевірці теж перетворюємо і обмежуємо
    return pwd_context.verify(plain_password.encode("utf-8")[:72], hashed_password)

# Функція створення токена (знадобиться для логіну)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    
    # Беремо секретний ключ з налаштувань, або використовуємо запасний
    secret_key = getattr(settings, "SECRET_KEY", "super-secret-key-for-lab5")
    algorithm = getattr(settings, "ALGORITHM", "HS256")
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt