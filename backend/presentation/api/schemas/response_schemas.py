"""Response Schemas"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class SessionResponse(BaseModel):
    """세션 응답"""
    session_id: str
    questions: List[str] = []
    is_complete: bool = False
    iteration_count: int = 0
    judge_feedback: Optional[str] = None
    final_srs: Optional[str] = None


class SessionStatusResponse(BaseModel):
    """세션 상태 응답"""
    session_id: str
    is_complete: bool
    iteration_count: int


class SRSResponse(BaseModel):
    """SRS 응답"""
    session_id: str
    final_srs: Optional[str]
    is_complete: bool


class CollectedInfoResponse(BaseModel):
    """수집된 정보 응답"""
    session_id: str
    collected_info: Dict[str, Any]


class ResetResponse(BaseModel):
    """리셋 응답"""
    message: str
    session_id: str


class ErrorResponse(BaseModel):
    """에러 응답"""
    error: str
    session_id: Optional[str] = None
