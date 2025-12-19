"""Consultant Agent - LLM 기반 질문 생성"""
from backend.domain.models.state import RequirementState, Message
from backend.infrastructure.llm.gemini_client import get_gemini_client
from backend.infrastructure.prompts.consultant_prompt import (
    CONSULTANT_SYSTEM_PROMPT,
    get_consultant_prompt
)


def consultant_agent(state: RequirementState) -> RequirementState:
    """
    사용자 입력을 분석하고 추가 질문을 생성하는 에이전트 (LLM 기반)

    Args:
        state: 현재 요구사항 상태

    Returns:
        업데이트된 요구사항 상태
    """
    # LLM 클라이언트 가져오기
    llm_client = get_gemini_client()

    # 대화 히스토리 생성 (assistant 메시지만 추출 - 이미 물어본 질문들)
    conversation_history = "\n".join([
        f"Already asked: {msg.content}" for msg in state.messages
        if msg.role == "assistant"
    ])

    # 프롬프트 생성
    user_prompt = get_consultant_prompt(
        collected_info=state.collected_info,
        user_input=state.user_input,
        conversation_history=conversation_history
    )

    try:
        # LLM 호출하여 질문 생성
        response = llm_client.generate_with_context(
            system_prompt=CONSULTANT_SYSTEM_PROMPT,
            user_message=user_prompt
        )

        # 응답 파싱: 프롬프트가 "질문만 출력"하라고 했으므로 전체 응답을 질문으로 사용
        response_clean = response.strip()

        # 만약 질문 형태가 아니면 (물음표가 없으면) 기본 질문 사용
        if '?' in response_clean or '？' in response_clean:
            # 여러 줄이 있으면 첫 번째 줄만 사용
            first_line = response_clean.split('\n')[0].strip()
            questions = [first_line]
        else:
            # 질문 형태가 아니면 fallback
            questions = ["프로젝트에 대해 더 자세히 설명해주실 수 있나요?"]

        # State 업데이트
        state.questions = questions

        # 메시지 추가 (예시 포함)
        if questions:
            main_question = questions[0]
            # 질문에 맞는 예시 추가
            example_hint = _get_example_hint_for_question(main_question, state.collected_info)

            if example_hint:
                full_message = f"추가 정보가 필요합니다:\n\n{main_question}\n\n{example_hint}"
            else:
                full_message = f"추가 정보가 필요합니다:\n\n{main_question}"

            state.messages.append(
                Message(
                    role="assistant",
                    content=full_message
                )
            )

    except Exception as e:
        print(f"⚠️ Consultant Agent LLM error: {e}")
        print(f"⚠️ Error details: {str(e)}")
        print("⚠️ Falling back to default questions")

        # Fallback: 기본 질문 사용
        default_questions = [
            "프로젝트의 주요 기능은 무엇인가요?"
        ]

        state.questions = default_questions
        state.messages.append(
            Message(
                role="assistant",
                content=f"추가 정보가 필요합니다:\n\n{default_questions[0]}"
            )
        )

    return state


def _get_example_hint_for_question(question: str, collected_info: dict) -> str:
    """
    질문에 맞는 간단한 예시 힌트 생성 (인라인용)

    Args:
        question: 생성된 질문
        collected_info: 수집된 정보

    Returns:
        예시 힌트 문자열 (없으면 None)
    """
    question_lower = question.lower() if question else ""

    # 결제 관련 질문
    if "결제" in question_lower or "pg" in question_lower:
        return "💡 예: 토스페이먼츠, KG이니시스, 카카오페이, 네이버페이 등"

    # 인증 관련 질문
    elif "인증" in question_lower or "로그인" in question_lower:
        return "💡 예: JWT 토큰, OAuth 2.0, 소셜로그인(카카오/네이버/구글) 등"

    # 규모 관련 질문
    elif "규모" in question_lower or "사용자" in question_lower or "트래픽" in question_lower or "접속" in question_lower:
        return "💡 예: 일 500명, 일 1,000~5,000명, 동시접속 100명 등"

    # 배포 환경 관련 질문
    elif "배포" in question_lower or "서버" in question_lower or "인프라" in question_lower or "클라우드" in question_lower:
        return "💡 예: AWS, GCP, Azure, Docker/Kubernetes 등"

    # 기능 관련 질문
    elif "기능" in question_lower:
        project_type = collected_info.get("project_type", "")
        if "이커머스" in project_type or "쇼핑" in project_type:
            return "💡 예: 상품 검색/필터링, 장바구니, 주문/결제, 리뷰, 위시리스트 등"
        else:
            return "💡 예: 회원가입, 게시글 작성, 댓글, 검색, 알림 등"

    # 데이터베이스 관련 질문
    elif "데이터베이스" in question_lower or "db" in question_lower:
        return "💡 예: PostgreSQL, MySQL, MongoDB, Redis 등"

    # 기타 - 힌트 없음
    else:
        return None


def _generate_example_response(last_question: str, collected_info: dict) -> str:
    """
    마지막 질문에 대한 예시를 제공하는 응답 생성

    Args:
        last_question: 마지막으로 한 질문
        collected_info: 수집된 정보

    Returns:
        예시를 포함한 응답 문자열
    """
    question_lower = last_question.lower() if last_question else ""

    # 결제 관련 질문
    if "결제" in question_lower or "pg" in question_lower:
        return """예를 들어:
- 토스페이먼츠
- KG 이니시스
- 나이스페이먼츠
- 카카오페이
- 네이버페이

위 중에서 선택하거나 사용하실 PG사를 말씀해주세요."""

    # 인증 관련 질문
    elif "인증" in question_lower or "로그인" in question_lower:
        return """예를 들어:
- JWT 토큰 인증
- OAuth 2.0
- 소셜 로그인 (카카오, 네이버, 구글)
- 이메일/비밀번호 인증

어떤 방식을 사용하실 건가요?"""

    # 규모 관련 질문
    elif "규모" in question_lower or "사용자" in question_lower or "트래픽" in question_lower:
        return """예를 들어:
- 소규모: 일 500명 이하
- 중규모: 일 1,000~5,000명
- 대규모: 일 1만 명 이상
- 동시접속: 동시에 100명, 500명 등

예상하시는 규모를 말씀해주세요."""

    # 배포 환경 관련 질문
    elif "배포" in question_lower or "서버" in question_lower or "인프라" in question_lower:
        return """예를 들어:
- AWS (Amazon Web Services)
- GCP (Google Cloud Platform)
- Azure (Microsoft Azure)
- 온프레미스 (자체 서버)
- Docker, Kubernetes

어떤 환경에 배포하실 건가요?"""

    # 기능 관련 질문
    elif "기능" in question_lower:
        project_type = collected_info.get("project_type", "")
        if "이커머스" in project_type or "쇼핑" in project_type:
            return """예를 들어:
- 상품 검색 및 필터링
- 장바구니 기능
- 주문 및 결제
- 리뷰 및 평점
- 위시리스트
- 쿠폰/할인 기능

어떤 기능들이 필요하신가요?"""
        else:
            return """구체적인 기능들을 말씀해주시면 더 정확한 SRS를 작성할 수 있습니다.
예: "회원가입, 게시글 작성, 댓글 기능" 등"""

    # 일반적인 예시 요청
    else:
        return """구체적으로 어떤 부분에 대한 예시가 필요하신가요?

일반적인 예시:
- 결제: 토스페이먼츠, KG이니시스 등
- 인증: JWT, 소셜로그인 등
- 규모: 일 1000명, 동시접속 100명 등
- 배포: AWS, GCP 등

원하시는 항목을 선택하거나 직접 답변해주세요."""
