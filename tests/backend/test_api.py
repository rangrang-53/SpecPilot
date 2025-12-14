"""API Test Suite"""
import pytest
from fastapi.testclient import TestClient
from backend.presentation.main import app

client = TestClient(app)


class TestSessionAPI:
    """Session API 테스트"""

    def test_start_session(self):
        """세션 시작 API 테스트"""
        response = client.post(
            "/api/session/start",
            json={"initial_input": "쇼핑몰을 만들고 싶습니다"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "questions" in data
        assert isinstance(data["questions"], list)

    def test_continue_session(self):
        """세션 계속 API 테스트"""
        # 먼저 세션 생성
        start_response = client.post(
            "/api/session/start",
            json={"initial_input": "온라인 쇼핑몰"}
        )
        session_id = start_response.json()["session_id"]

        # 세션 계속
        continue_response = client.post(
            "/api/session/continue",
            json={
                "session_id": session_id,
                "user_response": "카드 결제 지원"
            }
        )

        assert continue_response.status_code == 200
        data = continue_response.json()
        assert data["session_id"] == session_id

    def test_get_session_status(self):
        """세션 상태 조회 API 테스트"""
        # 세션 생성
        start_response = client.post(
            "/api/session/start",
            json={"initial_input": "테스트 프로젝트"}
        )
        session_id = start_response.json()["session_id"]

        # 상태 조회
        status_response = client.get(f"/api/session/{session_id}/status")

        assert status_response.status_code == 200
        data = status_response.json()
        assert "session_id" in data
        assert "is_complete" in data

    def test_reset_session(self):
        """세션 리셋 API 테스트"""
        # 세션 생성
        start_response = client.post(
            "/api/session/start",
            json={"initial_input": "테스트"}
        )
        session_id = start_response.json()["session_id"]

        # 세션 리셋
        reset_response = client.post(f"/api/session/{session_id}/reset")

        assert reset_response.status_code == 200
        data = reset_response.json()
        assert "message" in data or "session_id" in data


class TestSRSAPI:
    """SRS API 테스트"""

    def test_get_srs(self):
        """SRS 조회 API 테스트"""
        # 세션 생성
        start_response = client.post(
            "/api/session/start",
            json={"initial_input": "테스트 프로젝트"}
        )
        session_id = start_response.json()["session_id"]

        # SRS 조회
        srs_response = client.get(f"/api/srs/{session_id}")

        assert srs_response.status_code == 200
        data = srs_response.json()
        assert "session_id" in data

    def test_get_collected_info(self):
        """수집된 정보 조회 API 테스트"""
        # 세션 생성
        start_response = client.post(
            "/api/session/start",
            json={"initial_input": "테스트"}
        )
        session_id = start_response.json()["session_id"]

        # 수집된 정보 조회
        info_response = client.get(f"/api/session/{session_id}/collected-info")

        assert info_response.status_code == 200
        data = info_response.json()
        assert "session_id" in data
        assert "collected_info" in data
