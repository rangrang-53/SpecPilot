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

        print(f"🔍 [DEBUG] Consultant LLM Response: {response}")
        print(f"🔍 [DEBUG] Collected info: {state.collected_info}")

        # 응답 파싱: 프롬프트가 "질문만 출력"하라고 했으므로 전체 응답을 질문으로 사용
        response_clean = response.strip()

        # 만약 질문 형태가 아니면 (물음표가 없으면) 기본 질문 사용
        if '?' in response_clean or '？' in response_clean:
            # 여러 줄이 있으면 첫 번째 줄만 사용
            first_line = response_clean.split('\n')[0].strip()
            questions = [first_line]
        else:
            # 질문 형태가 아니면 fallback
            print(f"⚠️ [DEBUG] LLM response is not a question: {response_clean}")
            questions = ["프로젝트에 대해 더 자세히 설명해주실 수 있나요?"]

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
