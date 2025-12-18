"""API Client - Direct Backend Integration for Streamlit Deployment"""
import sys
import os
from typing import Dict, Any

# 프로젝트 루트를 sys.path에 추가 (Streamlit Cloud 배포용)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.application.use_cases.start_session_use_case import StartSessionUseCase
from backend.application.use_cases.continue_session_use_case import ContinueSessionUseCase
from backend.application.use_cases.get_srs_use_case import GetSRSUseCase


class APIClient:
    """
    백엔드 직접 통합 클라이언트 (Streamlit 단일 배포용)

    HTTP API 대신 백엔드 Use Case를 직접 호출합니다.
    """

    def __init__(self):
        """API Client 초기화"""
        self.start_session_uc = StartSessionUseCase()
        self.continue_session_uc = ContinueSessionUseCase()
        self.get_srs_uc = GetSRSUseCase()

    def start_session(self, initial_input: str) -> Dict[str, Any]:
        """
        새 세션 시작

        Args:
            initial_input: 초기 사용자 입력

        Returns:
            세션 정보
        """
        return self.start_session_uc.execute(initial_input)

    def continue_session(self, session_id: str, user_response: str) -> Dict[str, Any]:
        """
        세션 계속

        Args:
            session_id: 세션 ID
            user_response: 사용자 응답

        Returns:
            업데이트된 세션 정보
        """
        return self.continue_session_uc.execute(session_id, user_response)

    def get_srs(self, session_id: str) -> Dict[str, Any]:
        """
        SRS 문서 조회

        Args:
            session_id: 세션 ID

        Returns:
            SRS 문서
        """
        return self.get_srs_uc.execute(session_id)

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """
        세션 상태 조회

        Args:
            session_id: 세션 ID

        Returns:
            세션 상태
        """
        result = self.get_srs_uc.execute(session_id)
        return {
            "is_complete": result.get("is_complete", False),
            "session_id": session_id
        }

    def reset_session(self, session_id: str) -> Dict[str, Any]:
        """
        세션 리셋

        Args:
            session_id: 세션 ID

        Returns:
            리셋 결과
        """
        # 세션 리셋은 새 세션을 시작하는 것으로 대체
        return {"message": "Session reset - please start a new session"}
