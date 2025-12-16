"""Infrastructure Layer Test Suite"""
import pytest
from backend.infrastructure.llm.gemini_client import DummyGeminiClient
from backend.infrastructure.persistence.checkpointer import DummyCheckpointer
from backend.infrastructure.persistence.state_store import DummyStateStore


class TestDummyGeminiClient:
    """더미 Gemini 클라이언트 테스트"""

    def test_client_initialization(self):
        """클라이언트 초기화 테스트"""
        client = DummyGeminiClient()
        assert client is not None

    def test_generate_response(self):
        """더미 응답 생성 테스트"""
        client = DummyGeminiClient()
        response = client.generate("test prompt")
        assert isinstance(response, str)
        assert len(response) > 0


class TestDummyCheckpointer:
    """더미 Checkpointer 테스트"""

    def test_checkpointer_initialization(self):
        """Checkpointer 초기화 테스트"""
        checkpointer = DummyCheckpointer()
        assert checkpointer is not None

    def test_save_checkpoint(self):
        """체크포인트 저장 테스트"""
        checkpointer = DummyCheckpointer()
        state = {"iteration": 1}
        result = checkpointer.save("session_1", state)
        assert result is True

    def test_load_checkpoint(self):
        """체크포인트 로드 테스트"""
        checkpointer = DummyCheckpointer()
        state = {"iteration": 1}
        checkpointer.save("session_1", state)
        loaded = checkpointer.load("session_1")
        assert loaded is not None
        assert loaded["iteration"] == 1


class TestDummyStateStore:
    """더미 State Store 테스트"""

    def test_state_store_initialization(self):
        """State Store 초기화 테스트"""
        store = DummyStateStore()
        assert store is not None

    def test_store_state(self):
        """상태 저장 테스트"""
        store = DummyStateStore()
        result = store.set("key1", "value1")
        assert result is True

    def test_retrieve_state(self):
        """상태 조회 테스트"""
        store = DummyStateStore()
        store.set("key1", "value1")
        value = store.get("key1")
        assert value == "value1"

    def test_retrieve_nonexistent_key(self):
        """존재하지 않는 키 조회 테스트"""
        store = DummyStateStore()
        value = store.get("nonexistent")
        assert value is None
