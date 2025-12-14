"""SRS Document Models"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class FunctionalRequirement(BaseModel):
    """기능 요구사항 모델"""
    id: str = Field(description="요구사항 ID (예: FR-001)")
    title: str = Field(description="요구사항 제목")
    description: str = Field(description="상세 설명")
    priority: Literal["High", "Medium", "Low"] = Field(description="우선순위")
    tech_suggestions: List[str] = Field(
        default_factory=list,
        description="기술 제안 목록"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "FR-001",
                "title": "사용자 로그인",
                "description": "사용자가 이메일과 비밀번호로 로그인할 수 있다",
                "priority": "High",
                "tech_suggestions": ["JWT", "OAuth2.0"]
            }
        }


class TechStackRecommendation(BaseModel):
    """기술 스택 추천 모델"""
    category: str = Field(description="카테고리 (예: Backend, Frontend)")
    technologies: List[str] = Field(description="추천 기술 목록")
    rationale: str = Field(description="선택 근거")

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Backend",
                "technologies": ["FastAPI", "PostgreSQL", "Redis"],
                "rationale": "빠른 개발과 확장성을 위해 선택"
            }
        }


class GherkinScenario(BaseModel):
    """Gherkin 테스트 시나리오 모델"""
    feature: str = Field(description="기능명")
    scenario: str = Field(description="시나리오명")
    given: str = Field(description="Given 조건")
    when: str = Field(description="When 동작")
    then: str = Field(description="Then 결과")

    class Config:
        json_schema_extra = {
            "example": {
                "feature": "로그인",
                "scenario": "정상 로그인",
                "given": "사용자가 로그인 페이지에 있다",
                "when": "올바른 이메일과 비밀번호를 입력한다",
                "then": "메인 페이지로 이동한다"
            }
        }


class SRSDocument(BaseModel):
    """최종 SRS 문서 모델"""
    project_name: str = Field(description="프로젝트명")
    overview: str = Field(description="프로젝트 개요")
    functional_requirements: List[FunctionalRequirement] = Field(
        description="기능 요구사항 목록"
    )
    non_functional_requirements: List[str] = Field(
        description="비기능 요구사항 목록"
    )
    tech_stack: List[TechStackRecommendation] = Field(
        description="기술 스택 추천 목록"
    )
    test_scenarios: List[GherkinScenario] = Field(
        description="테스트 시나리오 목록"
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="가정 및 제약사항"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "온라인 쇼핑몰",
                "overview": "모바일 최적화된 전자상거래 플랫폼",
                "functional_requirements": [],
                "non_functional_requirements": ["응답시간 1초 이내"],
                "tech_stack": [],
                "test_scenarios": [],
                "assumptions": ["AWS 인프라 사용"]
            }
        }
