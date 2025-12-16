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
    # 순서대로 질문할 질문 리스트 (순서 유지를 위해 리스트 사용)
    question_sequence = [
        ("project_name", "프로젝트 이름은 무엇인가요?"),
        ("payment", "결제 수단은 어떤 것을 지원하나요? (신용카드, 가상계좌, 간편결제 등)"),
        ("scale", "예상되는 일일 주문 건수와 동시 접속자 수는 얼마나 되나요?"),
        ("authentication", "사용자 인증 방식은 어떻게 할 예정인가요? (자체 회원가입, 소셜 로그인 등)"),
        ("deployment", "배포 환경은 어디인가요? (AWS, GCP, Azure, 온프레미스 등)")
    ]

    # 현재까지 답변받은 질문 개수 확인
    answered_count = len(state.collected_info)

    # 아직 답변받지 않은 다음 질문 찾기
    if answered_count < len(question_sequence):
        # 다음 질문 하나만 선택
        next_category, next_question = question_sequence[answered_count]

        # State 업데이트 (한 개의 질문만)
        state.questions = [next_question]

        # 메시지 추가
        state.messages.append(
            Message(
                role="assistant",
                content=f"추가 정보가 필요합니다:\n\n{next_question}"
            )
        )
    else:
        # 모든 정보가 수집되었으면 빈 질문 리스트
        state.questions = []

    return state
