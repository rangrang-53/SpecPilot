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
from backend.utils.string_utils import safe_lower


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

    # CRITICAL: 초기 요청(initial_request)도 함께 분석
    initial_request = collected_info.get("initial_request", "")
    combined_input = f"{user_input} {initial_request}"
    input_lower = safe_lower(combined_input)
    scale_lower = safe_lower(scale)

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

    deployment_lower = safe_lower(deployment)

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
        deploy_target = deployment if (deployment and deployment != "지정되지 않음") else "AWS EC2"
        devops_tech = ["Docker", "Docker Compose", deploy_target]
        devops_rationale = f"Docker 컨테이너화를 통해 일관된 환경을 보장하고, {deploy_target}에 배포합니다."

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

    if payment and payment != "지정되지 않음" and any(keyword in safe_lower(payment) for keyword in ["pg", "결제", "카드", "간편결제"]):
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

    # CRITICAL: 초기 요청(initial_request)도 함께 분석
    initial_request = collected_info.get("initial_request", "")
    combined_input = f"{user_input} {initial_request}"
    input_lower = safe_lower(combined_input)

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

    # 2. 결제 시나리오 (결제 정보가 있는 모든 프로젝트)
    if payment_info and payment_info != "지정되지 않음":
        if is_ecommerce:
            scenarios.append(GherkinScenario(
                feature="결제 처리",
                scenario="상품 결제",
                given="사용자가 장바구니에 상품을 담고 결제 페이지에 있다",
                when=f"{payment_info} 결제 정보를 입력하고 결제 버튼을 클릭한다",
                then="결제가 승인되고 주문 확인 페이지로 이동한다"
            ))
        elif is_booking:
            scenarios.append(GherkinScenario(
                feature="결제 처리",
                scenario="예약 결제",
                given="사용자가 예약 정보를 입력하고 결제 페이지에 있다",
                when=f"{payment_info} 결제 정보를 입력하고 결제 버튼을 클릭한다",
                then="결제가 승인되고 예약이 확정된다"
            ))
        else:
            scenarios.append(GherkinScenario(
                feature="결제 처리",
                scenario="일반 결제",
                given="사용자가 결제 페이지에 있다",
                when=f"{payment_info} 결제 정보를 입력하고 결제 버튼을 클릭한다",
                then="결제가 승인되고 결제 완료 페이지로 이동한다"
            ))

        # 결제 실패 시나리오도 추가
        scenarios.append(GherkinScenario(
            feature="결제 처리",
            scenario="결제 실패 처리",
            given="사용자가 결제 페이지에 있다",
            when="잔액이 부족한 카드로 결제를 시도한다",
            then="결제 실패 메시지가 표시되고 다시 시도할 수 있다"
        ))

    # 3. 이커머스 시나리오
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

    # 4. 소셜/커뮤니티 시나리오
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

    # 5. 예약 시스템 시나리오
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

    # 6. 실시간 채팅/메시징 시나리오
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

    # 7. 배달 서비스 시나리오
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

    # 8. 관리자 기능 시나리오
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

    # 9. 콘텐츠 관리 시나리오
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


