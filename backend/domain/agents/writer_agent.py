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
    # collected_info에서 사용자 답변 추출
    project_name = state.collected_info.get("project_name", "프로젝트")
    payment_info = state.collected_info.get("payment", "지정되지 않음")
    scale_info = state.collected_info.get("scale", "지정되지 않음")
    auth_info = state.collected_info.get("authentication", "지정되지 않음")
    deployment_info = state.collected_info.get("deployment", "지정되지 않음")

    # 사용자 입력을 반영한 개요 생성
    overview = f"""
{state.user_input}

**수집된 요구사항:**
- 프로젝트명: {project_name}
- 결제 수단: {payment_info}
- 규모: {scale_info}
- 인증 방식: {auth_info}
- 배포 환경: {deployment_info}
    """.strip()

    # 비기능 요구사항에 사용자 답변 반영
    nfr_list = [
        "응답 시간: 평균 1초 이내",
        f"예상 규모: {scale_info}",
        "가용성: 99.9% uptime"
    ]

    # 기술 스택에 배포 환경 반영
    tech_stack_list = [
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
            technologies=["Docker", "Kubernetes", deployment_info if deployment_info != "지정되지 않음" else "클라우드"],
            rationale=f"{deployment_info} 환경에서 컨테이너 기반 배포와 자동 스케일링을 지원합니다."
        ),
    ]

    # Assumptions에 사용자 답변 반영
    assumptions_list = [
        f"{deployment_info} 클라우드 인프라를 사용합니다" if deployment_info != "지정되지 않음" else "클라우드 인프라를 사용합니다",
        "개발 기간은 3개월로 가정합니다",
        f"결제 수단: {payment_info}",
        f"인증 방식: {auth_info}"
    ]

    # SRS 문서 생성
    dummy_srs = SRSDocument(
        project_name=project_name,
        overview=overview,
        functional_requirements=[
            FunctionalRequirement(
                id="FR-001",
                title="사용자 인증",
                description=f"{auth_info} 방식으로 사용자 인증을 구현합니다.",
                priority="High",
                tech_suggestions=["JWT", "OAuth2.0"]
            ),
            FunctionalRequirement(
                id="FR-002",
                title="결제 처리",
                description=f"{payment_info} 결제 수단을 지원합니다.",
                priority="High",
                tech_suggestions=["PG 연동", "결제 게이트웨이"]
            ),
            FunctionalRequirement(
                id="FR-003",
                title="데이터 관리",
                description="사용자가 데이터를 생성, 조회, 수정, 삭제할 수 있습니다.",
                priority="Medium",
                tech_suggestions=["REST API", "PostgreSQL"]
            ),
        ],
        non_functional_requirements=nfr_list,
        tech_stack=tech_stack_list,
        test_scenarios=[
            GherkinScenario(
                feature="사용자 인증",
                scenario="정상 로그인",
                given="사용자가 로그인 페이지에 있다",
                when=f"{auth_info} 방식으로 인증을 시도한다",
                then="메인 페이지로 이동한다"
            ),
            GherkinScenario(
                feature="결제 처리",
                scenario="결제 진행",
                given="사용자가 결제 페이지에 있다",
                when=f"{payment_info} 결제를 진행한다",
                then="결제가 성공적으로 완료된다"
            ),
        ],
        assumptions=assumptions_list
    )

    # JSON으로 변환하여 저장
    state.final_srs = dummy_srs.model_dump_json(indent=2)

    return state
