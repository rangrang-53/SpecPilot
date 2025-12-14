"""Dummy Checkpointer"""
from typing import Any, Optional, Dict


class DummyCheckpointer:
    """더미 체크포인터 (인메모리 저장)"""

    def __init__(self):
        """초기화"""
        self._storage: Dict[str, Any] = {}

    def save(self, session_id: str, state: Any) -> bool:
        """
        체크포인트 저장

        Args:
            session_id: 세션 ID
            state: 저장할 상태

        Returns:
            저장 성공 여부
        """
        self._storage[session_id] = state
        return True

    def load(self, session_id: str) -> Optional[Any]:
        """
        체크포인트 로드

        Args:
            session_id: 세션 ID

        Returns:
            저장된 상태 또는 None
        """
        return self._storage.get(session_id)

    def delete(self, session_id: str) -> bool:
        """
        체크포인트 삭제

        Args:
            session_id: 세션 ID

        Returns:
            삭제 성공 여부
        """
        if session_id in self._storage:
            del self._storage[session_id]
            return True
        return False

    def clear_all(self) -> None:
        """모든 체크포인트 삭제"""
        self._storage.clear()