def _generate_functional_requirements(
    user_input: str,
    collected_info: dict,
    auth_info: str,
    payment_info: str
) -> List[FunctionalRequirement]:
    """
    프로젝트 특성에 맞는 기능 요구사항을 동적으로 생성

    Args:
        user_input: 사용자 초기 입력
        collected_info: 수집된 정보
        auth_info: 인증 정보
        payment_info: 결제 정보

    Returns:
        기능 요구사항 리스트
    """
    requirements = []

    # CRITICAL: 초기 요청(initial_request)도 함께 분석
    initial_request = collected_info.get("initial_request", "")
    combined_input = f"{user_input} {initial_request}"
    input_lower = safe_lower(combined_input)
    fr_id = 1

    # 프로젝트 유형 분석
    is_ecommerce = any(keyword in input_lower for keyword in ["쇼핑", "이커머스", "커머스", "주문", "장바구니"])
    is_social = any(keyword in input_lower for keyword in ["소셜", "sns", "커뮤니티", "게시글", "댓글"])
    is_booking = any(keyword in input_lower for keyword in ["예약", "예매", "숙박", "호텔"])
    is_intranet = any(keyword in input_lower for keyword in ["인트라넷", "사내", "그룹웨어", "전자결재"])
    is_content = any(keyword in input_lower for keyword in ["블로그", "콘텐츠", "게시판"])
    is_realtime = any(keyword in input_lower for keyword in ["실시간", "채팅", "알림"])
    is_delivery = any(keyword in input_lower for keyword in ["배달", "배송", "음식"])

    # 1. 인증은 거의 모든 프로젝트에 필요
    if auth_info and auth_info != "지정되지 않음":
        requirements.append(FunctionalRequirement(
            id=f"FR-{fr_id:03d}",
            title="사용자 인증 및 권한 관리",
            description=f"{auth_info} 방식으로 사용자 인증을 구현하고, 역할 기반 접근 제어(RBAC)를 통해 권한을 관리합니다.",
            priority="High",
            tech_suggestions=["JWT", "OAuth2.0", "Role-Based Access Control"]
        ))
        fr_id += 1

    # 2. 인트라넷 특화 기능
    if is_intranet:
        requirements.extend([
            FunctionalRequirement(
                id=f"FR-{fr_id:03d}",
                title="조직도 및 직원 정보 관리",
                description="부서별 조직도를 표시하고, 직원 정보(연락처, 직급, 소속 부서)를 조회 및 검색할 수 있습니다.",
                priority="High",
                tech_suggestions=["Tree Structure", "Elasticsearch", "LDAP 연동"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+1:03d}",
                title="전자결재 시스템",
                description="휴가 신청, 지출 결의, 업무 보고 등의 결재 문서를 작성하고, 결재선에 따라 승인/반려를 처리합니다.",
                priority="High",
                tech_suggestions=["Workflow Engine", "PDF 생성", "전자서명"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+2:03d}",
                title="사내 게시판 및 공지사항",
                description="전사 공지, 부서별 게시판, 경조사 알림 등을 게시하고 조회할 수 있습니다.",
                priority="Medium",
                tech_suggestions=["CMS", "알림 푸시", "파일 첨부"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+3:03d}",
                title="회의실 예약 시스템",
                description="회의실 예약 현황을 확인하고, 시간대별로 회의실을 예약하거나 취소할 수 있습니다.",
                priority="Medium",
                tech_suggestions=["캘린더 UI", "실시간 예약 충돌 방지", "Outlook 연동"]
            ),
        ])
        fr_id += 4

    # 3. 이커머스 특화 기능
    elif is_ecommerce:
        requirements.extend([
            FunctionalRequirement(
                id=f"FR-{fr_id:03d}",
                title="상품 관리",
                description="상품 등록, 수정, 삭제, 재고 관리 및 카테고리 분류를 수행합니다.",
                priority="High",
                tech_suggestions=["Product Catalog API", "이미지 최적화", "재고 알림"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+1:03d}",
                title="장바구니 및 주문 처리",
                description="사용자가 상품을 장바구니에 담고, 주문 및 결제를 진행할 수 있습니다.",
                priority="High",
                tech_suggestions=["세션 관리", "주문 상태 관리", "재고 차감 로직"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+2:03d}",
                title="결제 시스템",
                description=f"{payment_info} 결제 수단을 지원하고, 결제 내역을 기록합니다.",
                priority="High",
                tech_suggestions=["PG 연동", "결제 취소/환불", "영수증 발행"]
            ),
        ])
        fr_id += 3

    # 4. 소셜/커뮤니티 특화 기능
    elif is_social:
        requirements.extend([
            FunctionalRequirement(
                id=f"FR-{fr_id:03d}",
                title="게시글 작성 및 관리",
                description="사용자가 텍스트, 이미지, 동영상을 포함한 게시글을 작성하고 수정/삭제할 수 있습니다.",
                priority="High",
                tech_suggestions=["Rich Text Editor", "이미지/동영상 업로드", "해시태그"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+1:03d}",
                title="댓글 및 좋아요",
                description="게시글에 댓글을 달고, 좋아요/공유 기능을 제공합니다.",
                priority="Medium",
                tech_suggestions=["실시간 업데이트", "알림 시스템", "카운터 최적화"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+2:03d}",
                title="팔로우 및 피드",
                description="다른 사용자를 팔로우하고, 팔로우한 사용자의 게시글을 피드로 확인할 수 있습니다.",
                priority="High",
                tech_suggestions=["팔로우 그래프", "피드 알고리즘", "무한 스크롤"]
            ),
        ])
        fr_id += 3

    # 5. 예약 시스템 특화 기능
    elif is_booking:
        requirements.extend([
            FunctionalRequirement(
                id=f"FR-{fr_id:03d}",
                title="날짜/시간 검색 및 예약",
                description="사용자가 원하는 날짜와 시간대를 검색하고 예약할 수 있습니다.",
                priority="High",
                tech_suggestions=["캘린더 UI", "실시간 재고 확인", "중복 예약 방지"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+1:03d}",
                title="예약 확인 및 취소",
                description="예약 내역을 조회하고, 취소 정책에 따라 예약을 취소할 수 있습니다.",
                priority="High",
                tech_suggestions=["이메일/SMS 알림", "환불 처리", "취소 수수료 계산"]
            ),
        ])
        fr_id += 2

    # 6. 배달 서비스 특화 기능
    elif is_delivery:
        requirements.extend([
            FunctionalRequirement(
                id=f"FR-{fr_id:03d}",
                title="음식점 및 메뉴 검색",
                description="위치 기반으로 음식점을 검색하고, 메뉴를 조회할 수 있습니다.",
                priority="High",
                tech_suggestions=["지도 API", "위치 기반 검색", "필터링"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+1:03d}",
                title="주문 및 배달 추적",
                description="음식을 주문하고, 실시간으로 배달 상태를 추적할 수 있습니다.",
                priority="High",
                tech_suggestions=["실시간 위치 추적", "푸시 알림", "배달 상태 관리"]
            ),
        ])
        fr_id += 2

    # 7. 실시간 기능이 필요한 경우
    if is_realtime:
        requirements.append(FunctionalRequirement(
            id=f"FR-{fr_id:03d}",
            title="실시간 채팅 및 알림",
            description="사용자 간 실시간 메시지 전송 및 시스템 알림을 제공합니다.",
            priority="High",
            tech_suggestions=["WebSocket", "Socket.io", "Redis Pub/Sub", "FCM"]
        ))
        fr_id += 1

    # 8. 결제 기능이 명시된 경우 (아직 추가되지 않았다면)
    if payment_info and payment_info != "지정되지 않음" and not any(req.title == "결제 시스템" for req in requirements):
        requirements.append(FunctionalRequirement(
            id=f"FR-{fr_id:03d}",
            title="결제 처리",
            description=f"{payment_info} 결제 수단을 지원하고, 결제 내역을 관리합니다.",
            priority="High",
            tech_suggestions=["PG 연동", "결제 게이트웨이", "보안 결제"]
        ))
        fr_id += 1

    # 9. 기본 CRUD 기능 (특정 프로젝트 유형이 없을 경우만)
    if not requirements or len(requirements) < 2:
        requirements.extend([
            FunctionalRequirement(
                id=f"FR-{fr_id:03d}",
                title="데이터 조회",
                description="사용자가 데이터 목록을 조회하고 상세 정보를 확인할 수 있습니다.",
                priority="Medium",
                tech_suggestions=["REST API", "페이지네이션", "검색 필터"]
            ),
            FunctionalRequirement(
                id=f"FR-{fr_id+1:03d}",
                title="데이터 생성 및 수정",
                description="사용자가 새로운 데이터를 생성하고, 기존 데이터를 수정할 수 있습니다.",
                priority="Medium",
                tech_suggestions=["Form Validation", "REST API", "에러 핸들링"]
            ),
        ])

    return requirements


