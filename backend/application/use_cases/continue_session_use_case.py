"""Continue Session Use Case"""
from typing import Dict, Any, Optional
from backend.infrastructure.graph.executor import DummyExecutor


class ContinueSessionUseCase:
    """
    세션 계속 Use Case

    기존 세션에 사용자 응답을 추가하고 워크플로우를 계속 진행합니다.
    """

    def __init__(self):
        """Use Case 초기화"""
        self.executor = DummyExecutor()

    def execute(self, session_id: str, user_response: str) -> Dict[str, Any]:
        """
        세션 계속 실행

        Args:
            session_id: 세션 ID
            user_response: 사용자 응답

        Returns:
            업데이트된 세션 정보
        """
        # 기존 상태 확인
        existing_state = self.executor.get_state(session_id)
        if existing_state is None:
            return {"error": "Session not found", "session_id": session_id}

        # 워크플로우 실행
        state = self.executor.execute(session_id, user_response)

        # 결과 반환
        result = {
            "session_id": session_id,
            "questions": state.questions,
            "is_complete": state.is_complete,
            "judge_feedback": state.judge_feedback,
            "iteration_count": state.iteration_count,
            "final_srs": state.final_srs,
        }

        return result
