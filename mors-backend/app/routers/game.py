from fastapi import APIRouter, HTTPException, status

from app.models.roles_registry import ROLES
from app.schemas.game import NewGameRequest, NewGameResponse, TurnRequest, TurnResponse
from app.services.game_service import GameService


router = APIRouter(prefix="/game", tags=["game"])
_game_service: GameService | None = None


def _get_game_service() -> GameService:
    global _game_service
    if _game_service is None:
        _game_service = GameService()
    return _game_service


@router.post("/new", response_model=NewGameResponse, status_code=status.HTTP_201_CREATED)
async def new_game(request: NewGameRequest | None = None):
    service = _get_game_service()
    role_id = request.role if request else ""

    # Validate role if provided
    if role_id and role_id not in ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown role: {role_id}",
        )

    state, narrative = service.new_game(role_id=role_id)

    role_display_name = ""
    role_difficulty = ""
    if role_id and role_id in ROLES:
        role_def = ROLES[role_id]
        role_display_name = role_def.display_name
        role_difficulty = role_def.difficulty

    return NewGameResponse(
        session_id=state.session_id,
        state=state,
        narrative=narrative,
        role_display_name=role_display_name,
        role_difficulty=role_difficulty,
    )


@router.post("/turn", response_model=TurnResponse)
async def turn(request: TurnRequest):
    service = _get_game_service()
    try:
        result = service.process_turn(request.session_id, request.action)
        return TurnResponse(
            new_state=result.new_state,
            deltas=result.deltas,
            event=result.event,
            narrative=result.narrative,
            epitaph=result.epitaph,
            is_terminal=result.is_terminal,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/state/{session_id}")
async def get_state(session_id: str):
    service = _get_game_service()
    state = service.get_state(session_id)
    if state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return {"state": state}
