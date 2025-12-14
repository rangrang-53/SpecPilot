"""Requirement State Models"""
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    """대화 메시지 모델"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "온라인 쇼핑몰을 만들고 싶습니다",
                "timestamp": "2025-12-14T17:30:00Z"
            }
        }


class RequirementState(BaseModel):
    """LangGraph State 객체"""
    # 사용자 입력
    user_input: str

    # 대화 히스토리
    messages: List[Message] = Field(default_factory=list)

    # 수집된 요구사항 정보
    collected_info: Dict[str, Any] = Field(default_factory=dict)

    # Consultant가 생성한 질문
    questions: List[str] = Field(default_factory=list)

    # Judge의 평가 결과
    is_complete: bool = False
    judge_feedback: Optional[str] = None

    # 최종 SRS 문서
    final_srs: Optional[str] = None

    # 반복 횟수 (무한 루프 방지)
    iteration_count: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "user_input": "쇼핑몰을 만들고 싶습니다",
                "messages": [],
                "collected_info": {},
                "questions": [],
                "is_complete": False,
                "iteration_count": 0
            }
        }
