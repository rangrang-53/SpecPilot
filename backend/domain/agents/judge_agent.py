"""Judge Agent - 더미 구현"""
from backend.domain.models.state import RequirementState, Message


def judge_agent(state: RequirementState) -> RequirementState:
    """
    수집된 정보의 완전성을 평가하는 에이전트 (더미)

    Args:
        state: 현재 요구사항 상태

    Returns:
        업데이트된 요구사항 상태
    """
    # 더미 평가 로직
    # collected_info에 최소 3개 이상의 키가 있으면 완료로 간주
    info_count = len(state.collected_info)

    if info_count >= 3:
        state.is_complete = True
        state.judge_feedback = "충분한 정보가 수집되었습니다. SRS 문서를 생성할 수 있습니다."
    else:
        state.is_complete = False
        state.judge_feedback = f"추가 정보가 필요합니다. (현재 {info_count}/3개 정보 수집됨)"

        # 피드백 메시지 추가
        state.messages.append(
            Message(
                role="system",
                content=f"[Judge] {state.judge_feedback}"
            )
        )

    return state
