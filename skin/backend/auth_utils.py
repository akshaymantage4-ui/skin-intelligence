from datetime import datetime, timedelta, UTC
from jose import jwt
from config import SECRET_KEY, ALGORITHM

def create_access_token(user_id: int, email: str, role: str):
    payload = {"user_id": user_id, "email": email, "role": role, "exp": datetime.now(UTC) + timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
