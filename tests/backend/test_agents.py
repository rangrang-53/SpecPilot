"""Domain Agents Test Suite"""
import pytest
from backend.domain.models.state import RequirementState, Message
from backend.domain.agents.consultant_agent import consultant_agent
from backend.domain.agents.judge_agent import judge_agent
from backend.domain.agents.writer_agent import writer_agent


class TestConsultantAgent:
    """Consultant Agent 테스트"""

    def test_consultant_agent_generates_questions(self):
        """Consultant가 질문을 생성하는지 테스트"""
        state = RequirementState(user_input="쇼핑몰을 만들고 싶습니다")
        result = consultant_agent(state)

        assert isinstance(result, RequirementState)
        assert len(result.questions) > 0
        assert isinstance(result.questions[0], str)

    def test_consultant_agent_updates_messages(self):
        """Consultant가 메시지를 업데이트하는지 테스트"""
        state = RequirementState(user_input="쇼핑몰을 만들고 싶습니다")
        result = consultant_agent(state)

        # 메시지가 추가되었는지 확인
        assert len(result.messages) > 0

    def test_consultant_agent_with_collected_info(self):
        """수집된 정보가 있을 때 Consultant 동작 테스트"""
        state = RequirementState(
            user_input="결제는 카드만 지원합니다",
            collected_info={"payment": "card"}
        )
        result = consultant_agent(state)

        assert isinstance(result, RequirementState)
        assert len(result.questions) > 0


class TestJudgeAgent:
    """Judge Agent 테스트"""

    def test_judge_agent_incomplete_info(self):
        """정보가 부족할 때 Judge 동작 테스트"""
        state = RequirementState(
            user_input="쇼핑몰",
            collected_info={"feature": "쇼핑"}
        )
        result = judge_agent(state)

        assert isinstance(result, RequirementState)
        assert result.is_complete is False
        assert result.judge_feedback is not None

    def test_judge_agent_complete_info(self):
        """정보가 충분할 때 Judge 동작 테스트"""
        state = RequirementState(
            user_input="쇼핑몰",
            collected_info={
                "core_features": ["상품 등록", "장바구니", "결제"],
                "payment_methods": ["카드", "가상계좌"],
                "expected_users": 10000,
                "authentication": "JWT",
                "deployment": "AWS ECS"
            }
        )
        result = judge_agent(state)

        assert isinstance(result, RequirementState)
        # 더미 구현에서는 항상 complete 처리
        assert result.is_complete is True

    def test_judge_agent_provides_feedback(self):
        """Judge가 피드백을 제공하는지 테스트"""
        state = RequirementState(
            user_input="test",
            collected_info={}
        )
        result = judge_agent(state)

        assert result.judge_feedback is not None
        assert isinstance(result.judge_feedback, str)


class TestWriterAgent:
    """Writer Agent 테스트"""

    def test_writer_agent_generates_srs(self):
        """Writer가 SRS를 생성하는지 테스트"""
        state = RequirementState(
            user_input="쇼핑몰 프로젝트",
            collected_info={
                "project_name": "온라인 쇼핑몰",
                "features": ["상품 관리", "주문 처리"]
            },
            is_complete=True
        )
        result = writer_agent(state)

        assert isinstance(result, RequirementState)
        assert result.final_srs is not None
        assert isinstance(result.final_srs, str)

    def test_writer_agent_with_conversation_history(self):
        """대화 히스토리가 있을 때 Writer 동작 테스트"""
        messages = [
            Message(role="user", content="쇼핑몰을 만들고 싶습니다"),
            Message(role="assistant", content="어떤 기능이 필요한가요?"),
            Message(role="user", content="상품 관리와 결제 기능입니다")
        ]
        state = RequirementState(
            user_input="쇼핑몰",
            messages=messages,
            collected_info={"features": ["상품 관리", "결제"]},
            is_complete=True
        )
        result = writer_agent(state)

        assert result.final_srs is not None
