"""Google Gemini LLM Client"""
import os
import json
import time
from typing import Optional, Dict, Any
import google.generativeai as genai
from config.settings import settings


class GeminiClient:
    """
    Google Gemini API 클라이언트

    실제 Gemini API를 사용하여 LLM 응답을 생성합니다.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Gemini 클라이언트 초기화

        Args:
            api_key: Google API 키 (None이면 환경 변수에서 가져옴)
        """
        # API 키 설정
        self.api_key = api_key or settings.google_api_key or os.getenv("GOOGLE_API_KEY")

        if not self.api_key or self.api_key == "dummy-api-key":
            raise ValueError(
                "Google API key not found. "
                "Please set GOOGLE_API_KEY in .env file or pass it to GeminiClient."
            )

        # Gemini 설정
        genai.configure(api_key=self.api_key)

        # 모델 초기화
        self.model_name = settings.model_name
        self.temperature = settings.temperature
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )

    def generate(
        self,
        prompt: str,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> str:
        """
        텍스트 응답 생성

        Args:
            prompt: 입력 프롬프트
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 간 대기 시간 (초)

        Returns:
            생성된 응답 문자열

        Raises:
            Exception: API 호출 실패 시
        """
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)

                # 응답 검증
                if not response or not response.text:
                    raise ValueError("Empty response from Gemini API")

                return response.text.strip()

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Gemini API error (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(retry_delay * (attempt + 1))  # 지수 백오프
                    continue
                else:
                    raise Exception(f"Gemini API failed after {max_retries} attempts: {e}")

    def generate_json(
        self,
        prompt: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        JSON 형식 응답 생성

        Args:
            prompt: 입력 프롬프트 (JSON 형식 요청 포함)
            max_retries: 최대 재시도 횟수

        Returns:
            파싱된 JSON 응답

        Raises:
            json.JSONDecodeError: JSON 파싱 실패 시
        """
        # JSON 형식 요청 추가
        json_prompt = f"{prompt}\n\nPlease respond with valid JSON only, no additional text."

        response_text = self.generate(json_prompt, max_retries=max_retries)

        # JSON 파싱 시도
        try:
            # 마크다운 코드 블록 제거 (```json ... ```)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            return json.loads(response_text)

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {response_text}")
            raise json.JSONDecodeError(f"Invalid JSON from Gemini: {e}", response_text, 0)

    def generate_with_context(
        self,
        system_prompt: str,
        user_message: str,
        max_retries: int = 3
    ) -> str:
        """
        시스템 프롬프트와 사용자 메시지를 결합하여 응답 생성

        Args:
            system_prompt: 시스템 역할 프롬프트
            user_message: 사용자 메시지
            max_retries: 최대 재시도 횟수

        Returns:
            생성된 응답 문자열
        """
        combined_prompt = f"{system_prompt}\n\nUser Input:\n{user_message}"
        return self.generate(combined_prompt, max_retries=max_retries)


class DummyGeminiClient:
    """
    더미 Gemini 클라이언트 (테스트 및 개발용)

    API 키 없이 개발/테스트할 수 있도록 더미 응답을 반환합니다.
    """

    def __init__(self):
        """초기화"""
        self.model_name = "gemini-3-pro-dummy"
        print("⚠️ Using DummyGeminiClient - responses will be simulated")

    def generate(self, prompt: str, **kwargs) -> str:
        """더미 응답 생성"""
        return "This is a dummy response from Gemini client."

    def generate_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """더미 JSON 응답 생성"""
        return {
            "response": "Dummy structured response",
            "note": "This is a dummy response for testing"
        }

    def generate_with_context(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        """더미 컨텍스트 응답 생성"""
        return f"Dummy response to: {user_message[:50]}..."


def get_gemini_client() -> GeminiClient:
    """
    Gemini 클라이언트 인스턴스 가져오기

    API 키가 설정되어 있으면 실제 클라이언트를,
    없으면 더미 클라이언트를 반환합니다.

    Returns:
        GeminiClient 또는 DummyGeminiClient 인스턴스
    """
    try:
        return GeminiClient()
    except ValueError as e:
        print(f"⚠️ {e}")
        print("⚠️ Falling back to DummyGeminiClient")
        return DummyGeminiClient()
