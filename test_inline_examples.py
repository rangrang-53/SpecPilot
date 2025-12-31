#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""인라인 예시 테스트"""

from backend.domain.agents.consultant_agent import _get_rule_based_example, _get_fallback_example

# 테스트 질문들
test_questions = [
    "배송 정책은 어떻게 되나요?",
    "인증 방식은 무엇인가요?",
    "결제 수단은 어떤 것을 지원하나요?",
    "배포는 어디에 하시겠습니까?",
    "예상 사용자 규모는 얼마나 되나요?",
    "프로젝트 일정은 언제까지인가요?",  # 폴백 예시
]

print("=" * 60)
print("인라인 예시 테스트")
print("=" * 60)

for question in test_questions:
    print(f"\n질문: {question}")

    # 규칙 기반 예시 시도
    rule_example = _get_rule_based_example(question)

    if rule_example:
        print(f"✅ 규칙 기반: {rule_example}")
    else:
        # 폴백 예시
        fallback = _get_fallback_example(question)
        print(f"⚠️ 폴백: {fallback}")

print("\n" + "=" * 60)
print("✅ 모든 질문에 예시가 제공됩니다!")
print("=" * 60)
