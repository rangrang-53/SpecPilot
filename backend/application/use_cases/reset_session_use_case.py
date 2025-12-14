"""Reset Session Use Case"""
from typing import Dict, Any
from backend.infrastructure.graph.executor import DummyExecutor


class ResetSessionUseCase:
    """
    세션 리셋 Use Case

    기존 세션을 삭제하고 초기화합니다.
    """

    def __init__(self):
        """Use Case 초기화"""
        self.executor = DummyExecutor()

    def execute(self, session_id: str) -> Dict[str, Any]:
        """
        세션 리셋 실행

        Args:
            session_id: 세션 ID

        Returns:
            리셋 결과
        """
        # 세션 삭제
        deleted = self.executor.repository.delete(session_id)

        if deleted:
            return {
                "message": "Session reset successfully",
                "session_id": session_id,
            }
        else:
            return {
                "error": "Session not found",
                "session_id": session_id,
            }
