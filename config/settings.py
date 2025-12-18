"""Application Settings"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Google Gemini 설정
    google_api_key: str = "dummy-api-key"
    model_name: str = "gemini-1.5-pro"
    temperature: float = 0.7

    # 워크플로우 설정
    max_iterations: int = 5

    # API 설정
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Frontend 설정
    frontend_port: int = 8501
    streamlit_port: int = 8501
    backend_url: str = "http://localhost:8000"

    # Session 설정
    session_timeout: int = 3600

    # 로깅 설정
    log_level: str = "INFO"
    debug: bool = True

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # .env에 추가 필드가 있어도 무시
        protected_namespaces=()  # model_ prefix 허용
    )


# 전역 설정 인스턴스
settings = Settings()
