"""Dummy Gemini Client"""


class DummyGeminiClient:
    """더미 Gemini 클라이언트 (테스트용)"""

    def __init__(self):
        """초기화"""
        self.model = "gemini-3-pro"

    def generate(self, prompt: str) -> str:
        """
        더미 응답 생성

        Args:
            prompt: 입력 프롬프트

        Returns:
            더미 응답 문자열
        """
        # 더미 응답 반환
        return "This is a dummy response from Gemini client."

    def generate_structured(self, prompt: str, schema: dict) -> dict:
        """
        구조화된 더미 응답 생성

        Args:
            prompt: 입력 프롬프트
            schema: 응답 스키마

        Returns:
            더미 구조화 응답
        """
        # 더미 구조화 응답 반환
        return {
            "response": "Dummy structured response",
            "schema": schema
        }
