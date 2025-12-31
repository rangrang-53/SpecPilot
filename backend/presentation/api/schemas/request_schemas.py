"""Request Schemas"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class StartSessionRequest(BaseModel):
    """세션 시작 요청"""
    initial_input: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="프로젝트 초기 입력 (10-5000자)",
        examples=["온라인 쇼핑몰을 만들고 싶습니다. 상품 관리, 결제, 주문 관리 기능이 필요합니다."]
    )

    @field_validator('initial_input')
    @classmethod
    def validate_initial_input(cls, v: str) -> str:
        """입력 검증 및 정제"""
        v = v.strip()
        if not v:
            raise ValueError("입력이 비어있습니다.")
        if len(v) < 10:
            raise ValueError("입력이 너무 짧습니다. 최소 10자 이상 입력해주세요.")
        if len(v) > 5000:
            raise ValueError("입력이 너무 깁니다. 최대 5000자까지 입력 가능합니다.")
        return v


class ContinueSessionRequest(BaseModel):
    """세션 계속 요청"""
    session_id: str = Field(
        ...,
        min_length=1,
        description="세션 ID"
    )
    user_response: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="사용자 응답 (1-2000자)"
    )

    @field_validator('user_response')
    @classmethod
    def validate_user_response(cls, v: str) -> str:
        """응답 검증 및 정제"""
        v = v.strip()
        if not v:
            raise ValueError("응답이 비어있습니다.")
        if len(v) > 2000:
            raise ValueError("응답이 너무 깁니다. 최대 2000자까지 입력 가능합니다.")
        return v
