"""API Client for Backend Communication"""
import requests
from typing import Dict, Any


class APIClient:
    """
    Backend API와 통신하는 클라이언트

    Note: 실제 환경에서는 환경 변수에서 URL을 가져와야 함
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        API Client 초기화

        Args:
            base_url: Backend API 기본 URL
        """
        self.base_url = base_url

    def start_session(self, initial_input: str) -> Dict[str, Any]:
        """
        새 세션 시작

        Args:
            initial_input: 초기 사용자 입력

        Returns:
            세션 정보
        """
        response = requests.post(
            f"{self.base_url}/api/session/start",
            json={"initial_input": initial_input}
        )
        response.raise_for_status()
        return response.json()

    def continue_session(self, session_id: str, user_response: str) -> Dict[str, Any]:
        """
        세션 계속

        Args:
            session_id: 세션 ID
            user_response: 사용자 응답

        Returns:
            업데이트된 세션 정보
        """
        response = requests.post(
            f"{self.base_url}/api/session/continue",
            json={"session_id": session_id, "user_response": user_response}
        )
        response.raise_for_status()
        return response.json()

    def get_srs(self, session_id: str) -> Dict[str, Any]:
        """
        SRS 문서 조회

        Args:
            session_id: 세션 ID

        Returns:
            SRS 문서
        """
        response = requests.get(f"{self.base_url}/api/srs/{session_id}")
        response.raise_for_status()
        return response.json()

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """
        세션 상태 조회

        Args:
            session_id: 세션 ID

        Returns:
            세션 상태
        """
        response = requests.get(f"{self.base_url}/api/session/{session_id}/status")
        response.raise_for_status()
        return response.json()

    def reset_session(self, session_id: str) -> Dict[str, Any]:
        """
        세션 리셋

        Args:
            session_id: 세션 ID

        Returns:
            리셋 결과
        """
        response = requests.post(f"{self.base_url}/api/session/{session_id}/reset")
        response.raise_for_status()
        return response.json()
