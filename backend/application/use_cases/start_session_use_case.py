"""Start Session Use Case"""
from typing import Dict, Any
from backend.infrastructure.graph.executor import DummyExecutor


class StartSessionUseCase:
    """
    세션 시작 Use Case

    새로운 요구사항 수집 세션을 시작합니다.
    """

    def __init__(self):
        """Use Case 초기화"""
        self.executor = DummyExecutor()

    def execute(self, initial_input: str) -> Dict[str, Any]:
        """
        세션 시작 실행

        Args:
            initial_input: 초기 사용자 입력

        Returns:
            세션 정보 및 첫 질문
        """
        # 새 세션 생성
        session_id = self.executor.create_session()

        # 워크플로우 실행
        state = self.executor.execute(session_id, initial_input)

        # 결과 반환
        return {
            "session_id": session_id,
            "questions": state.questions,
            "is_complete": state.is_complete,
            "iteration_count": state.iteration_count,
        }
