"""Dummy Executor - 더미 구현"""
import uuid
from typing import Optional
from backend.domain.models.state import RequirementState, Message
from backend.infrastructure.graph.workflow import DummyWorkflow
from backend.infrastructure.graph.session_repository import DummySessionRepository
from backend.utils.info_extractor import InfoExtractor


# 전역 공유 repository (싱글톤 패턴)
_shared_repository = DummySessionRepository()


class DummyExecutor:
    """
    워크플로우 실행기 더미 구현

    세션 관리와 워크플로우 실행을 담당합니다.
    """

    def __init__(self):
        """Executor 초기화"""
        self.workflow = DummyWorkflow()
        self.repository = _shared_repository
        self.info_extractor = InfoExtractor()

    def create_session(self) -> str:
        """
        새로운 세션 생성

        Returns:
            생성된 세션 ID (UUID)
        """
        session_id = str(uuid.uuid4())
        return session_id

    def execute(self, session_id: str, user_input: str) -> RequirementState:
        """
        워크플로우 실행

        Args:
            session_id: 세션 ID
            user_input: 사용자 입력

        Returns:
            업데이트된 요구사항 상태
        """
        # 1. 기존 상태 로드 또는 새로운 상태 생성
        state = self.repository.load(session_id)
        if state is None:
            state = RequirementState(user_input=user_input)
        else:
            # 기존 세션이면 user_input 업데이트
            state.user_input = user_input

        # 2. 사용자 입력에서 정보 추출 및 collected_info 업데이트
        extracted_info = self.info_extractor.extract(user_input, state.collected_info)
        state.collected_info.update(extracted_info)

        # 3. 사용자 메시지 추가
        state.messages.append(
            Message(role="user", content=user_input)
        )

        # 4. 워크플로우 실행
        state = self.workflow.run(state)

        # 5. 상태 저장
        self.repository.save(session_id, state)

        return state

    def get_state(self, session_id: str) -> Optional[RequirementState]:
        """
        세션 상태 조회

        Args:
            session_id: 세션 ID

        Returns:
            요구사항 상태 또는 None
        """
        return self.repository.load(session_id)
