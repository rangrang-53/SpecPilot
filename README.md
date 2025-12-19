# ✈️ SpecPilot: AI-Powered SRS Generator

> **"From Vague Ideas to Concrete Specs."**

모호한 아이디어를 명확한 기술 명세서(SRS)로 자동 전환하는 AI 에이전트

---

## 🎯 Why?

초기 기획 단계의 고질적 문제들:
- **불완전한 요구사항**: 고객/PM의 초기 요구사항은 대부분 불완전하고 모호함
- **반복적인 커뮤니케이션 비용**: 요구사항 명확화를 위한 수십 번의 이메일과 미팅
- **문서화 부담**: SRS 작성에 소요되는 막대한 시간
- **기술 스택 결정의 어려움**: 프로젝트 특성에 맞는 기술 선택의 불확실성

**SpecPilot은 Multi-Agent AI 시스템으로 이 모든 과정을 자동화합니다.**

---

## 🤖 How It Works

### 핵심 아이디어: **3개의 AI 에이전트가 협업**

```
User Input
    │
    ▼
┌──────────────────────┐
│  Consultant Agent    │  ← Google Gemini
│  (질문 생성)          │     사용자 입력 분석 → 맞춤형 질문 생성
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Judge Agent         │  ← Google Gemini
│  (완전성 평가)        │     정보 충분성 지능 평가 (max 5회)
└──────────┬───────────┘
           │
           ▼ (완료 시)
┌──────────────────────┐
│  Writer Agent        │  ← 규칙 기반 엔진
│  (SRS 생성)          │     동적 기술 스택 + 테스트 시나리오 생성
└──────────────────────┘
```

### 1. **Consultant Agent** (Google Gemini 2.0 Flash 기반)
- Business Analyst처럼 동작
- 사용자 입력 분석 → **컨텍스트 기반 질문 생성**
- 정적인 질문이 아닌, 프로젝트별 맞춤 질문
- 답변에서 자동으로 정보 추출 및 저장
- 우선순위 기반 질문 (결제 → 인증 → 규모 → 배포)

### 2. **Judge Agent** (Google Gemini 2.0 Flash 기반)
- QA/PM처럼 동작
- 수집된 정보의 **질** 평가
- 필수 항목 체크: 인증, 배포, 규모, 결제(이커머스 시)
- 부족 시 Consultant에게 추가 질문 요청, 충분 시 Writer로 이동
- 최대 10회 반복으로 과도한 질문 방지

### 3. **Writer Agent** (규칙 기반 엔진)
- **동적 기술 스택 선택**:
  - 프로젝트 특성 자동 분석 (이커머스, 실시간, 모바일 등)
  - 규모/유형에 따라 최적 기술 자동 선택
  - 예: 대규모 이커머스 → Spring Boot + MSA + Kafka
  - 예: 실시간 채팅 → Node.js + Socket.io + MongoDB

- **동적 테스트 시나리오 생성**:
  - 8가지 프로젝트 패턴 인식 (이커머스, 소셜, 예약, 실시간 등)
  - Gherkin Given-When-Then 시나리오 자동 생성
  - 프로젝트 유형별 맞춤형 테스트 케이스

---

## 🏗 Architecture

### Tech Stack
- **AI/LLM**: Google Gemini 2.0 Flash (Experimental)
- **Workflow Orchestration**: Custom Multi-Agent State Machine
- **Backend**: Python 3.11+, Pydantic (Type-Safe)
- **Frontend**: Streamlit (단일 통합 배포)
- **Architecture Pattern**: Clean Architecture + Multi-Agent System

### Design Decisions

#### 1. **왜 Multi-Agent Pattern?**
- 단일 LLM보다 **역할 분리**로 품질 향상
- Consultant: 질문 전문, Judge: 평가 전문, Writer: 생성 전문
- LangGraph로 에이전트 간 **상태 기반 전이** 관리

#### 2. **왜 Writer는 LLM 대신 규칙 기반?**
- 기술 스택 선택은 **일관성과 예측 가능성**이 중요
- LLM의 창의성보다 **검증된 베스트 프랙티스** 적용이 유리
- 키워드 기반 규칙 엔진으로 신뢰성 확보

