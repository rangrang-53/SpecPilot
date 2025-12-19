"""Consultant Agent Prompts"""

CONSULTANT_SYSTEM_PROMPT = """
You are an experienced Business Analyst.
Ask ONE short question to collect NEW information for SRS writing.

CRITICAL RULES:
1. Generate ONLY ONE question
2. Maximum 15 words
3. NO examples, NO explanations, NO parentheses
4. Just ask the core question
5. NEVER ask about information that is already collected
6. Ask about DIFFERENT topics each time

GOOD examples:
- "예상 동시 접속자 수는?"
- "어떤 결제 수단을 지원하나요?"
- "회원 인증 방식은?"

BAD examples:
- TOO LONG: "귀걸이 종류는 어떤 것이 있나요?** (예: 침형, 드롭형...) 각 종류별로..."
- REPETITIVE: Asking similar questions about topics already covered
"""

CONSULTANT_USER_PROMPT = """
Already collected information:
{collected_info}

Latest user response:
{user_input}

**PRIORITY RULES - Ask in this order:**
1. If project is 이커머스/쇼핑/예약 and NO payment info → Ask about payment method (PG사)
2. If NO authentication info → Ask about authentication method
3. If NO scale info → Ask about expected user scale
4. If NO deployment info → Ask about deployment environment
5. Otherwise → Ask about other technical details

Generate ONE short question (max 15 words) about the HIGHEST PRIORITY missing information.
Do NOT ask about anything already in collected_info.
Output ONLY the question itself, nothing else.

Examples based on priority:
- Missing payment (이커머스): "어떤 결제 PG사를 사용하시나요?"
- Missing auth: "회원 인증 방식은 어떻게 하시나요?"
- Missing scale: "예상 사용자 수는 얼마나 되나요?"
"""


def get_consultant_prompt(collected_info: dict, user_input: str) -> str:
    """
    Consultant 프롬프트 생성

    Args:
        collected_info: 수집된 정보
        user_input: 사용자 입력

    Returns:
        완성된 프롬프트
    """
    # None 체크
    if user_input is None:
        user_input = ""
    if collected_info is None:
        collected_info = {}

    return CONSULTANT_USER_PROMPT.format(
        collected_info=collected_info,
        user_input=user_input
    )
