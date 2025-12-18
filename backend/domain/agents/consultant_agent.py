"""Consultant Agent - LLM 기반 질문 생성 및 정보 수집"""
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
    # 1. 사용자 답변에서 정보 추출하여 collected_info에 저장
    if state.iteration_count > 0:  # 첫 번째가 아니면 답변 저장
        # 간단한 키워드 기반 정보 추출
        user_input_lower = state.user_input.lower()

        # 카테고리별로 정보 저장
        if not state.collected_info.get("main_features"):
            state.collected_info["main_features"] = state.user_input

        # 결제 관련
        if any(keyword in user_input_lower for keyword in ["결제", "payment", "페이", "카드"]):
            state.collected_info["payment"] = state.user_input

        # 규모 관련
        if any(keyword in user_input_lower for keyword in ["사용자", "명", "규모", "트래픽", "동시"]):
            state.collected_info["scale"] = state.user_input

        # 인증 관련
        if any(keyword in user_input_lower for keyword in ["인증", "로그인", "회원", "소셜"]):
            state.collected_info["authentication"] = state.user_input

        # 배포 관련
        if any(keyword in user_input_lower for keyword in ["배포", "aws", "gcp", "azure", "클라우드", "서버"]):
            state.collected_info["deployment"] = state.user_input

        # 기타 정보도 저장
        if "other_info" not in state.collected_info:
            state.collected_info["other_info"] = []
        state.collected_info["other_info"].append(state.user_input)

    # 2. LLM 클라이언트 가져오기
    llm_client = get_gemini_client()

    # 3. 프롬프트 생성
    user_prompt = get_consultant_prompt(
        collected_info=state.collected_info,
        user_input=state.user_input
    )

    try:
        # 4. LLM 호출하여 질문 생성
        response = llm_client.generate_with_context(
            system_prompt=CONSULTANT_SYSTEM_PROMPT,
            user_message=user_prompt
        )

        # 5. 응답을 줄 단위로 나누고 질문만 추출
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            # 번호가 있는 질문만 추출 (예: "1. 질문내용", "- 질문내용")
            if line and (
                line[0].isdigit() or
                line.startswith('-') or
                line.startswith('*') or
                line.startswith('•')
            ):
                # 번호 및 마크다운 기호 제거
                cleaned = line.lstrip('0123456789.-*• ').strip()
                if cleaned and '?' in cleaned:  # 질문 형태만
                    questions.append(cleaned)

        # 질문이 없으면 기본 질문 사용
        if not questions:
            questions = ["프로젝트에 대해 더 자세히 설명해주실 수 있나요?"]

        # 최대 3개 질문으로 제한 (한 번에 너무 많으면 부담)
        questions = questions[:3]

        # 6. State 업데이트
        state.questions = questions

        # 7. 메시지 추가 (첫 번째 질문만 표시)
        if questions:
            state.messages.append(
                Message(
                    role="assistant",
                    content=f"추가 정보가 필요합니다:\n\n{questions[0]}"
                )
            )

    except Exception as e:
        print(f"⚠️ Consultant Agent LLM error: {e}")
        print("⚠️ Falling back to default questions")

        # Fallback: 기본 질문 사용
        default_questions = [
            "프로젝트의 주요 기능은 무엇인가요?",
            "예상 사용자 수는 얼마나 되나요?",
            "배포 환경은 어디인가요? (클라우드, 온프레미스 등)"
        ]

        state.questions = default_questions
        state.messages.append(
            Message(
                role="assistant",
                content=f"추가 정보가 필요합니다:\n\n{default_questions[0]}"
            )
        )

    return state
