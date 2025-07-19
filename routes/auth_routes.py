from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from controllers.auth_controller import (
    create_new_session,
    logout_session,
    refresh_user_session,
    get_session_info,
    get_sessions_stats,
    SessionCreateRequest,
)
from middleware.auth import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()
security = HTTPBearer()


@router.post("/login", status_code=status.HTTP_201_CREATED)
def login(request: SessionCreateRequest = None):
    return create_new_session(request)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(jwt_bearer)):
    return logout_session(token)


@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(token: str = Depends(jwt_bearer)):
    return refresh_user_session(token)


@router.get("/session", status_code=status.HTTP_200_OK)
def get_current_session(token: str = Depends(jwt_bearer)):
    return get_session_info(token)


@router.get("/sessions/stats", status_code=status.HTTP_200_OK)
def session_statistics():
    return get_sessions_stats()