def _extract_info_smart(collected_info: dict, category: str, default: str = None) -> str:
    """
    collected_info에서 특정 카테고리 정보를 스마트하게 추출
    InfoExtractor에서 이미 추출된 깔끔한 정보를 우선 사용

    Args:
        collected_info: 수집된 정보 딕셔너리
        category: 추출할 카테고리 (payment, authentication, scale, deployment, project_type)
        default: 기본값 (None이면 정보 없음)

    Returns:
        추출된 정보 문자열 또는 None
    """
    # 1. InfoExtractor가 이미 추출한 정보가 있으면 우선 사용
    if category in collected_info and collected_info[category]:
        value = collected_info[category]
        # 값이 긴 문장이 아닌 경우만 반환 (InfoExtractor가 제대로 추출한 경우)
        if len(value) < 50:  # 50자 이하만 유효한 정보로 간주
            return value

    # 2. response_X에서 수동으로 추출 (백업)
    for key, value in collected_info.items():
        if not key.startswith("response_"):
            continue

        # value가 None이거나 빈 문자열이거나 문자열이 아니면 스킵
        if not value or not isinstance(value, str):
            continue

        value_lower = safe_lower(value)

        # 카테고리별 키워드 기반 추출
        if category == "payment":
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
                if keyword in value_lower:
                    return pg_name

        elif category == "authentication":
            if "oauth" in value_lower:
                return "OAuth 2.0"
            if "jwt" in value_lower:
                return "JWT 토큰 인증"
            socials = []
            if "카카오" in value_lower:
                socials.append("카카오")
            if "네이버" in value_lower:
                socials.append("네이버")
            if "구글" in value_lower:
                socials.append("구글")
            if socials:
                return f"{'/'.join(socials)} 소셜 로그인"

        elif category == "scale":
            import re
            # "월 1만 명", "500명" 등 패턴 찾기
            patterns = [
                r'(\d+)\s*만\s*명',
                r'(\d+)\s*천\s*명',
                r'(\d+)\s*명'
            ]
            for pattern in patterns:
                match = re.search(pattern, value)
                if match:
                    number = match.group(1)
                    if "만" in value:
                        return f"{number}만 명"
                    elif "천" in value:
                        return f"{number}천 명"
                    else:
                        return f"{number}명"

        elif category == "deployment":
            deploy_map = {
                "aws": "AWS",
                "gcp": "GCP",
                "azure": "Azure",
                "클라우드": "클라우드",
                "온프레미스": "온프레미스",
                "도커": "Docker",
                "쿠버네티스": "Kubernetes"
            }
            for keyword, deploy_name in deploy_map.items():
                if keyword in value_lower:
                    return deploy_name

    return default


