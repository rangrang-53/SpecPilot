"""Writer Agent - 더미 구현"""
import json
from typing import List
from backend.domain.models.state import RequirementState
from backend.domain.models.srs import (
    SRSDocument,
    FunctionalRequirement,
    TechStackRecommendation,
    GherkinScenario,
)


def _generate_tech_stack(
    user_input: str,
    collected_info: dict,
    scale: str,
    deployment: str,
    payment: str
) -> List[TechStackRecommendation]:
    """
    프로젝트 규모와 요구사항에 따라 동적으로 기술 스택을 생성

    Args:
        user_input: 사용자 초기 입력
        collected_info: 수집된 정보
        scale: 규모 정보
        deployment: 배포 환경
        payment: 결제 정보

    Returns:
        기술 스택 추천 리스트
    """
    tech_stack = []

    # 입력 텍스트 분석 (소문자 변환)
    input_lower = user_input.lower()
    scale_lower = scale.lower()

    # 1. Backend 기술 스택 결정
    backend_tech = []
    backend_rationale = ""

    # 규모 및 복잡도에 따른 백엔드 선택
    is_large_scale = any(keyword in scale_lower for keyword in ["대규모", "많은", "수천", "수만", "트래픽"])
    is_ecommerce = any(keyword in input_lower for keyword in ["쇼핑", "이커머스", "커머스", "결제", "주문"])
    is_realtime = any(keyword in input_lower for keyword in ["실시간", "채팅", "알림", "스트리밍"])

    if is_large_scale or is_ecommerce:
        # 대규모 또는 복잡한 시스템
        backend_tech = ["Spring Boot", "Microservices", "PostgreSQL", "Redis", "Kafka"]
        backend_rationale = "대규모 트래픽과 복잡한 비즈니스 로직을 처리하기 위해 Spring Boot 기반의 MSA 아키텍처를 채택했습니다. PostgreSQL로 안정적인 데이터 저장, Redis로 캐싱 및 세션 관리, Kafka로 비동기 메시지 처리를 구현합니다."
    elif is_realtime:
        # 실시간 처리 필요
        backend_tech = ["Node.js", "Socket.io", "MongoDB", "Redis"]
        backend_rationale = "실시간 양방향 통신을 위해 Node.js와 Socket.io를 사용합니다. MongoDB로 유연한 데이터 구조 관리, Redis로 실시간 데이터 캐싱을 지원합니다."
    else:
        # 소규모/중규모 프로젝트
        backend_tech = ["FastAPI", "PostgreSQL", "SQLAlchemy"]
        backend_rationale = "빠른 개발과 높은 성능을 위해 FastAPI를 선택했습니다. PostgreSQL로 안정적인 관계형 데이터 관리를 수행합니다."

    tech_stack.append(TechStackRecommendation(
        category="Backend",
        technologies=backend_tech,
        rationale=backend_rationale
    ))

    # 2. Frontend 기술 스택 결정
    frontend_tech = []
    frontend_rationale = ""

    is_mobile = any(keyword in input_lower for keyword in ["모바일", "앱", "ios", "android"])
    is_seo_important = any(keyword in input_lower for keyword in ["검색", "seo", "마케팅", "블로그", "커머스"])
    is_admin = any(keyword in input_lower for keyword in ["관리자", "어드민", "대시보드", "백오피스"])

    if is_mobile:
        # 모바일 앱
        frontend_tech = ["React Native", "Expo", "TypeScript"]
        frontend_rationale = "iOS와 Android를 동시에 지원하기 위해 React Native를 사용합니다. TypeScript로 타입 안정성을 확보합니다."
    elif is_seo_important:
        # SEO 중요
        frontend_tech = ["Next.js", "React", "TypeScript", "Tailwind CSS"]
        frontend_rationale = "SEO 최적화와 서버 사이드 렌더링(SSR)을 위해 Next.js를 채택했습니다. Tailwind CSS로 빠른 UI 개발을 지원합니다."
    elif is_admin:
        # 관리자 페이지
        frontend_tech = ["React", "TypeScript", "Ant Design", "React Query"]
        frontend_rationale = "복잡한 데이터 관리를 위해 React와 Ant Design UI 라이브러리를 사용합니다. React Query로 서버 상태 관리를 효율화합니다."
    else:
        # 기본 웹 앱
        frontend_tech = ["React", "TypeScript", "Vite", "Tailwind CSS"]
        frontend_rationale = "현대적인 UI 개발을 위해 React와 TypeScript를 사용합니다. Vite로 빠른 개발 환경을 구성하고 Tailwind CSS로 일관된 디자인을 제공합니다."

    tech_stack.append(TechStackRecommendation(
        category="Frontend",
        technologies=frontend_tech,
        rationale=frontend_rationale
    ))

    # 3. Database 추가 (필요시)
    if is_large_scale or is_ecommerce:
        tech_stack.append(TechStackRecommendation(
            category="Database",
            technologies=["PostgreSQL", "Redis", "S3"],
            rationale="PostgreSQL로 트랜잭션 데이터 관리, Redis로 세션/캐시 관리, S3로 정적 파일 및 미디어 저장소를 구축합니다."
        ))

    # 4. DevOps 기술 스택 결정
    devops_tech = []
    devops_rationale = ""

    deployment_lower = deployment.lower()

    if is_large_scale:
        # 대규모: Kubernetes 기반
        cloud = "AWS" if "aws" in deployment_lower else "GCP" if "gcp" in deployment_lower else "Azure" if "azure" in deployment_lower else "AWS"
        devops_tech = ["Docker", "Kubernetes", f"{cloud} EKS", "GitHub Actions", "Terraform"]
        devops_rationale = f"{cloud} EKS에서 Kubernetes 기반 오케스트레이션을 통해 자동 스케일링과 무중단 배포를 구현합니다. Terraform으로 인프라를 코드화(IaC)합니다."
    elif "aws" in deployment_lower:
        # AWS 중소규모
        devops_tech = ["Docker", "AWS ECS", "AWS RDS", "GitHub Actions"]
        devops_rationale = "AWS ECS를 통한 컨테이너 기반 배포로 확장성을 확보하고, RDS로 관리형 데이터베이스를 사용합니다."
    elif "gcp" in deployment_lower:
        # GCP
        devops_tech = ["Docker", "Google Cloud Run", "Cloud SQL", "Cloud Build"]
        devops_rationale = "Google Cloud Run으로 서버리스 컨테이너 배포를 수행하고, Cloud SQL로 관리형 DB를 사용합니다."
    elif "heroku" in deployment_lower or "소규모" in scale_lower:
        # 소규모
        devops_tech = ["Docker", "Heroku", "PostgreSQL"]
        devops_rationale = "빠른 배포와 간편한 관리를 위해 Heroku PaaS를 사용합니다."
    else:
        # 기본
        devops_tech = ["Docker", "Docker Compose", deployment if deployment != "지정되지 않음" else "AWS EC2"]
        devops_rationale = f"Docker 컨테이너화를 통해 일관된 환경을 보장하고, {deployment if deployment != '지정되지 않음' else 'AWS EC2'}에 배포합니다."

    tech_stack.append(TechStackRecommendation(
        category="DevOps",
        technologies=devops_tech,
        rationale=devops_rationale
    ))

    # 5. 추가 인프라 (조건부)
    if is_realtime:
        tech_stack.append(TechStackRecommendation(
            category="Real-time Infrastructure",
            technologies=["Redis Pub/Sub", "Socket.io", "WebSocket"],
            rationale="실시간 메시징과 알림을 위해 Redis Pub/Sub와 WebSocket 프로토콜을 사용합니다."
        ))

    if payment != "지정되지 않음" and any(keyword in payment.lower() for keyword in ["pg", "결제", "카드", "간편결제"]):
        tech_stack.append(TechStackRecommendation(
            category="Payment",
            technologies=["PG 연동 API", "토스페이먼츠", "카카오페이"],
            rationale=f"{payment} 결제 수단 지원을 위해 검증된 PG사 API를 연동합니다. PCI-DSS 보안 기준을 준수합니다."
        ))

    return tech_stack


