"""Infrastructure Graph Test Suite"""
import pytest
from backend.domain.models.state import RequirementState, Message
from backend.infrastructure.graph.workflow import DummyWorkflow
from backend.infrastructure.graph.executor import DummyExecutor
from backend.infrastructure.graph.session_repository import DummySessionRepository


class TestDummyWorkflow:
    """DummyWorkflow 테스트"""

    def test_workflow_initialization(self):
        """Workflow가 초기화되는지 테스트"""
        workflow = DummyWorkflow()
        assert workflow is not None

    def test_workflow_has_agents(self):
        """Workflow가 에이전트들을 포함하는지 테스트"""
        workflow = DummyWorkflow()
        assert hasattr(workflow, 'consultant_agent')
        assert hasattr(workflow, 'judge_agent')
        assert hasattr(workflow, 'writer_agent')

    def test_workflow_run_incomplete_path(self):
        """정보가 불완전할 때 Workflow 실행 테스트"""
        workflow = DummyWorkflow()
        state = RequirementState(user_input="쇼핑몰을 만들고 싶습니다")
        result = workflow.run(state)

        assert isinstance(result, RequirementState)
        # 정보가 불완전하므로 is_complete는 False
        assert result.is_complete is False
        # Consultant가 질문을 생성했어야 함
        assert len(result.questions) > 0

    def test_workflow_run_complete_path(self):
        """정보가 충분할 때 Workflow 실행 테스트"""
        workflow = DummyWorkflow()
        state = RequirementState(
            user_input="쇼핑몰 프로젝트",
            collected_info={
                "project_name": "BuyGo",
                "payment": "카드",
                "scale": "200건",
                "authentication": "소셜 로그인",
                "deployment": "AWS"
            }
        )
        result = workflow.run(state)

        assert isinstance(result, RequirementState)
        # 정보가 충분하므로 (5개 이상) is_complete는 True
        assert result.is_complete is True
        # Writer가 SRS를 생성했어야 함
        assert result.final_srs is not None

    def test_workflow_preserves_iteration_count(self):
        """Workflow가 iteration count를 증가시키는지 테스트"""
        workflow = DummyWorkflow()
        state = RequirementState(user_input="test", iteration_count=0)
        result = workflow.run(state)

        assert result.iteration_count >= state.iteration_count


class TestDummyExecutor:
    """DummyExecutor 테스트"""

    def test_executor_initialization(self):
        """Executor가 초기화되는지 테스트"""
        executor = DummyExecutor()
        assert executor is not None

    def test_executor_create_session(self):
        """Executor가 세션을 생성하는지 테스트"""
        executor = DummyExecutor()
        session_id = executor.create_session()

        assert session_id is not None
        assert isinstance(session_id, str)
        assert len(session_id) > 0

    def test_executor_execute_workflow(self):
        """Executor가 워크플로우를 실행하는지 테스트"""
        executor = DummyExecutor()
        session_id = executor.create_session()
        user_input = "쇼핑몰을 만들고 싶습니다"

        result = executor.execute(session_id, user_input)

        assert isinstance(result, RequirementState)
        assert result.user_input == user_input

    def test_executor_get_state(self):
        """Executor가 세션 상태를 조회하는지 테스트"""
        executor = DummyExecutor()
        session_id = executor.create_session()
        user_input = "test input"

        # 워크플로우 실행
        executor.execute(session_id, user_input)

        # 상태 조회
        state = executor.get_state(session_id)
        assert state is not None
        assert isinstance(state, RequirementState)

    def test_executor_nonexistent_session(self):
        """존재하지 않는 세션 조회 시 None 반환 테스트"""
        executor = DummyExecutor()
        state = executor.get_state("nonexistent-session-id")
        assert state is None

    def test_executor_resume_session(self):
        """Executor가 세션을 재개하는지 테스트"""
        executor = DummyExecutor()
        session_id = executor.create_session()

        # 첫 번째 실행
        executor.execute(session_id, "첫 번째 입력")

        # 세션 재개
        result = executor.execute(session_id, "두 번째 입력")

        assert isinstance(result, RequirementState)
        assert len(result.messages) > 0


class TestDummySessionRepository:
    """DummySessionRepository 테스트"""

    def test_repository_initialization(self):
        """Repository가 초기화되는지 테스트"""
        repo = DummySessionRepository()
        assert repo is not None

    def test_repository_save_and_load(self):
        """Repository가 세션을 저장하고 불러오는지 테스트"""
        repo = DummySessionRepository()
        session_id = "test-session-123"
        state = RequirementState(user_input="test")

        # 저장
        success = repo.save(session_id, state)
        assert success is True

        # 불러오기
        loaded_state = repo.load(session_id)
        assert loaded_state is not None
        assert isinstance(loaded_state, RequirementState)
        assert loaded_state.user_input == "test"

    def test_repository_load_nonexistent_session(self):
        """존재하지 않는 세션 로드 시 None 반환 테스트"""
        repo = DummySessionRepository()
        loaded_state = repo.load("nonexistent-session")
        assert loaded_state is None

    def test_repository_delete_session(self):
        """Repository가 세션을 삭제하는지 테스트"""
        repo = DummySessionRepository()
        session_id = "test-session-456"
        state = RequirementState(user_input="test")

        # 저장
        repo.save(session_id, state)

        # 삭제
        deleted = repo.delete(session_id)
        assert deleted is True

        # 삭제 후 로드하면 None
        loaded_state = repo.load(session_id)
        assert loaded_state is None

    def test_repository_delete_nonexistent_session(self):
        """존재하지 않는 세션 삭제 시 False 반환 테스트"""
        repo = DummySessionRepository()
        deleted = repo.delete("nonexistent-session")
        assert deleted is False

    def test_repository_list_sessions(self):
        """Repository가 모든 세션을 나열하는지 테스트"""
        repo = DummySessionRepository()

        # 여러 세션 저장
        repo.save("session-1", RequirementState(user_input="test1"))
        repo.save("session-2", RequirementState(user_input="test2"))
        repo.save("session-3", RequirementState(user_input="test3"))

        # 세션 목록 조회
        session_ids = repo.list_sessions()
        assert isinstance(session_ids, list)
        assert len(session_ids) >= 3
        assert "session-1" in session_ids
        assert "session-2" in session_ids
        assert "session-3" in session_ids
