from fastapi import HTTPException, status
from middleware.auth import (
    create_session,
    invalidate_session,
    refresh_session,
    get_active_sessions_count,
    get_session_data,
)
from pydantic import BaseModel
from typing import Optional


class SessionCreateRequest(BaseModel):
    user_id: Optional[str] = None
    metadata: Optional[dict] = None


class SessionResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


def create_new_session(request: SessionCreateRequest = None):
    try:
        user_data = {}
        if request:
            if request.user_id:
                user_data["user_id"] = request.user_id
            if request.metadata:
                user_data.update(request.metadata)

        token = create_session(user_data)

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 1800,
            "message": "Session created successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}",
        )


def logout_session(token: str):
    try:
        success = invalidate_session(token)
        if success:
            return {"message": "Session invalidated successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or already expired",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invalidate session: {str(e)}",
        )


def refresh_user_session(token: str):
    try:
        new_token = refresh_session(token)

        return {
            "access_token": new_token,
            "token_type": "bearer",
            "expires_in": 1800,
            "message": "Session refreshed successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh session: {str(e)}",
        )


def get_session_info(token: str):
    try:
        session_data = get_session_data(token)

        return {
            "session_id": session_data["session_id"],
            "created_at": session_data["created_at"].isoformat(),
            "expires_at": session_data["expires_at"].isoformat(),
            "user_data": session_data.get("user_data", {}),
            "is_active": True,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session info: {str(e)}",
        )


def get_sessions_stats():
    try:
        active_count = get_active_sessions_count()

        return {
            "active_sessions": active_count,
            "message": "Session statistics retrieved successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session stats: {str(e)}",
        )
