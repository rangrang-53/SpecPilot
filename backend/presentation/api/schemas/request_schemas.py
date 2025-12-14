"""Request Schemas"""
from pydantic import BaseModel


class StartSessionRequest(BaseModel):
    """세션 시작 요청"""
    initial_input: str


class ContinueSessionRequest(BaseModel):
    """세션 계속 요청"""
    session_id: str
    user_response: str
