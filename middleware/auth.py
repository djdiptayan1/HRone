from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Optional
import uuid

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

active_sessions = {}

security = HTTPBearer()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token.",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )

    def verify_jwt(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            session_id = payload.get("session_id")

            if session_id and session_id in active_sessions:
                session = active_sessions[session_id]
                if session["expires_at"] > datetime.utcnow():
                    return True
                else:
                    del active_sessions[session_id]
            return False
        except JWTError:
            return False


def create_session(user_data: dict = None) -> str:
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Store session data
    active_sessions[session_id] = {
        "session_id": session_id,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "user_data": user_data or {},
    }

    token_data = {"session_id": session_id, "exp": expires_at, "iat": datetime.utcnow()}

    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_session_data(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        session_id = payload.get("session_id")

        if session_id and session_id in active_sessions:
            session = active_sessions[session_id]
            if session["expires_at"] > datetime.utcnow():
                return session
            else:
                del active_sessions[session_id]

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def invalidate_session(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        session_id = payload.get("session_id")

        if session_id and session_id in active_sessions:
            del active_sessions[session_id]
            return True
        return False
    except JWTError:
        return False


def get_current_session(token: str = Depends(JWTBearer())):
    return get_session_data(token)


def refresh_session(token: str) -> str:
    session_data = get_session_data(token)
    invalidate_session(token)

    return create_session(session_data.get("user_data", {}))


def get_active_sessions_count() -> int:
    current_time = datetime.utcnow()
    expired_sessions = [
        session_id
        for session_id, session in active_sessions.items()
        if session["expires_at"] <= current_time
    ]

    for session_id in expired_sessions:
        del active_sessions[session_id]

    return len(active_sessions)