#### 3. **왜 Session-based In-Memory?**
- 프로토타입 단계: 빠른 개발과 테스트
- UUID 기반 세션 관리로 상태 독립성 보장
- 향후 PostgreSQL/Redis로 마이그레이션 용이

---

## 🚀 Quick Start

### 1. API 키 받기 (무료!)
```bash
# Google Gemini API 키 발급 (무료 티어 제공)
# https://makersuite.google.com/app/apikey
```

### 2. 설치 및 실행
```bash
# 저장소 클론
git clone https://github.com/your-repo/SpecPilot.git
cd SpecPilot

# 가상환경 및 의존성 설치
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# API 키 설정
cp .env.example .env
# .env 파일 편집: GOOGLE_API_KEY=your-key-here

# 앱 실행
streamlit run frontend/app.py
```

### 3. 사용 예시
```
1. 프로젝트 입력: "음식 배달 앱을 만들고 싶습니다"
   ↓
2. AI 질문: "예상 사용자 수는 얼마나 되나요?"
   → 답변: "중소규모, 일 1000명 정도"
   ↓
3. AI 질문: "결제 시스템이 필요한가요?"
   → 답변: "네, 신용카드와 간편결제 지원 필요"
   ↓
4. SRS 자동 생성:
   - 기능 요구사항: 주문 관리, 결제, 배달 추적
   - 기술 스택: Node.js, React Native, PostgreSQL, Redis
   - 테스트 시나리오: 주문 생성, 결제 처리, 배달 상태 업데이트 등
```

---

## 📁 Project Structure

```
SpecPilot/
├── backend/
│   ├── domain/
│   │   ├── agents/
│   │   │   ├── consultant_agent.py    # LLM 기반 질문 생성
│   │   │   ├── judge_agent.py         # LLM 기반 완전성 평가
│   │   │   └── writer_agent.py        # 규칙 기반 SRS 생성
│   │   └── models/
│   │       ├── state.py               # RequirementState (Pydantic)
│   │       └── srs.py                 # SRSDocument
│   ├── infrastructure/
│   │   ├── llm/
│   │   │   └── gemini_client.py       # Google Gemini API 클라이언트
│   │   ├── graph/
│   │   │   └── workflow.py            # LangGraph 워크플로우
│   │   └── prompts/                   # Agent 프롬프트
│   └── application/
│       └── use_cases/                 # StartSession, ContinueSession
│
├── frontend/
│   ├── app.py                         # Streamlit UI (3 screens)
│   ├── services/
│   │   └── api_client.py              # 백엔드 직접 호출 (HTTP 제거)
│   └── utils/
│       └── srs_formatter.py           # JSON → Markdown 변환
│
├── .env.example                       # API 키 설정 템플릿
├── requirements.txt                   # 의존성
└── README.md
```

---

## 🎨 Key Features

### 동적 기술 스택 생성
```python
# 프로젝트 특성 자동 분석
if is_large_scale or is_ecommerce:
    backend = ["Spring Boot", "Microservices", "Kafka"]
elif is_realtime:
    backend = ["Node.js", "Socket.io", "MongoDB"]
else:
    backend = ["FastAPI", "PostgreSQL"]
```

### 동적 테스트 시나리오 생성
```gherkin
Feature: 상품 검색
  Scenario: 사용자가 상품을 검색한다
    Given 사용자가 메인 페이지에 있다
    When 검색창에 "노트북"을 입력하고 검색 버튼을 클릭한다
    Then 검색 결과 페이지에 관련 상품 목록이 표시된다
```

---

## 🔮 Future Roadmap

- [ ] **데이터베이스 영속화**: In-Memory → PostgreSQL/Redis
- [ ] **히스토리 관리**: 이전 SRS 재사용
- [ ] **Jira 통합**: SRS → Jira Epic/Story 자동 변환
- [ ] **코드 생성**: SRS → 프로젝트 스캐폴딩 자동화
- [ ] **협업 기능**: 팀 단위 SRS 공동 작성

---

## 📄 License

MIT License

## 👥 Author

**RANG** - SpecPilot v1.0

---

**SpecPilot** - "From Vague Ideas to Concrete Specs." ✈️
