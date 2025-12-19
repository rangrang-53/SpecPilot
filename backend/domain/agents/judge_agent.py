"""Judge Agent - LLM 기반 완전성 평가"""
import json
from backend.domain.models.state import RequirementState, Message
from backend.infrastructure.llm.gemini_client import get_gemini_client
from backend.infrastructure.prompts.judge_prompt import (
    JUDGE_SYSTEM_PROMPT,
    get_judge_prompt
)


def judge_agent(state: RequirementState) -> RequirementState:
    """
    수집된 정보의 완전성을 평가하는 에이전트 (LLM 기반)

    Args:
        state: 현재 요구사항 상태

    Returns:
        업데이트된 요구사항 상태
    """
    # iteration 제한 체크
    if state.iteration_count >= 10:
        state.is_complete = True
        state.judge_feedback = "최대 반복 횟수에 도달했습니다. 현재 수집된 정보로 SRS를 생성합니다."
        return state

    # LLM 클라이언트 가져오기
    llm_client = get_gemini_client()

    # 대화 히스토리 생성
    conversation_history = "\n".join([
        f"{msg.role}: {msg.content}" for msg in state.messages
    ])

    # 프롬프트 생성
    user_prompt = get_judge_prompt(
        collected_info=state.collected_info,
        conversation_history=conversation_history
    )

    try:
        # LLM 호출하여 평가 수행
        response = llm_client.generate_with_context(
            system_prompt=JUDGE_SYSTEM_PROMPT,
            user_message=user_prompt
        )

        # 응답 파싱 (decision, completeness_score, feedback 추출)
        decision = "reject"  # 기본값
        completeness_score = 0.0
        feedback = ""

        # 간단한 파싱: "approve" 또는 "reject" 키워드 찾기
        response_lower = response.lower()

        if "approve" in response_lower or "충분" in response or "완료" in response:
            decision = "approve"
            completeness_score = 0.8
        elif "reject" in response_lower or "부족" in response or "필요" in response:
            decision = "reject"
            completeness_score = 0.4

        # completeness_score 추출 시도
        if "completeness_score" in response_lower:
            try:
                # "completeness_score: 0.7" 형태 찾기
                score_str = response.split("completeness_score")[1].split()[0].strip(':').strip()
                completeness_score = float(score_str)
            except:
                pass

        # feedback 추출
        feedback_lines = []
        for line in response.split('\n'):
            line = line.strip()
            if line and not line.startswith('-') and not line.startswith('*'):
                # JSON 키가 아닌 일반 텍스트만 피드백으로 사용
                if not any(key in line.lower() for key in ['decision', 'completeness', 'missing']):
                    feedback_lines.append(line)

        feedback = " ".join(feedback_lines[:3])  # 최대 3줄

        # State 업데이트
        if decision == "approve" or completeness_score >= 0.7:
            state.is_complete = True
            state.judge_feedback = feedback or "충분한 정보가 수집되었습니다. SRS 문서를 생성할 수 있습니다."
        else:
            state.is_complete = False
            state.judge_feedback = feedback or "추가 정보가 필요합니다."

    except Exception as e:
        print(f"⚠️ Judge Agent LLM error: {e}")
        print("⚠️ Falling back to strict evaluation")

        # Fallback: 엄격한 평가 로직
        info_count = len(state.collected_info)
        required_count = 5  # 최소 5개 정보 필요

        # 필수 카테고리 확인
        has_project_type = "project_type" in state.collected_info
        has_scale = "scale" in state.collected_info
        has_auth = "authentication" in state.collected_info
        has_deployment = "deployment" in state.collected_info

        missing_items = []
        if not has_auth:
            missing_items.append("인증 방식")
        if not has_deployment:
            missing_items.append("배포 환경")
        if not has_scale:
            missing_items.append("예상 규모")

        # 정보 개수와 필수 항목 모두 충족해야 approve
        if info_count >= required_count and not missing_items:
            state.is_complete = True
            state.judge_feedback = "충분한 정보가 수집되었습니다. SRS 문서를 생성할 수 있습니다."
        else:
            state.is_complete = False
            if missing_items:
                missing_str = ", ".join(missing_items)
                state.judge_feedback = f"추가 정보 필요: {missing_str} (현재 {info_count}/{required_count}개 수집)"
            else:
                state.judge_feedback = f"추가 정보가 필요합니다. (현재 {info_count}/{required_count}개 정보 수집됨)"

    return state
