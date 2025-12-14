"""Agent Response Models"""
from typing import List, Literal
from pydantic import BaseModel, Field


class ConsultantResponse(BaseModel):
    """Consultant Agent 응답 모델"""
    questions: List[str] = Field(
        description="생성된 질문 리스트"
    )
    reasoning: str = Field(
        description="왜 이 질문들이 필요한지 설명"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "questions": [
                    "결제 수단은 어떤 것을 지원하나요?",
                    "예상되는 일일 주문 건수는 얼마나 되나요?"
                ],
                "reasoning": "결제 시스템과 성능 요구사항을 파악하기 위해"
            }
        }


class JudgeResponse(BaseModel):
    """Judge Agent 응답 모델"""
    decision: Literal["approve", "reject"] = Field(
        description="승인 또는 거절"
    )
    completeness_score: float = Field(
        ge=0.0,
        le=1.0,
        description="완전성 점수 (0.0 ~ 1.0)"
    )
    missing_areas: List[str] = Field(
        default_factory=list,
        description="부족한 정보 영역"
    )
    feedback: str = Field(
        description="평가 피드백"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "decision": "reject",
                "completeness_score": 0.45,
                "missing_areas": ["기술 스택", "예상 사용자 수"],
                "feedback": "추가 정보가 필요합니다"
            }
        }
