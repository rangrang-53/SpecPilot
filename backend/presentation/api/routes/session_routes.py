"""Session Routes"""
from fastapi import APIRouter, HTTPException
from backend.presentation.api.schemas.request_schemas import (
    StartSessionRequest,
    ContinueSessionRequest,
)
from backend.presentation.api.schemas.response_schemas import (
    SessionResponse,
    SessionStatusResponse,
    CollectedInfoResponse,
    ResetResponse,
)
from backend.application.use_cases.start_session_use_case import StartSessionUseCase
from backend.application.use_cases.continue_session_use_case import ContinueSessionUseCase
from backend.application.use_cases.reset_session_use_case import ResetSessionUseCase
from backend.infrastructure.graph.executor import DummyExecutor

router = APIRouter(prefix="/api/session", tags=["session"])


@router.post("/start", response_model=SessionResponse)
def start_session(request: StartSessionRequest):
    """세션 시작"""
    use_case = StartSessionUseCase()
    result = use_case.execute(request.initial_input)
    return SessionResponse(**result)


@router.post("/continue", response_model=SessionResponse)
def continue_session(request: ContinueSessionRequest):
    """세션 계속"""
    use_case = ContinueSessionUseCase()
    result = use_case.execute(request.session_id, request.user_response)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return SessionResponse(**result)


@router.get("/{session_id}/status", response_model=SessionStatusResponse)
def get_session_status(session_id: str):
    """세션 상태 조회"""
    executor = DummyExecutor()
    state = executor.get_state(session_id)

    if state is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionStatusResponse(
        session_id=session_id,
        is_complete=state.is_complete,
        iteration_count=state.iteration_count,
    )


@router.post("/{session_id}/reset", response_model=ResetResponse)
def reset_session(session_id: str):
    """세션 리셋"""
    use_case = ResetSessionUseCase()
    result = use_case.execute(session_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return ResetResponse(**result)


@router.get("/{session_id}/collected-info", response_model=CollectedInfoResponse)
def get_collected_info(session_id: str):
    """수집된 정보 조회"""
    executor = DummyExecutor()
    state = executor.get_state(session_id)

    if state is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return CollectedInfoResponse(
        session_id=session_id,
        collected_info=state.collected_info,
    )
