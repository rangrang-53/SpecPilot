"""Info Extractor - 사용자 입력에서 정보 추출"""
from typing import Dict, Any
import re


class InfoExtractor:
    """
    사용자 입력 텍스트에서 구조화된 정보를 추출하는 유틸리티

    스마트 추출: 전체 문장이 아닌 핵심 정보만 추출
    """

    def __init__(self):
        """InfoExtractor 초기화"""
        # 각 카테고리별 추출 패턴
        self.patterns = {
            "payment": {
                "keywords": ["KG", "이니시스", "토스", "나이스", "페이팔", "페이코", "카카오페이", "네이버페이"],
                "extractor": self._extract_payment
            },
            "authentication": {
                "keywords": ["OAuth", "JWT", "소셜로그인", "카카오", "네이버", "구글"],
                "extractor": self._extract_authentication
            },
            "deployment": {
                "keywords": ["AWS", "GCP", "Azure", "클라우드", "온프레미스", "도커", "쿠버네티스"],
                "extractor": self._extract_deployment
            },
            "scale": {
                "keywords": ["명", "만", "동시접속", "사용자", "트래픽"],
                "extractor": self._extract_scale
            },
            "project_type": {
                "keywords": ["쇼핑몰", "이커머스", "인트라넷", "사내", "그룹웨어", "SNS", "커뮤니티", "배달", "예약"],
                "extractor": self._extract_project_type
            }
        }

    def _extract_payment(self, text: str) -> str:
        """결제 수단 추출"""
        text_lower = text.lower()
        pg_map = {
            "kg": "KG 이니시스",
            "이니시스": "KG 이니시스",
            "토스": "토스페이먼츠",
            "나이스": "나이스페이먼츠",
            "페이팔": "PayPal",
            "페이코": "PAYCO",
            "카카오페이": "카카오페이",
            "네이버페이": "네이버페이"
        }
        for keyword, pg_name in pg_map.items():
            if keyword in text_lower:
                return pg_name
        return None

    def _extract_authentication(self, text: str) -> str:
        """인증 방식 추출"""
        text_lower = text.lower()
        if "oauth" in text_lower:
            return "OAuth 2.0"
        if "jwt" in text_lower:
            return "JWT 토큰 인증"
        if "소셜로그인" in text_lower or "소셜" in text_lower:
            socials = []
            if "카카오" in text_lower:
                socials.append("카카오")
            if "네이버" in text_lower:
                socials.append("네이버")
            if "구글" in text_lower:
                socials.append("구글")
            if socials:
                return f"{'/'.join(socials)} 소셜 로그인"
            return "소셜 로그인"
        return None

    def _extract_deployment(self, text: str) -> str:
        """배포 환경 추출"""
        text_upper = text.upper()
        if "AWS" in text_upper:
            return "AWS"
        if "GCP" in text_upper:
            return "GCP"
        if "AZURE" in text_upper:
            return "Azure"
        if "클라우드" in text:
            return "클라우드"
        if "온프레미스" in text:
            return "온프레미스"
        if "도커" in text or "DOCKER" in text_upper:
            return "Docker"
        if "쿠버네티스" in text or "KUBERNETES" in text_upper or "K8S" in text_upper:
            return "Kubernetes"
        return None

    def _extract_scale(self, text: str) -> str:
        """규모 정보 추출 (숫자 + 단위)"""
        # 패턴: "월 1만 명", "동시접속 500명", "일 10만 건" 등
        patterns = [
            r'(\d+(?:,\d+)?)\s*만\s*명',  # "1만 명"
            r'(\d+(?:,\d+)?)\s*천\s*명',  # "5천 명"
            r'(\d+(?:,\d+)?)\s*명',       # "500명"
            r'동시접속\s*(\d+(?:,\d+)?)', # "동시접속 500"
            r'월\s*(\d+(?:,\d+)?)\s*만',  # "월 1만"
            r'일\s*(\d+(?:,\d+)?)\s*만',  # "일 10만"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                number = match.group(1)
                # 컨텍스트 추출 (숫자 주변 5단어)
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end].strip()

                # "월 1만 명" 형태로 정리
                if "만" in context:
                    return f"{number}만 명"
                elif "천" in context:
                    return f"{number}천 명"
                else:
                    return f"{number}명"

        return None

    def _extract_project_type(self, text: str) -> str:
        """프로젝트 타입 추출"""
        text_lower = text.lower()
        type_map = {
            "쇼핑몰": "이커머스",
            "이커머스": "이커머스",
            "커머스": "이커머스",
            "인트라넷": "사내 인트라넷",
            "사내": "사내 인트라넷",
            "그룹웨어": "사내 인트라넷",
            "sns": "소셜 네트워크",
            "커뮤니티": "커뮤니티",
            "배달": "배달 서비스",
            "예약": "예약 시스템",
            "블로그": "블로그/콘텐츠"
        }
        for keyword, ptype in type_map.items():
            if keyword in text_lower:
                return ptype
        return None

    def extract(self, text: str, existing_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        텍스트에서 정보 추출

        Args:
            text: 사용자 입력 텍스트
            existing_info: 기존에 수집된 정보 (중복 방지용)

        Returns:
            추출된 정보 딕셔너리 (핵심 정보만 포함)
        """
        # text가 None이거나 빈 문자열이면 빈 딕셔너리 반환
        if not text:
            return {}

        if existing_info is None:
            existing_info = {}

        result = {}

        # 각 카테고리별로 스마트 추출
        for category, config in self.patterns.items():
            # 이미 수집된 정보는 건너뛰기
            if category in existing_info:
                continue

            # 키워드가 포함되어 있는지 확인
            keywords = config["keywords"]
            text_lower = text.lower()
            has_keyword = any(keyword.lower() in text_lower for keyword in keywords)

            if has_keyword:
                # 카테고리별 추출 함수 실행
                extractor = config["extractor"]
                extracted_value = extractor(text)

                if extracted_value:
                    result[category] = extracted_value

        return result
