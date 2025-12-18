"""Application Settings"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os

# Streamlit Secrets 지원
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Google Gemini 설정
    google_api_key: str = "dummy-api-key"
    model_name: str = "gemini-2.0-flash-exp"
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
def get_settings() -> Settings:
    """설정 인스턴스 가져오기 (Streamlit Secrets 우선)"""
    # Streamlit Cloud 환경이면 Secrets 사용
    if HAS_STREAMLIT and hasattr(st, 'secrets'):
        try:
            return Settings(
                google_api_key=st.secrets.get("GOOGLE_API_KEY", "dummy-api-key"),
                model_name=st.secrets.get("MODEL_NAME", "gemini-2.0-flash-exp"),
                temperature=float(st.secrets.get("TEMPERATURE", 0.7)),
                max_iterations=int(st.secrets.get("MAX_ITERATIONS", 5)),
            )
        except Exception:
            pass

    # 로컬 환경이면 .env 사용
    return Settings()


settings = get_settings()
