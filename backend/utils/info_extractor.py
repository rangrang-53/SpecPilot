"""Info Extractor - 사용자 입력에서 정보 추출"""
from typing import Dict, Any
import re


class InfoExtractor:
    """
    사용자 입력 텍스트에서 구조화된 정보를 추출하는 유틸리티

    더미 구현: 간단한 키워드 매칭으로 정보 추출
    """

    def __init__(self):
        """InfoExtractor 초기화"""
        self.keywords = {
            "payment": ["결제", "카드", "가상계좌", "간편결제", "페이"],
            "authentication": ["인증", "로그인", "회원가입", "OAuth", "JWT"],
            "deployment": ["배포", "AWS", "GCP", "Azure", "클라우드", "온프레미스"],
            "scale": ["동시접속", "사용자", "트래픽", "주문", "건수"],
            "features": ["기능", "쇼핑몰", "커머스", "장바구니", "상품"],
        }

    def extract(self, text: str, existing_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        텍스트에서 정보 추출

        Args:
            text: 사용자 입력 텍스트
            existing_info: 기존에 수집된 정보 (중복 방지용)

        Returns:
            추출된 정보 딕셔너리
        """
        if existing_info is None:
            existing_info = {}

        result = {}

        # 각 카테고리별로 키워드 매칭
        for category, keywords in self.keywords.items():
            # 이미 수집된 정보는 건너뛰기
            if category in existing_info:
                continue

            for keyword in keywords:
                if keyword in text:
                    # 첫 번째 매칭된 키워드만 저장 (문자열로)
                    result[category] = text.strip()
                    break

        return result
