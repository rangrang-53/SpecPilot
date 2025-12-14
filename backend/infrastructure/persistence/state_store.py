"""Dummy State Store"""
from typing import Any, Optional, Dict


class DummyStateStore:
    """더미 상태 저장소 (인메모리)"""

    def __init__(self):
        """초기화"""
        self._store: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> bool:
        """
        상태 저장

        Args:
            key: 키
            value: 값

        Returns:
            저장 성공 여부
        """
        self._store[key] = value
        return True

    def get(self, key: str) -> Optional[Any]:
        """
        상태 조회

        Args:
            key: 키

        Returns:
            저장된 값 또는 None
        """
        return self._store.get(key)

    def delete(self, key: str) -> bool:
        """
        상태 삭제

        Args:
            key: 키

        Returns:
            삭제 성공 여부
        """
        if key in self._store:
            del self._store[key]
            return True
        return False

    def exists(self, key: str) -> bool:
        """
        키 존재 여부 확인

        Args:
            key: 키

        Returns:
            존재 여부
        """
        return key in self._store

    def clear(self) -> None:
        """모든 상태 삭제"""
        self._store.clear()
