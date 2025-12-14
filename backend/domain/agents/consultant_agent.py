"""Consultant Agent - 더미 구현"""
from backend.domain.models.state import RequirementState, Message


def consultant_agent(state: RequirementState) -> RequirementState:
    """
    사용자 입력을 분석하고 추가 질문을 생성하는 에이전트 (더미)

    Args:
        state: 현재 요구사항 상태

    Returns:
        업데이트된 요구사항 상태
    """
    # 더미 질문 생성
    dummy_questions = [
        "결제 수단은 어떤 것을 지원하나요? (신용카드, 가상계좌, 간편결제 등)",
        "예상되는 일일 주문 건수와 동시 접속자 수는 얼마나 되나요?",
        "사용자 인증 방식은 어떻게 할 예정인가요? (자체 회원가입, 소셜 로그인 등)",
        "배포 환경은 어디인가요? (AWS, GCP, Azure, 온프레미스 등)"
    ]

    # State 업데이트
    state.questions = dummy_questions

    # 메시지 추가
    questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(dummy_questions)])
    state.messages.append(
        Message(
            role="assistant",
            content=f"추가 정보가 필요합니다:\n{questions_text}"
        )
    )

    return state
