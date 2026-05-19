from fastapi import APIRouter, HTTPException, status

from app.services.session_service import SessionService


router = APIRouter(prefix="/game", tags=["session"])
_session_service: SessionService | None = None


def _get_session_service() -> SessionService:
    global _session_service
    if _session_service is None:
        _session_service = SessionService()
    return _session_service


@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str):
    service = _get_session_service()
    service.delete_session(session_id)
    return None


@router.get("/sessions")
async def list_sessions():
    service = _get_session_service()
    sessions = service.list_sessions()
    return {"sessions": sessions, "count": len(sessions)}