def writer_agent(state: RequirementState) -> RequirementState:
    """
    최종 SRS 문서를 생성하는 에이전트 (더미)

    Args:
        state: 현재 요구사항 상태

    Returns:
        업데이트된 요구사항 상태
    """
    # collected_info에서 사용자 답변 추출 (스마트 추출 함수 사용)
    project_name = _extract_info_smart(state.collected_info, "project_type", "프로젝트")
    payment_info = _extract_info_smart(state.collected_info, "payment", None)
    scale_info = _extract_info_smart(state.collected_info, "scale", None)
    auth_info = _extract_info_smart(state.collected_info, "authentication", None)
    deployment_info = _extract_info_smart(state.collected_info, "deployment", None)

    # 사용자 입력을 반영한 개요 생성 (수집된 정보만 표시)
    requirements_list = []
    requirements_list.append(f"- 프로젝트 유형: {project_name}")
    if payment_info:
        requirements_list.append(f"- 결제 수단: {payment_info}")
    if scale_info:
        requirements_list.append(f"- 예상 규모: {scale_info}")
    if auth_info:
        requirements_list.append(f"- 인증 방식: {auth_info}")
    if deployment_info:
        requirements_list.append(f"- 배포 환경: {deployment_info}")

    overview = f"""
{state.collected_info.get('initial_request', state.user_input)}

**수집된 요구사항:**
{chr(10).join(requirements_list)}
    """.strip()

    # 비기능 요구사항에 사용자 답변 반영 (정보가 있는 경우만)
    nfr_list = ["응답 시간: 평균 1초 이내"]
    if scale_info:
        nfr_list.append(f"예상 규모: {scale_info}")
    nfr_list.append("가용성: 99.9% uptime")

    # 동적 기능 요구사항 생성 - 프로젝트 유형에 맞춰 생성
    functional_requirements_list = _generate_functional_requirements(
        state.user_input,
        state.collected_info,
        auth_info,
        payment_info
    )

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

    # Assumptions에 사용자 답변 반영 (정보가 있는 경우만 추가)
    assumptions_list = []
    if deployment_info:
        assumptions_list.append(f"{deployment_info} 환경에 배포합니다")
    else:
        assumptions_list.append("클라우드 인프라 사용을 가정합니다")

    assumptions_list.append("개발 기간은 3개월로 가정합니다")

    if payment_info:
        assumptions_list.append(f"결제 수단: {payment_info}")
    if auth_info:
        assumptions_list.append(f"인증 방식: {auth_info}")

    # SRS 문서 생성
    dummy_srs = SRSDocument(
        project_name=project_name,
        overview=overview,
        functional_requirements=functional_requirements_list,
        non_functional_requirements=nfr_list,
        tech_stack=tech_stack_list,
        test_scenarios=test_scenarios_list,
        assumptions=assumptions_list
    )

    # JSON으로 변환하여 저장
    state.final_srs = dummy_srs.model_dump_json(indent=2)

    return state
