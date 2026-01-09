#!/usr/bin/env python
"""
SpecPilot 데모 실행 스크립트

사용법:
    python demo_data/run_demo.py --scenario 1
    python demo_data/run_demo.py --scenario ecommerce
    python demo_data/run_demo.py --all
"""

import json
import sys
import argparse
from pathlib import Path
import os

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.application.use_cases.start_session_use_case import StartSessionUseCase
from backend.application.use_cases.continue_session_use_case import ContinueSessionUseCase


SCENARIOS = {
    "1": "scenario_1_ecommerce.json",
    "ecommerce": "scenario_1_ecommerce.json",
    "2": "scenario_2_chat.json",
    "chat": "scenario_2_chat.json",
    "3": "scenario_3_intranet.json",
    "intranet": "scenario_3_intranet.json",
    "4": "scenario_4_booking.json",
    "booking": "scenario_4_booking.json",
    "5": "scenario_5_iot.json",
    "iot": "scenario_5_iot.json",
}


def load_scenario(scenario_name: str) -> dict:
    """시나리오 파일 로드"""
    demo_dir = Path(__file__).parent
    scenario_file = demo_dir / SCENARIOS.get(scenario_name, scenario_name)

    if not scenario_file.exists():
        print(f"❌ 시나리오 파일을 찾을 수 없습니다: {scenario_file}")
        sys.exit(1)

    with open(scenario_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_scenario(scenario_data: dict, auto_answer: bool = False):
    """시나리오 실행"""
    print(f"\n{'='*60}")
    print(f"📋 시나리오: {scenario_data['scenario_name']}")
    print(f"{'='*60}\n")

    # 1. 세션 시작
    print("🚀 세션 시작...")
    print(f"\n초기 입력:\n{scenario_data['initial_input']}\n")

    start_uc = StartSessionUseCase()
    result = start_uc.execute(scenario_data['initial_input'])

    session_id = result['session_id']
    print(f"✅ 세션 생성 완료: {session_id[:20]}...\n")

    # 2. AI 질문에 답변
    continue_uc = ContinueSessionUseCase()
    iteration = 1

    while not result.get('is_complete', False):
        messages = result.get('messages', [])

        if not messages:
            print("⚠️ 메시지가 없습니다.")
            break

        # 마지막 AI 질문 출력
        last_message = messages[-1]
        if last_message['role'] == 'assistant':
            print(f"\n{'─'*60}")
            print(f"🤖 AI 질문 #{iteration}:")
            print(f"{'─'*60}")
            print(last_message['content'])
            print()

        # 답변 결정
        if auto_answer and iteration <= len(scenario_data.get('expected_questions', [])):
            # 자동 답변 모드
            expected_qa = scenario_data['expected_questions'][iteration - 1]
            user_answer = expected_qa['answer']
            print(f"💬 답변 (자동): {user_answer}\n")
        else:
            # 수동 입력 모드
            user_answer = input("💬 답변을 입력하세요 (종료: q): ").strip()
            if user_answer.lower() == 'q':
                print("\n❌ 사용자가 종료했습니다.")
                break

        # 답변 전송
        result = continue_uc.execute(session_id, user_answer)
        iteration += 1

        # 최대 반복 방지
        if iteration > 10:
            print("\n⚠️ 최대 반복 횟수 도달")
            break

    # 3. 완료 확인
    if result.get('is_complete', False):
        print(f"\n{'='*60}")
        print("🎉 SRS 문서 생성 완료!")
        print(f"{'='*60}\n")

        # SRS 조회
        from backend.application.use_cases.get_srs_use_case import GetSRSUseCase
        get_srs_uc = GetSRSUseCase()
        srs_result = get_srs_uc.execute(session_id)

        if srs_result.get('final_srs'):
            srs_data = json.loads(srs_result['final_srs'])

            print("📊 생성된 내용 요약:")
            print(f"  - 프로젝트명: {srs_data.get('project_name', 'N/A')}")
            print(f"  - 기능 요구사항: {len(srs_data.get('functional_requirements', []))}개")
            print(f"  - 비기능 요구사항: {len(srs_data.get('non_functional_requirements', []))}개")
            print(f"  - 기술 스택: {len(srs_data.get('tech_stack', []))}개 카테고리")
            print(f"  - 테스트 시나리오: {len(srs_data.get('test_scenarios', []))}개")

            # 결과 저장
            output_file = Path(__file__).parent / f"output_{scenario_data['scenario_name'].replace(' ', '_')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(srs_data, f, ensure_ascii=False, indent=2)

            print(f"\n💾 결과 저장: {output_file}")
        else:
            print("⚠️ SRS 문서를 찾을 수 없습니다.")
    else:
        print("\n⚠️ SRS 생성이 완료되지 않았습니다.")


def main():
    parser = argparse.ArgumentParser(description='SpecPilot 데모 실행')
    parser.add_argument(
        '--scenario', '-s',
        help='시나리오 번호 또는 이름 (1, 2, 3, 4, 5 또는 ecommerce, chat, intranet, booking, iot)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='모든 시나리오 실행'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='자동 답변 모드 (시나리오에 정의된 답변 사용)'
    )

    args = parser.parse_args()

    # 시나리오 목록 출력
    if not args.scenario and not args.all:
        print("\n사용 가능한 시나리오:")
        print("  1, ecommerce   - 이커머스 쇼핑몰")
        print("  2, chat        - 실시간 채팅 앱")
        print("  3, intranet    - 사내 인트라넷")
        print("  4, booking     - PT 예약 시스템")
        print("  5, iot         - IoT 모니터링 대시보드")
        print("\n사용법:")
        print("  python demo_data/run_demo.py --scenario 1")
        print("  python demo_data/run_demo.py --scenario ecommerce --auto")
        print("  python demo_data/run_demo.py --all --auto")
        sys.exit(0)

    # 실행
    if args.all:
        # 모든 시나리오 실행
        for scenario_key in ["1", "2", "3", "4", "5"]:
            scenario_data = load_scenario(scenario_key)
            run_scenario(scenario_data, auto_answer=args.auto)
            print("\n" + "="*60 + "\n")
    else:
        # 단일 시나리오 실행
        scenario_data = load_scenario(args.scenario)
        run_scenario(scenario_data, auto_answer=args.auto)


if __name__ == "__main__":
    main()
