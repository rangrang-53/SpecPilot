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

    def extract(self, text: str) -> Dict[str, Any]:
        """
        텍스트에서 정보 추출

        Args:
            text: 사용자 입력 텍스트

        Returns:
            추출된 정보 딕셔너리
        """
        result = {}

        for category, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text:
                    if category not in result:
                        result[category] = []
                    if keyword not in result[category]:
                        result[category].append(keyword)

        # 숫자 추출 (동시 접속자, 주문 건수 등)
        numbers = re.findall(r'\d+', text)
        if numbers and "scale" in result:
            result["scale_numbers"] = [int(n) for n in numbers]

        return result
