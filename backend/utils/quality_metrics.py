"""Quality Metrics - 요구사항 품질 평가"""
from typing import List
from backend.domain.models.state import RequirementState


class QualityMetrics:
    """
    요구사항 완전성 및 품질을 평가하는 유틸리티

    더미 구현: collected_info 키 개수 기반 점수 계산
    """

    def __init__(self):
        """QualityMetrics 초기화"""
        self.required_areas = [
            "features",
            "payment",
            "authentication",
            "deployment",
            "scale"
        ]

    def calculate_completeness(self, state: RequirementState) -> float:
        """
        요구사항 완전성 점수 계산 (0.0 ~ 1.0)

        Args:
            state: 요구사항 상태

        Returns:
            완전성 점수 (0.0 ~ 1.0)
        """
        if not state.collected_info:
            return 0.0

        collected_count = len(state.collected_info)
        total_required = len(self.required_areas)

        # 기본 점수: 수집된 정보 개수 / 필요한 영역 개수
        score = min(collected_count / total_required, 1.0)

        return round(score, 2)

    def get_missing_areas(self, state: RequirementState) -> List[str]:
        """
        누락된 영역 목록 조회

        Args:
            state: 요구사항 상태

        Returns:
            누락된 영역 리스트
        """
        collected_keys = set(state.collected_info.keys())
        required_keys = set(self.required_areas)

        missing = list(required_keys - collected_keys)
        return missing