def _generate_test_scenarios(
    user_input: str,
    collected_info: dict,
    auth_info: str,
    payment_info: str
) -> List[GherkinScenario]:
    """
    프로젝트 특성에 맞는 테스트 시나리오를 동적으로 생성

    Args:
        user_input: 사용자 초기 입력
        collected_info: 수집된 정보
        auth_info: 인증 정보
        payment_info: 결제 정보

    Returns:
        Gherkin 테스트 시나리오 리스트
    """
    scenarios = []
    input_lower = user_input.lower()

    # 프로젝트 유형 분석
    is_ecommerce = any(keyword in input_lower for keyword in ["쇼핑", "이커머스", "커머스", "주문", "장바구니"])
    is_social = any(keyword in input_lower for keyword in ["소셜", "sns", "커뮤니티", "게시글", "댓글", "팔로우"])
    is_booking = any(keyword in input_lower for keyword in ["예약", "예매", "숙박", "호텔", "티켓"])
    is_content = any(keyword in input_lower for keyword in ["블로그", "콘텐츠", "게시판", "포스팅"])
    is_realtime = any(keyword in input_lower for keyword in ["실시간", "채팅", "알림", "메시지"])
    is_admin = any(keyword in input_lower for keyword in ["관리자", "어드민", "대시보드", "통계"])
    is_delivery = any(keyword in input_lower for keyword in ["배달", "배송", "딜리버리", "음식"])

    # 1. 사용자 인증 시나리오 (거의 모든 프로젝트)
    if auth_info and auth_info != "지정되지 않음":
        scenarios.append(GherkinScenario(
            feature="사용자 인증",
            scenario="정상 로그인",
            given="사용자가 로그인 페이지에 접속한다",
            when=f"유효한 {auth_info} 인증 정보로 로그인을 시도한다",
            then="메인 페이지로 리다이렉트되고 세션이 생성된다"
        ))

        scenarios.append(GherkinScenario(
            feature="사용자 인증",
            scenario="로그아웃",
            given="사용자가 로그인된 상태이다",
            when="로그아웃 버튼을 클릭한다",
            then="세션이 종료되고 로그인 페이지로 이동한다"
        ))

    # 2. 이커머스 시나리오
    if is_ecommerce:
        scenarios.extend([
            GherkinScenario(
                feature="상품 검색",
                scenario="키워드로 상품 검색",
                given="사용자가 메인 페이지에 있다",
                when="검색창에 상품명을 입력하고 검색 버튼을 클릭한다",
                then="검색 결과 페이지에 관련 상품 목록이 표시된다"
            ),
            GherkinScenario(
                feature="장바구니 관리",
                scenario="장바구니에 상품 추가",
                given="사용자가 상품 상세 페이지에 있다",
                when="'장바구니 담기' 버튼을 클릭한다",
                then="상품이 장바구니에 추가되고 확인 메시지가 표시된다"
            ),
        ])

        if payment_info and payment_info != "지정되지 않음":
            scenarios.append(GherkinScenario(
                feature="결제 처리",
                scenario="상품 결제",
                given="사용자가 장바구니에 상품을 담고 결제 페이지에 있다",
                when=f"{payment_info} 결제 정보를 입력하고 결제 버튼을 클릭한다",
                then="결제가 승인되고 주문 확인 페이지로 이동한다"
            ))

    # 3. 소셜/커뮤니티 시나리오
    if is_social:
        scenarios.extend([
            GherkinScenario(
                feature="게시글 작성",
                scenario="새 게시글 작성",
                given="사용자가 로그인된 상태에서 게시판에 있다",
                when="'글쓰기' 버튼을 클릭하고 내용을 작성한 후 저장한다",
                then="새 게시글이 생성되고 게시글 목록 상단에 표시된다"
            ),
            GherkinScenario(
                feature="댓글 작성",
                scenario="게시글에 댓글 달기",
                given="사용자가 게시글 상세 페이지에 있다",
                when="댓글 입력창에 내용을 작성하고 등록 버튼을 클릭한다",
                then="댓글이 게시글 하단에 즉시 표시된다"
            ),
            GherkinScenario(
                feature="팔로우",
                scenario="다른 사용자 팔로우",
                given="사용자가 다른 사용자의 프로필 페이지에 있다",
                when="'팔로우' 버튼을 클릭한다",
                then="팔로우 관계가 생성되고 버튼이 '팔로잉'으로 변경된다"
            ),
        ])

    # 4. 예약 시스템 시나리오
    if is_booking:
        scenarios.extend([
            GherkinScenario(
                feature="예약 검색",
                scenario="날짜별 예약 가능 여부 조회",
                given="사용자가 예약 페이지에 있다",
                when="원하는 날짜와 시간을 선택한다",
                then="해당 시간대의 예약 가능 여부가 표시된다"
            ),
            GherkinScenario(
                feature="예약 생성",
                scenario="새 예약 등록",
                given="사용자가 예약 가능한 시간대를 선택했다",
                when="필요한 정보를 입력하고 예약 버튼을 클릭한다",
                then="예약이 확정되고 확인 이메일이 발송된다"
            ),
            GherkinScenario(
                feature="예약 취소",
                scenario="기존 예약 취소",
                given="사용자가 예약 내역 페이지에서 예약을 선택했다",
                when="'예약 취소' 버튼을 클릭하고 확인한다",
                then="예약이 취소되고 해당 시간대가 다시 예약 가능 상태가 된다"
            ),
        ])

    # 5. 실시간 채팅/메시징 시나리오
    if is_realtime:
        scenarios.extend([
            GherkinScenario(
                feature="실시간 채팅",
                scenario="메시지 전송",
                given="사용자가 채팅방에 입장해 있다",
                when="메시지를 입력하고 전송 버튼을 클릭한다",
                then="메시지가 즉시 채팅방의 모든 참여자에게 표시된다"
            ),
            GherkinScenario(
                feature="알림",
                scenario="실시간 알림 수신",
                given="사용자가 앱에 로그인되어 있다",
                when="다른 사용자가 해당 사용자에게 메시지를 보낸다",
                then="실시간 푸시 알림이 표시된다"
            ),
        ])

    # 6. 배달 서비스 시나리오
    if is_delivery:
        scenarios.extend([
            GherkinScenario(
                feature="음식 주문",
                scenario="메뉴 선택 및 주문",
                given="사용자가 음식점 메뉴 페이지에 있다",
                when="원하는 메뉴를 선택하고 주문하기 버튼을 클릭한다",
                then="주문이 접수되고 예상 배달 시간이 표시된다"
            ),
            GherkinScenario(
                feature="배달 추적",
                scenario="실시간 배달 위치 확인",
                given="사용자가 주문을 완료했다",
                when="주문 상세 페이지에서 배달 추적을 조회한다",
                then="배달원의 현재 위치와 예상 도착 시간이 지도에 표시된다"
            ),
        ])

    # 7. 관리자 기능 시나리오
    if is_admin:
        scenarios.extend([
            GherkinScenario(
                feature="대시보드 조회",
                scenario="주요 지표 확인",
                given="관리자가 대시보드에 로그인했다",
                when="메인 대시보드 페이지에 접속한다",
                then="일일 사용자 수, 매출, 전환율 등 주요 지표가 차트로 표시된다"
            ),
            GherkinScenario(
                feature="사용자 관리",
                scenario="사용자 계정 정지",
                given="관리자가 사용자 관리 페이지에 있다",
                when="특정 사용자를 선택하고 '계정 정지' 버튼을 클릭한다",
                then="해당 사용자의 계정이 정지되고 로그인이 불가능해진다"
            ),
        ])

    # 8. 콘텐츠 관리 시나리오
    if is_content:
        scenarios.extend([
            GherkinScenario(
                feature="글 작성",
                scenario="마크다운 에디터로 글 작성",
                given="사용자가 글쓰기 페이지에 있다",
                when="마크다운 문법으로 내용을 작성하고 발행 버튼을 클릭한다",
                then="글이 발행되고 미리보기 형식으로 렌더링된다"
            ),
            GherkinScenario(
                feature="이미지 업로드",
                scenario="본문에 이미지 삽입",
                given="사용자가 글을 작성 중이다",
                when="이미지 파일을 드래그 앤 드롭한다",
                then="이미지가 업로드되고 본문에 삽입된다"
            ),
        ])

    # 기본 시나리오가 없으면 범용 시나리오 추가
    if not scenarios:
        scenarios.extend([
            GherkinScenario(
                feature="데이터 조회",
                scenario="목록 조회",
                given="사용자가 메인 페이지에 접속했다",
                when="목록 조회 버튼을 클릭한다",
                then="전체 데이터 목록이 표시된다"
            ),
            GherkinScenario(
                feature="데이터 생성",
                scenario="새 항목 생성",
                given="사용자가 생성 페이지에 있다",
                when="필요한 정보를 입력하고 저장 버튼을 클릭한다",
                then="새 항목이 생성되고 목록에 추가된다"
            ),
            GherkinScenario(
                feature="데이터 수정",
                scenario="기존 항목 수정",
                given="사용자가 상세 페이지에서 항목을 선택했다",
                when="내용을 수정하고 업데이트 버튼을 클릭한다",
                then="변경사항이 저장되고 수정된 내용이 표시된다"
            ),
        ])

    return scenarios


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

    # 동적 기술 스택 생성 - 프로젝트 규모와 요구사항에 따라 결정
    tech_stack_list = _generate_tech_stack(
        state.user_input,
        state.collected_info,
        scale_info,
        deployment_info,
        payment_info
    )

    # 동적 테스트 시나리오 생성 - 프로젝트 특성에 맞춰 생성
    test_scenarios_list = _generate_test_scenarios(
        state.user_input,
        state.collected_info,
        auth_info,
        payment_info
    )

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
        test_scenarios=test_scenarios_list,
        assumptions=assumptions_list
    )

    # JSON으로 변환하여 저장
    state.final_srs = dummy_srs.model_dump_json(indent=2)

    return state
