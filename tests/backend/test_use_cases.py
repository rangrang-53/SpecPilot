"""Use Cases Test Suite"""
import pytest
from backend.application.use_cases.start_session_use_case import StartSessionUseCase
from backend.application.use_cases.continue_session_use_case import ContinueSessionUseCase
from backend.application.use_cases.get_srs_use_case import GetSRSUseCase
from backend.application.use_cases.reset_session_use_case import ResetSessionUseCase
from backend.domain.models.state import RequirementState


class TestStartSessionUseCase:
    """StartSessionUseCase 테스트"""

    def test_use_case_initialization(self):
        """Use Case가 초기화되는지 테스트"""
        use_case = StartSessionUseCase()
        assert use_case is not None

    def test_execute_creates_session(self):
        """세션 생성 실행 테스트"""
        use_case = StartSessionUseCase()
        result = use_case.execute("쇼핑몰을 만들고 싶습니다")

        assert "session_id" in result
        assert "questions" in result
        assert "is_complete" in result
        assert isinstance(result["session_id"], str)
        assert isinstance(result["questions"], list)

    def test_execute_returns_questions(self):
        """질문이 반환되는지 테스트"""
        use_case = StartSessionUseCase()
        result = use_case.execute("온라인 쇼핑몰")

        assert len(result["questions"]) > 0


class TestContinueSessionUseCase:
    """ContinueSessionUseCase 테스트"""

    def test_use_case_initialization(self):
        """Use Case가 초기화되는지 테스트"""
        use_case = ContinueSessionUseCase()
        assert use_case is not None

    def test_execute_continues_session(self):
        """세션 계속 실행 테스트"""
        # 먼저 세션 생성
        start_use_case = StartSessionUseCase()
        start_result = start_use_case.execute("쇼핑몰")
        session_id = start_result["session_id"]

        # 세션 계속
        continue_use_case = ContinueSessionUseCase()
        result = continue_use_case.execute(session_id, "카드와 가상계좌 지원")

        assert "session_id" in result
        assert result["session_id"] == session_id

    def test_nonexistent_session_returns_error(self):
        """존재하지 않는 세션 처리 테스트"""
        use_case = ContinueSessionUseCase()
        result = use_case.execute("nonexistent-id", "답변")

        assert "error" in result or "session_id" in result


class TestGetSRSUseCase:
    """GetSRSUseCase 테스트"""

    def test_use_case_initialization(self):
        """Use Case가 초기화되는지 테스트"""
        use_case = GetSRSUseCase()
        assert use_case is not None

    def test_execute_returns_srs(self):
        """SRS 조회 실행 테스트"""
        # 세션 생성
        start_use_case = StartSessionUseCase()
        start_result = start_use_case.execute("테스트 프로젝트")
        session_id = start_result["session_id"]

        # SRS 조회
        get_srs_use_case = GetSRSUseCase()
        result = get_srs_use_case.execute(session_id)

        assert "session_id" in result
        assert result["session_id"] == session_id

    def test_nonexistent_session_returns_error(self):
        """존재하지 않는 세션의 SRS 조회 테스트"""
        use_case = GetSRSUseCase()
        result = use_case.execute("nonexistent-id")

        assert "error" in result or "session_id" in result


class TestResetSessionUseCase:
    """ResetSessionUseCase 테스트"""

    def test_use_case_initialization(self):
        """Use Case가 초기화되는지 테스트"""
        use_case = ResetSessionUseCase()
        assert use_case is not None

    def test_execute_resets_session(self):
        """세션 리셋 실행 테스트"""
        # 세션 생성
        start_use_case = StartSessionUseCase()
        start_result = start_use_case.execute("테스트")
        session_id = start_result["session_id"]

        # 세션 리셋
        reset_use_case = ResetSessionUseCase()
        result = reset_use_case.execute(session_id)

        assert "message" in result or "session_id" in result

    def test_nonexistent_session_reset(self):
        """존재하지 않는 세션 리셋 테스트"""
        use_case = ResetSessionUseCase()
        result = use_case.execute("nonexistent-id")

        assert "error" in result or "message" in result
