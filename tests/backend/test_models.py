"""Domain Models Test Suite"""
import pytest
from datetime import datetime
from backend.domain.models.state import Message, RequirementState
from backend.domain.models.agent_response import ConsultantResponse, JudgeResponse
from backend.domain.models.srs import (
    FunctionalRequirement,
    TechStackRecommendation,
    GherkinScenario,
    SRSDocument,
)


class TestMessage:
    """Message 모델 테스트"""

    def test_message_creation(self):
        """Message 생성 테스트"""
        message = Message(
            role="user",
            content="테스트 메시지"
        )
        assert message.role == "user"
        assert message.content == "테스트 메시지"
        assert message.timestamp is None

    def test_message_with_timestamp(self):
        """Timestamp 포함 Message 테스트"""
        ts = "2025-12-14T17:30:00Z"
        message = Message(
            role="assistant",
            content="응답 메시지",
            timestamp=ts
        )
        assert message.timestamp == ts

    def test_message_role_validation(self):
        """Role 유효성 검증 테스트"""
        valid_roles = ["user", "assistant", "system"]
        for role in valid_roles:
            message = Message(role=role, content="test")
            assert message.role == role


class TestRequirementState:
    """RequirementState 모델 테스트"""

    def test_state_initialization(self):
        """State 초기화 테스트"""
        state = RequirementState(user_input="쇼핑몰 만들기")
        assert state.user_input == "쇼핑몰 만들기"
        assert state.messages == []
        assert state.collected_info == {}
        assert state.questions == []
        assert state.is_complete is False
        assert state.judge_feedback is None
        assert state.final_srs is None
        assert state.iteration_count == 0

    def test_state_with_messages(self):
        """메시지 포함 State 테스트"""
        messages = [
            Message(role="user", content="안녕하세요")
        ]
        state = RequirementState(
            user_input="test",
            messages=messages
        )
        assert len(state.messages) == 1
        assert state.messages[0].content == "안녕하세요"


class TestConsultantResponse:
    """ConsultantResponse 모델 테스트"""

    def test_consultant_response_creation(self):
        """ConsultantResponse 생성 테스트"""
        response = ConsultantResponse(
            questions=["질문1", "질문2", "질문3"],
            reasoning="이 질문들이 필요한 이유"
        )
        assert len(response.questions) == 3
        assert response.reasoning == "이 질문들이 필요한 이유"


class TestJudgeResponse:
    """JudgeResponse 모델 테스트"""

    def test_judge_response_approve(self):
        """승인 응답 테스트"""
        response = JudgeResponse(
            decision="approve",
            completeness_score=0.85,
            missing_areas=[],
            feedback="충분한 정보가 수집되었습니다"
        )
        assert response.decision == "approve"
        assert response.completeness_score == 0.85
        assert response.missing_areas == []

    def test_judge_response_reject(self):
        """거절 응답 테스트"""
        response = JudgeResponse(
            decision="reject",
            completeness_score=0.45,
            missing_areas=["기술 스택", "예상 사용자 수"],
            feedback="추가 정보가 필요합니다"
        )
        assert response.decision == "reject"
        assert len(response.missing_areas) == 2


class TestFunctionalRequirement:
    """FunctionalRequirement 모델 테스트"""

    def test_functional_requirement_creation(self):
        """기능 요구사항 생성 테스트"""
        req = FunctionalRequirement(
            id="FR-001",
            title="사용자 로그인",
            description="사용자가 이메일과 비밀번호로 로그인할 수 있다",
            priority="High",
            tech_suggestions=["JWT", "OAuth2.0"]
        )
        assert req.id == "FR-001"
        assert req.priority == "High"
        assert len(req.tech_suggestions) == 2


class TestTechStackRecommendation:
    """TechStackRecommendation 모델 테스트"""

    def test_tech_stack_creation(self):
        """기술 스택 추천 생성 테스트"""
        tech = TechStackRecommendation(
            category="Backend",
            technologies=["FastAPI", "PostgreSQL"],
            rationale="빠른 개발과 확장성을 위해"
        )
        assert tech.category == "Backend"
        assert len(tech.technologies) == 2
        assert "FastAPI" in tech.technologies


class TestGherkinScenario:
    """GherkinScenario 모델 테스트"""

    def test_gherkin_scenario_creation(self):
        """Gherkin 시나리오 생성 테스트"""
        scenario = GherkinScenario(
            feature="로그인",
            scenario="정상 로그인",
            given="사용자가 로그인 페이지에 있다",
            when="올바른 이메일과 비밀번호를 입력한다",
            then="메인 페이지로 이동한다"
        )
        assert scenario.feature == "로그인"
        assert scenario.scenario == "정상 로그인"


class TestSRSDocument:
    """SRSDocument 모델 테스트"""

    def test_srs_document_creation(self):
        """SRS 문서 생성 테스트"""
        srs = SRSDocument(
            project_name="쇼핑몰 프로젝트",
            overview="온라인 쇼핑몰 시스템",
            functional_requirements=[],
            non_functional_requirements=["성능: 1초 이내 응답"],
            tech_stack=[],
            test_scenarios=[],
            assumptions=["AWS 인프라 사용"]
        )
        assert srs.project_name == "쇼핑몰 프로젝트"
        assert len(srs.non_functional_requirements) == 1
        assert len(srs.assumptions) == 1

    def test_srs_document_with_requirements(self):
        """요구사항 포함 SRS 문서 테스트"""
        req = FunctionalRequirement(
            id="FR-001",
            title="로그인",
            description="사용자 로그인 기능",
            priority="High"
        )
        srs = SRSDocument(
            project_name="Test",
            overview="Test project",
            functional_requirements=[req],
            non_functional_requirements=[],
            tech_stack=[],
            test_scenarios=[]
        )
        assert len(srs.functional_requirements) == 1
        assert srs.functional_requirements[0].id == "FR-001"
