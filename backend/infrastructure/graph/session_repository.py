"""Dummy Session Repository - 더미 구현"""
from typing import Dict, Optional, List
from backend.domain.models.state import RequirementState


class DummySessionRepository:
    """
    세션 저장소 더미 구현 (In-Memory)

    실제 구현에서는 Redis, PostgreSQL 등을 사용할 수 있습니다.
    """

    def __init__(self):
        """Repository 초기화"""
        self._storage: Dict[str, RequirementState] = {}

    def save(self, session_id: str, state: RequirementState) -> bool:
        """
        세션 상태 저장

        Args:
            session_id: 세션 ID
            state: 요구사항 상태

        Returns:
            저장 성공 여부
        """
        try:
            self._storage[session_id] = state
            return True
        except Exception:
            return False

    def load(self, session_id: str) -> Optional[RequirementState]:
        """
        세션 상태 로드

        Args:
            session_id: 세션 ID

        Returns:
            요구사항 상태 또는 None
        """
        return self._storage.get(session_id)

    def delete(self, session_id: str) -> bool:
        """
        세션 삭제

        Args:
            session_id: 세션 ID

        Returns:
            삭제 성공 여부
        """
        if session_id in self._storage:
            del self._storage[session_id]
            return True
        return False

    def list_sessions(self) -> List[str]:
        """
        모든 세션 ID 목록 조회

        Returns:
            세션 ID 리스트
        """
        return list(self._storage.keys())
