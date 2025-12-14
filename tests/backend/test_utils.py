"""Utils Test Suite"""
import pytest
from backend.domain.models.state import RequirementState
from backend.domain.models.srs import SRSDocument, FunctionalRequirement
from backend.utils.info_extractor import InfoExtractor
from backend.utils.srs_formatter import SRSFormatter
from backend.utils.quality_metrics import QualityMetrics


class TestInfoExtractor:
    """InfoExtractor 테스트"""

    def test_extractor_initialization(self):
        """InfoExtractor가 초기화되는지 테스트"""
        extractor = InfoExtractor()
        assert extractor is not None

    def test_extract_from_simple_text(self):
        """단순 텍스트에서 정보 추출 테스트"""
        extractor = InfoExtractor()
        text = "결제는 카드와 가상계좌를 지원하고, 하루 주문은 1000건 정도입니다"
        result = extractor.extract(text)

        assert isinstance(result, dict)
        assert len(result) > 0

    def test_extract_returns_dict(self):
        """추출 결과가 딕셔너리인지 테스트"""
        extractor = InfoExtractor()
        result = extractor.extract("테스트 입력")
        assert isinstance(result, dict)


class TestSRSFormatter:
    """SRSFormatter 테스트"""

    def test_formatter_initialization(self):
        """SRSFormatter가 초기화되는지 테스트"""
        formatter = SRSFormatter()
        assert formatter is not None

    def test_format_to_markdown(self):
        """SRS 문서를 Markdown으로 변환 테스트"""
        formatter = SRSFormatter()
        srs = SRSDocument(
            project_name="테스트 프로젝트",
            overview="프로젝트 개요",
            functional_requirements=[
                FunctionalRequirement(
                    id="FR-001",
                    title="기능1",
                    description="설명1",
                    priority="High",
                    tech_suggestions=["React"]
                )
            ],
            non_functional_requirements=["성능"],
            tech_stack=[],
            test_scenarios=[],
            assumptions=[]
        )

        markdown = formatter.to_markdown(srs)
        assert isinstance(markdown, str)
        assert len(markdown) > 0
        assert "테스트 프로젝트" in markdown
        assert "FR-001" in markdown

    def test_format_json_string_to_markdown(self):
        """JSON 문자열을 Markdown으로 변환 테스트"""
        formatter = SRSFormatter()
        json_str = '{"project_name": "테스트", "overview": "개요", "functional_requirements": [], "non_functional_requirements": [], "tech_stack": [], "test_scenarios": [], "assumptions": []}'

        markdown = formatter.json_to_markdown(json_str)
        assert isinstance(markdown, str)
        assert "테스트" in markdown


class TestQualityMetrics:
    """QualityMetrics 테스트"""

    def test_metrics_initialization(self):
        """QualityMetrics가 초기화되는지 테스트"""
        metrics = QualityMetrics()
        assert metrics is not None

    def test_calculate_completeness_score(self):
        """완전성 점수 계산 테스트"""
        metrics = QualityMetrics()
        state = RequirementState(
            user_input="테스트",
            collected_info={
                "feature": "기능",
                "tech": "기술",
                "deployment": "배포"
            }
        )

        score = metrics.calculate_completeness(state)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_empty_state_low_score(self):
        """빈 상태는 낮은 점수를 받는지 테스트"""
        metrics = QualityMetrics()
        state = RequirementState(user_input="테스트")

        score = metrics.calculate_completeness(state)
        assert score < 0.5

    def test_rich_state_high_score(self):
        """풍부한 정보는 높은 점수를 받는지 테스트"""
        metrics = QualityMetrics()
        state = RequirementState(
            user_input="테스트",
            collected_info={
                "feature": "기능",
                "payment": "결제",
                "auth": "인증",
                "deployment": "배포",
                "scale": "규모"
            }
        )

        score = metrics.calculate_completeness(state)
        assert score >= 0.5

    def test_get_missing_areas(self):
        """누락된 영역 조회 테스트"""
        metrics = QualityMetrics()
        state = RequirementState(
            user_input="테스트",
            collected_info={"feature": "기능"}
        )

        missing = metrics.get_missing_areas(state)
        assert isinstance(missing, list)
        assert len(missing) > 0
