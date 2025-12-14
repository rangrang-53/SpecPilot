"""Writer Agent - 더미 구현"""
import json
from backend.domain.models.state import RequirementState
from backend.domain.models.srs import (
    SRSDocument,
    FunctionalRequirement,
    TechStackRecommendation,
    GherkinScenario,
)


def writer_agent(state: RequirementState) -> RequirementState:
    """
    최종 SRS 문서를 생성하는 에이전트 (더미)

    Args:
        state: 현재 요구사항 상태

    Returns:
        업데이트된 요구사항 상태
    """
    # 더미 SRS 문서 생성
    dummy_srs = SRSDocument(
        project_name=state.collected_info.get("project_name", "더미 프로젝트"),
        overview="AI 기반 자동 생성된 프로젝트 개요입니다.",
        functional_requirements=[
            FunctionalRequirement(
                id="FR-001",
                title="사용자 인증",
                description="사용자가 이메일과 비밀번호로 로그인할 수 있다",
                priority="High",
                tech_suggestions=["JWT", "OAuth2.0"]
            ),
            FunctionalRequirement(
                id="FR-002",
                title="데이터 관리",
                description="사용자가 데이터를 생성, 조회, 수정, 삭제할 수 있다",
                priority="High",
                tech_suggestions=["REST API", "PostgreSQL"]
            ),
        ],
        non_functional_requirements=[
            "응답 시간: 평균 1초 이내",
            "동시 접속자: 최대 10,000명 지원",
            "가용성: 99.9% uptime"
        ],
        tech_stack=[
            TechStackRecommendation(
                category="Backend",
                technologies=["FastAPI", "PostgreSQL", "Redis"],
                rationale="빠른 개발과 확장성을 위해 FastAPI를 선택했습니다."
            ),
            TechStackRecommendation(
                category="Frontend",
                technologies=["React", "Next.js", "Tailwind CSS"],
                rationale="현대적인 UI/UX와 SEO 최적화를 위해 Next.js를 사용합니다."
            ),
            TechStackRecommendation(
                category="DevOps",
                technologies=["Docker", "Kubernetes", "AWS ECS"],
                rationale="컨테이너 기반 배포와 자동 스케일링을 지원합니다."
            ),
        ],
        test_scenarios=[
            GherkinScenario(
                feature="사용자 인증",
                scenario="정상 로그인",
                given="사용자가 로그인 페이지에 있다",
                when="올바른 이메일과 비밀번호를 입력한다",
                then="메인 페이지로 이동한다"
            ),
            GherkinScenario(
                feature="데이터 관리",
                scenario="데이터 생성",
                given="사용자가 로그인되어 있다",
                when="새로운 데이터를 입력하고 저장 버튼을 클릭한다",
                then="데이터가 성공적으로 저장되고 목록에 표시된다"
            ),
        ],
        assumptions=[
            "AWS 클라우드 인프라를 사용합니다",
            "개발 기간은 3개월로 가정합니다",
            "초기 사용자는 1,000명 이하로 예상됩니다"
        ]
    )

    # JSON으로 변환하여 저장
    state.final_srs = dummy_srs.model_dump_json(indent=2)

    return state
