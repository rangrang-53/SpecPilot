"""Get SRS Use Case"""
from typing import Dict, Any, Optional
from backend.infrastructure.graph.executor import DummyExecutor


class GetSRSUseCase:
    """
    SRS 문서 조회 Use Case

    세션의 최종 SRS 문서를 조회합니다.
    """

    def __init__(self):
        """Use Case 초기화"""
        self.executor = DummyExecutor()

    def execute(self, session_id: str, format: str = "json") -> Dict[str, Any]:
        """
        SRS 조회 실행

        Args:
            session_id: 세션 ID
            format: 문서 형식 (json 또는 markdown)

        Returns:
            SRS 문서
        """
        # 상태 조회
        state = self.executor.get_state(session_id)
        if state is None:
            return {"error": "Session not found", "session_id": session_id}

        # SRS 반환
        result = {
            "session_id": session_id,
            "final_srs": state.final_srs,
            "is_complete": state.is_complete,
        }

        return result
