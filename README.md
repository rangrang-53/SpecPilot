# ✈️ SpecPilot: AI-Powered SRS Generator

> **"From Vague Ideas to Concrete Specs."**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%202.0-4285F4.svg)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

모호한 아이디어를 명확한 기술 명세서(SRS)로 자동 전환하는 Multi-Agent AI 시스템

---

## 📑 Table of Contents

- [Why SpecPilot?](#-why-specpilot)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Development](#-development)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Why SpecPilot?

초기 기획 단계의 고질적 문제들:

- **불완전한 요구사항**: 고객/PM의 초기 요구사항은 대부분 불완전하고 모호함
- **반복적인 커뮤니케이션 비용**: 요구사항 명확화를 위한 수십 번의 이메일과 미팅
- **문서화 부담**: SRS 작성에 소요되는 막대한 시간 (평균 3-5일)
- **기술 스택 결정의 어려움**: 프로젝트 특성에 맞는 기술 선택의 불확실성

**SpecPilot은 Multi-Agent AI 시스템으로 이 모든 과정을 자동화합니다.**

### 💡 Key Benefits

- ⏱️ **시간 절약**: SRS 작성 시간을 3-5일 → 30분으로 단축
- 🎯 **정확성**: AI 기반 질문으로 누락된 요구사항 자동 발견
- 🔧 **맞춤형 기술 스택**: 프로젝트 특성에 최적화된 기술 자동 선택
- 📊 **일관성**: 표준화된 포맷으로 프로젝트 간 일관성 유지
- 🧪 **테스트 시나리오 자동 생성**: Gherkin 포맷의 테스트 케이스 자동 생성

---

## ✨ Key Features

### 1. Multi-Agent Collaboration System

3개의 전문화된 AI 에이전트가 협업하여 고품질 SRS를 생성합니다:

- **Consultant Agent** (Google Gemini 2.0 Flash): Business Analyst 역할
- **Judge Agent** (Google Gemini 2.0 Flash): QA/PM 역할
- **Writer Agent** (Rule-based Engine): Technical Writer 역할

### 2. Dynamic Tech Stack Generation

프로젝트 특성을 분석하여 최적의 기술 스택을 자동 선택:

- 이커머스 대규모: Spring Boot + MSA + Kafka
- 실시간 채팅: Node.js + Socket.io + MongoDB
- 소규모 웹앱: FastAPI + PostgreSQL + React

### 3. Automated Test Scenario Creation

8가지 프로젝트 패턴 인식 및 Gherkin 포맷 테스트 시나리오 자동 생성:
- E-commerce, Social Network, Booking System, Real-time Chat
- Content Management, IoT Platform, Finance, Education

### 4. Session-based Workflow

UUID 기반 세션 관리로 다중 프로젝트 동시 작업 지원

---

## 🤖 How It Works

### 핵심 아이디어: **3개의 AI 에이전트가 협업**

```
User Input ("온라인 쇼핑몰을 만들고 싶습니다")
    │
    ▼
┌──────────────────────────────────────────┐
│  Consultant Agent (Google Gemini)        │
│  - 컨텍스트 기반 질문 생성                 │
│  - 우선순위 기반 정보 수집                 │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Judge Agent (Google Gemini)             │
│  - 수집된 정보의 완전성 평가               │
│  - 필수 항목 검증 (인증, 배포, 규모 등)    │
│  - 최대 10회 반복으로 과도한 질문 방지     │
└──────────┬───────────────────────────────┘
           │
           ▼ (is_complete = True)
┌──────────────────────────────────────────┐
│  Writer Agent (Rule-based)               │
│  - 동적 기술 스택 선택                     │
│  - Gherkin 테스트 시나리오 생성           │
│  - 구조화된 SRS 문서 생성                 │
└──────────────────────────────────────────┘
           │
           ▼
    📄 Final SRS Document
    (JSON, Markdown)
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

### Prerequisites

- Python 3.11 or higher
- Google Gemini API Key ([Get Free API Key](https://makersuite.google.com/app/apikey))
- Git

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/SpecPilot.git
cd SpecPilot
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and add your Google API key
# GOOGLE_API_KEY=your-google-api-key-here
```

**Getting Google Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it into `.env` file

#### 5. Run the Application

```bash
streamlit run frontend/app.py
```

The application will open in your browser at `http://localhost:8501`

### 🎬 Demo Walkthrough

**Step 1: Initial Input**
```
User: "음식 배달 앱을 만들고 싶습니다"
```

**Step 2: AI Interview**
```
AI: "예상 사용자 수는 얼마나 되나요?"
User: "중소규모, 일 1000명 정도"

AI: "결제 시스템이 필요한가요?"
User: "네, 신용카드와 간편결제 지원 필요"

AI: "배달 추적 기능이 필요한가요?"
User: "네, 실시간 GPS 추적 필요합니다"
```

**Step 3: SRS Generated**
```
✅ SRS Document Created!

📋 Functional Requirements:
  - FR-001: 주문 관리 시스템 (High Priority)
  - FR-002: 실시간 결제 처리 (High Priority)
  - FR-003: GPS 기반 배달 추적 (High Priority)

🛠 Tech Stack:
  - Backend: Node.js, Express.js
  - Frontend: React Native
  - Database: PostgreSQL, Redis
  - Infrastructure: AWS, Docker

🧪 Test Scenarios:
  Feature: 주문 생성
    Given: 사용자가 메뉴를 선택했다
    When: 주문하기 버튼을 클릭한다
    Then: 주문이 생성되고 확인 메시지가 표시된다
```

---

## 💼 Usage Examples

### Example 1: E-commerce Platform

**User Input:**
```
"온라인 의류 쇼핑몰을 만들고 싶습니다. 상품 검색, 장바구니, 결제 기능이 필요합니다."
```

**Generated SRS Highlights:**
- Functional Requirements: 상품 관리, 검색 엔진, 장바구니, 주문/결제, 사용자 리뷰
- Tech Stack: Spring Boot (Backend), React (Frontend), PostgreSQL (DB), Elasticsearch (Search)
- Test Scenarios: 상품 검색, 장바구니 추가/삭제, 결제 프로세스

### Example 2: Real-time Chat Application

**User Input:**
```
"실시간 채팅 앱을 만들고 싶습니다. 1:1 채팅과 그룹 채팅, 파일 공유 기능이 필요합니다."
```

**Generated SRS Highlights:**
- Functional Requirements: 실시간 메시징, 그룹 채팅방, 파일 업로드/다운로드, 읽음 표시
- Tech Stack: Node.js + Socket.io (Backend), React Native (Mobile), MongoDB (DB), Redis (Cache)
- Test Scenarios: 메시지 전송/수신, 그룹 채팅방 생성, 파일 공유

### Example 3: Internal Corporate System

**User Input:**
```
"사내 인트라넷 시스템이 필요합니다. 직원 200명이 사용하며, 전자결재, 조직도, 공지사항 기능이 있어야 합니다."
```

**Generated SRS Highlights:**
- Functional Requirements: 전자결재 워크플로우, 조직도 관리, 공지사항, 회의실 예약
- Tech Stack: FastAPI (Backend), Vue.js (Frontend), PostgreSQL (DB)
- Test Scenarios: 결재 상신/승인, 조직도 조회, 공지사항 등록

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

## ⚙️ Configuration

### Environment Variables

Edit the `.env` file to customize the application:

```bash
# Google Gemini API Configuration
GOOGLE_API_KEY=your-google-api-key-here
MODEL_NAME=gemini-1.5-pro
TEMPERATURE=0.7

# Application Configuration
MAX_ITERATIONS=10              # Maximum interview iterations
SESSION_TIMEOUT=3600          # Session timeout in seconds

# Development
DEBUG=True
LOG_LEVEL=INFO
```

### Advanced Configuration

**Model Settings:**
- `MODEL_NAME`: Choose from `gemini-1.5-pro`, `gemini-1.5-flash`
- `TEMPERATURE`: Controls randomness (0.0-1.0). Lower = more deterministic

**Workflow Settings:**
- `MAX_ITERATIONS`: Maximum number of question-answer rounds
- Default: 10 (prevents excessive questioning)

---

## 🛠 Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Install testing tools
pip install pytest pytest-cov pytest-asyncio httpx

# Install code quality tools
pip install black ruff mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/backend/test_agents.py
```

### Code Quality

```bash
# Format code
black backend/ frontend/ tests/

# Lint code
ruff check backend/ frontend/ tests/

# Type checking
mypy backend/
```

### Project Structure Details

```
backend/
├── domain/              # Business logic layer
│   ├── agents/         # AI agents (Consultant, Judge, Writer)
│   ├── models/         # Domain models (State, SRS)
│   └── repositories/   # Repository interfaces
├── application/        # Application layer
│   └── use_cases/     # Business use cases
├── infrastructure/     # Infrastructure layer
│   ├── llm/           # LLM client (Gemini)
│   ├── graph/         # Workflow orchestration
│   ├── persistence/   # Data storage
│   └── prompts/       # Agent prompts
└── presentation/       # Presentation layer
    └── api/           # API routes and schemas

frontend/
├── app.py             # Streamlit UI
├── services/          # API client
└── utils/            # UI utilities

tests/
├── backend/          # Backend unit tests
└── frontend/         # Frontend tests
```

---

## 🧪 Testing

### Unit Tests

Each component has comprehensive unit tests:

```bash
# Test agents
pytest tests/backend/test_agents.py

# Test models
pytest tests/backend/test_models.py

# Test use cases
pytest tests/backend/test_use_cases.py
```

### Integration Tests

```bash
# Test full workflow
pytest tests/backend/test_infrastructure.py
```

---

## 🔮 로드맵

### 버전 2.0 (2025년 2분기)

- [ ] **데이터베이스 영속성**: PostgreSQL/Redis 기반 세션 저장
- [ ] **히스토리 관리**: 이전 SRS 문서 조회 및 재사용
- [ ] **다국어 지원**: 영어, 한국어, 일본어
- [ ] **내보내기 형식**: PDF, DOCX, HTML

### 버전 3.0 (2025년 3분기)

- [ ] **Jira 연동**: SRS에서 Epic/Story 자동 생성
- [ ] **코드 생성**: SRS 기반 프로젝트 스캐폴딩
- [ ] **팀 협업**: 다중 사용자 SRS 편집
- [ ] **API 게이트웨이**: 서드파티 통합을 위한 RESTful API

### 장기 비전

- [ ] **커스텀 에이전트 학습**: 회사별 템플릿 기반 에이전트 훈련
- [ ] **버전 관리**: SRS 변경 이력 추적
- [ ] **분석 대시보드**: 프로젝트 메트릭 및 인사이트
- [ ] **모바일 앱**: iOS/Android 네이티브 애플리케이션

---

## 👥 개발자

**RANG** - *프로젝트 생성* - [GitHub 프로필](https://github.com/rangrang-53)

---

## 🙏 감사의 말

- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM 제공
- [Streamlit](https://streamlit.io/) - 웹 UI 프레임워크
- [Pydantic](https://docs.pydantic.dev/) - 데이터 검증

---

## 📧 문의 및 지원

- **이메일**: jr0503@naver.com
- **이슈**: [GitHub Issues](https://github.com/rangrang-53/SpecPilot/issues)
- **토론**: [GitHub Discussions](https://github.com/rangrang-53/SpecPilot/discussions)

---

## 📊 프로젝트 상태

**현재 버전**: v1.0.0
**상태**: 활발히 개발 중
**최종 업데이트**: 2025년 1월

---

<div align="center">

**SpecPilot** - "모호한 아이디어를 명확한 명세서로" ✈️

Made with ❤️ by RANG

[⬆ 맨 위로](#️-specpilot-ai-powered-srs-generator)

</div>
