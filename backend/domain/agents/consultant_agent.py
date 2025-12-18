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

    # 프롬프트 생성
    user_prompt = get_consultant_prompt(
        collected_info=state.collected_info,
        user_input=state.user_input
    )

    try:
        # LLM 호출하여 질문 생성
        response = llm_client.generate_with_context(
            system_prompt=CONSULTANT_SYSTEM_PROMPT,
            user_message=user_prompt
        )

        # 응답을 줄 단위로 나누고 질문만 추출
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

        # 첫 번째 질문만 사용
        questions = [questions[0]]

        # State 업데이트
        state.questions = questions

        # 메시지 추가
        if questions:
            state.messages.append(
                Message(
                    role="assistant",
                    content=f"추가 정보가 필요합니다:\n\n{questions[0]}"
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
