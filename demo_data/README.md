# SpecPilot 데모 데이터

실제 테스트용 시나리오 데이터와 실행 스크립트입니다.

## 📁 파일 구조

```
demo_data/
├── README.md                      # 이 파일
├── run_demo.py                    # 데모 실행 스크립트
├── scenario_1_ecommerce.json      # 이커머스 쇼핑몰
├── scenario_2_chat.json           # 실시간 채팅 앱
├── scenario_3_intranet.json       # 사내 인트라넷
├── scenario_4_booking.json        # PT 예약 시스템
└── scenario_5_iot.json            # IoT 모니터링
```

## 🚀 사용법

### 1. 단일 시나리오 실행 (수동 입력)

```bash
python demo_data/run_demo.py --scenario 1
```

AI 질문에 직접 답변을 입력합니다.

### 2. 단일 시나리오 자동 실행

```bash
python demo_data/run_demo.py --scenario ecommerce --auto
```

시나리오 파일에 정의된 답변을 자동으로 사용합니다.

### 3. 모든 시나리오 자동 실행

```bash
python demo_data/run_demo.py --all --auto
```

5개 시나리오를 순차적으로 자동 실행합니다.

## 📋 시나리오 목록

| 번호 | 이름 | 설명 |
|------|------|------|
| 1, ecommerce | 이커머스 쇼핑몰 | 온라인 의류 쇼핑몰 |
| 2, chat | 실시간 채팅 앱 | 팀 협업 채팅 |
| 3, intranet | 사내 인트라넷 | 전자결재, 조직도 |
| 4, booking | PT 예약 시스템 | 헬스장 예약 |
| 5, iot | IoT 대시보드 | 공장 설비 모니터링 |

## 📄 시나리오 파일 형식

```json
{
  "scenario_name": "시나리오 이름",
  "initial_input": "초기 입력 텍스트...",
  "expected_questions": [
    {
      "question": "예상 질문",
      "answer": "답변"
    }
  ],
  "expected_tech_stack": {
    "backend": ["기술1", "기술2"],
    "frontend": ["기술3"]
  }
}
```

## 🎯 예시 실행

### 이커머스 시나리오 (자동)

```bash
python demo_data/run_demo.py -s 1 --auto
```

**출력 예시:**
```
================================================
📋 시나리오: 이커머스 쇼핑몰
================================================

🚀 세션 시작...
✅ 세션 생성 완료: 7a4009c5-2ca7...

────────────────────────────────────────────
🤖 AI 질문 #1:
────────────────────────────────────────────
사용자 인증 방식은 어떻게 하시겠습니까?

💬 답변 (자동): 이메일/비밀번호 방식과...

[...]

🎉 SRS 문서 생성 완료!
📊 생성된 내용 요약:
  - 기능 요구사항: 12개
  - 테스트 시나리오: 8개
💾 결과 저장: demo_data/output_이커머스_쇼핑몰.json
```

## 💾 출력 파일

실행이 완료되면 `output_*.json` 파일이 생성됩니다:

```
demo_data/
├── output_이커머스_쇼핑몰.json
├── output_실시간_채팅_앱.json
├── output_사내_인트라넷.json
├── output_PT_예약_시스템.json
└── output_IoT_모니터링_대시보드.json
```

이 파일들은 완성된 SRS 문서(JSON 형식)입니다.

## 🛠 개발자용

### 새 시나리오 추가

1. `scenario_X_name.json` 파일 생성
2. 위의 형식에 맞춰 작성
3. `run_demo.py`의 `SCENARIOS` 딕셔너리에 추가

### 스크립트 옵션

```
--scenario, -s  : 시나리오 선택
--all           : 전체 실행
--auto          : 자동 답변
```

## ⚠️ 주의사항

- `.env` 파일에 `GOOGLE_API_KEY` 설정 필요
- 자동 모드에서도 API 호출로 인한 시간 소요
- 각 시나리오당 약 2-5분 소요
