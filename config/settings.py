"""Application Settings"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # OpenAI 설정
    openai_api_key: str = "dummy-api-key"
    model_name: str = "gpt-4o"
    temperature: float = 0.7

    # 워크플로우 설정
    max_iterations: int = 5

    # API 설정
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Frontend 설정
    frontend_port: int = 8501
    backend_url: str = "http://localhost:8000"

    # 로깅 설정
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 전역 설정 인스턴스
settings = Settings()
