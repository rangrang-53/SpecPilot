# ✈️ SpecPilot: AI-based SRS Automation Agent

> **"From Vague Ideas to Concrete Specs."**

SpecPilot은 모호한 아이디어를 명확한 기술 명세서(SRS)로 전환하는 AI 기반 요구사항 자동화 에이전트입니다.

## 🎯 Why SpecPilot?

초기 기획 단계에서 발생하는 문제들:
- **불완전한 요구사항**: 고객이나 PM이 제공하는 초기 요구사항은 대부분 불완전하고 모호함
- **반복적인 커뮤니케이션 비용**: 요구사항을 명확히 하기 위한 수십 번의 이메일과 미팅
- **문서화 부담**: SRS 작성에 소요되는 시간과 노력
- **기술 스택 결정 어려움**: 프로젝트 특성에 맞는 기술 선택의 불확실성

SpecPilot은 이러한 문제를 **Multi-Agent Workflow**로 해결합니다.

## 🚀 핵심 기능

### 1. AI 주도형 인터뷰 (Consultant Agent)
- Business Analyst처럼 맥락을 이해하고 스마트한 질문 생성
- 프로젝트 규모, 배포 환경, 인증 방식, 결제 시스템 등 체계적으로 정보 수집
- 사용자 답변에 따라 동적으로 후속 질문 생성

### 2. 완전성 검증 (Judge Agent)
- 수집된 정보의 충분성을 자동 평가
- 최대 5회 iteration으로 정보 품질 보장
- 부족한 정보가 있을 경우 Consultant에게 추가 질문 요청

### 3. 동적 SRS 생성 (Writer Agent)
- **컨텍스트 기반 기술 스택 추천**:
  - 프로젝트 규모와 특성 분석 (이커머스, 실시간, 모바일, 관리자 등)
  - MSA vs Monolith, Spring Boot vs Node.js vs FastAPI 자동 선택
  - Cloud 인프라 최적화 (Kubernetes, ECS, Cloud Run, Heroku)
- **동적 테스트 시나리오 생성**:
  - 프로젝트 유형별 맞춤형 Gherkin 시나리오 (이커머스, 소셜, 예약, 실시간 등)
  - 8가지 프로젝트 패턴 인식 및 시나리오 자동 생성
- **개발 가능한 수준의 명세서**: 기능 요구사항, 비기능 요구사항, 기술 근거 포함

### 4. Streamlit 기반 UX
- 와이어프레임 기반 직관적 인터페이스
- 실시간 진행 상황 트래킹 (Iteration Counter)
- Markdown/JSON 다운로드 및 클립보드 복사

## 🏗 시스템 아키텍처

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend                          │
│  - 와이어프레임 기반 UI/UX                                        │
│  - Real-time Progress Tracking                                   │
│  - Form-based Input (Enter key support)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP REST API
┌────────────────────────────▼────────────────────────────────────┐
│                      FastAPI Backend                             │
│  - Session Management (In-Memory State)                          │
│  - RESTful API (POST /start, POST /continue, GET /srs)          │
│  - Pydantic Models (Type-safe Data Validation)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              LangGraph Multi-Agent Workflow                      │
│                                                                  │
│  ┌─────────────┐      ┌──────────┐      ┌────────────┐         │
│  │ Consultant  │─────▶│  Judge   │─────▶│   Writer   │         │
│  │   Agent     │      │  Agent   │      │   Agent    │         │
│  └─────────────┘      └──────────┘      └────────────┘         │
│       │                    │                    │               │
│    질문 생성          완전성 평가          SRS 문서 생성         │
│  (동적 인터뷰)      (Iteration 판단)    (동적 기술스택/시나리오)  │
│                                                                  │
│  State Management: RequirementState (Pydantic)                  │
│  - user_input, collected_info, questions, is_complete           │
│  - iteration_count (max 5), final_srs                           │
└──────────────────────────────────────────────────────────────────┘
```

### Agent Workflow Details

```
User Input
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ 1. Consultant Agent                                          │
│    - 사용자 입력 분석 (키워드 추출: 규모, 유형, 기술)          │
│    - 컨텍스트 기반 질문 생성 (규모, 배포, 인증, 결제 등)       │
│    - collected_info 업데이트                                  │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. Judge Agent                                               │
│    - 정보 충분성 평가 (규모, 배포환경, 인증, 결제 확인)        │
│    - is_complete = True/False 판단                           │
│    - iteration_count 증가 (max 5)                            │
│    - 부족 시: Consultant로 재라우팅                           │
│    - 충분 시: Writer로 이동                                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. Writer Agent                                              │
│    - _generate_tech_stack() 호출                             │
│      * 프로젝트 특성 분석 (이커머스, 실시간, 모바일 등)        │
│      * Backend: Spring Boot(MSA) / Node.js / FastAPI         │
│      * Frontend: React Native / Next.js / React+Vite         │
│      * DevOps: K8s / ECS / Cloud Run / Heroku                │
│    - _generate_test_scenarios() 호출                         │
│      * 8가지 패턴 인식 (ecommerce, social, booking, etc)     │
│      * Gherkin Given-When-Then 시나리오 자동 생성             │
│    - SRSDocument 생성 (JSON)                                 │
└──────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Multi-Agent Pattern 선택 이유**:
   - 각 에이전트의 역할 분리 (Consultant: 질문, Judge: 검증, Writer: 생성)
   - LangGraph의 상태 기반 워크플로우로 반복 가능한 대화 흐름 구현
   - 에이전트 간 명확한 인터페이스 (RequirementState)

2. **동적 기술 스택 생성**:
   - 하드코딩된 기술 스택 대신 **키워드 기반 규칙 엔진** 사용
   - 프로젝트 특성(규모, 유형, 배포환경)에 따라 최적 기술 자동 선택
   - 기술 선택 근거(rationale)를 명시하여 의사결정 투명성 확보

3. **Session-based Stateful Architecture**:
   - In-Memory 세션 관리 (UUID 기반)
   - 각 세션마다 독립적인 RequirementState 유지
   - 5회 iteration limit으로 무한 루프 방지

4. **Wireframe-driven UI/UX**:
   - SVG 와이어프레임 기반 디자인 시스템
   - 색상 테마 일관성 (Blue: Primary, Green: AI/Success, Yellow: Iteration)

## 📋 기술 스택

### Core Stack
- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Frontend**: Streamlit (Form-based UX, Custom CSS)
- **AI/LLM**: Google Gemini API (현재 더미 구현)
- **Workflow Orchestration**: LangGraph (State Machine), LangChain
- **Testing**: Pytest (76/76 tests passing)
- **Type Safety**: Pydantic Models, Python Type Hints

### Architecture Patterns
- **Clean Architecture**: Domain → Application → Infrastructure → Presentation
- **Multi-Agent System**: Consultant, Judge, Writer 에이전트 분리
- **State Machine**: LangGraph로 에이전트 간 전이 관리
- **Session Management**: In-Memory UUID 기반 세션

## 🛠 설치 및 실행

### 1. 로컬 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-repo/SpecPilot.git
cd SpecPilot

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 GOOGLE_API_KEY 설정
```

### 2. 백엔드 실행

```bash
# FastAPI 서버 실행
uvicorn backend.presentation.main:app --reload --host 0.0.0.0 --port 8000
```

API 문서: http://localhost:8000/docs

### 3. 프론트엔드 실행

```bash
# Streamlit 앱 실행
streamlit run frontend/app.py
```

앱 접속: http://localhost:8501

### 4. Streamlit Community Cloud에 배포

1. GitHub 저장소에 코드 푸시
2. [Streamlit Community Cloud](https://streamlit.io/cloud) 접속
3. "New app" 클릭
4. 저장소 선택 및 메인 파일 경로 입력: `frontend/app.py`
5. Advanced settings에서 환경 변수 추가:
   - `GOOGLE_API_KEY`: 본인의 Gemini API 키
   - `BACKEND_URL`: 백엔드 API URL (또는 로컬 테스트)
6. Deploy 클릭

**참고**: Streamlit 배포 시 백엔드와 프론트엔드가 통합된 구조로 작동하므로, `frontend/app.py`만 배포하면 됩니다.

### 5. Docker로 실행 (선택사항)

Docker 파일은 `docker/` 폴더에 보관되어 있습니다.
자세한 사용법은 [docker/README.md](docker/README.md)를 참고하세요.

```bash
# Docker 파일 복사
cp docker/Dockerfile.backend docker/Dockerfile.frontend docker/docker-compose.yml ./

# Docker Compose로 전체 스택 실행
docker-compose up --build
```

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest

# 백엔드 테스트만 실행
pytest tests/backend/ -v

# 커버리지와 함께 실행
pytest --cov=backend --cov-report=html
```

**현재 테스트 상태**: ✅ 76/76 통과

## 📁 프로젝트 구조

```
SpecPilot/
├── backend/
│   ├── domain/                    # Domain Layer (핵심 비즈니스 로직)
│   │   ├── agents/
│   │   │   ├── consultant_agent.py   # 질문 생성 에이전트
│   │   │   ├── judge_agent.py        # 완전성 검증 에이전트
│   │   │   └── writer_agent.py       # SRS 생성 + 동적 기술스택/테스트 시나리오
│   │   └── models/
│   │       ├── state.py              # RequirementState (Pydantic)
│   │       └── srs.py                # SRSDocument, FunctionalRequirement 등
│   │
│   ├── application/              # Application Layer (Use Cases)
│   │   └── use_cases.py          # StartSessionUseCase, ContinueSessionUseCase
│   │
│   ├── infrastructure/           # Infrastructure Layer
│   │   ├── workflow/
│   │   │   └── requirement_workflow.py  # LangGraph 워크플로우 정의
│   │   ├── prompts/
│   │   │   ├── consultant_prompt.py     # Consultant 프롬프트
│   │   │   ├── judge_prompt.py          # Judge 프롬프트
│   │   │   └── writer_prompt.py         # Writer 프롬프트
│   │   └── session_store.py      # In-Memory 세션 저장소
│   │
│   ├── presentation/             # Presentation Layer (API)
│   │   └── main.py               # FastAPI 라우트 정의
│   │
│   └── utils/
│       └── srs_formatter.py      # JSON → Markdown 변환
│
├── frontend/
│   ├── app.py                    # Streamlit 메인 앱 (3 screens)
│   │                             # - show_initial_screen()
│   │                             # - show_qa_screen()
│   │                             # - show_completion_screen()
│   └── services/
│       └── api_client.py         # Backend API 호출 클라이언트
│
├── tests/
│   └── backend/                  # 76 unit tests
│       ├── domain/
│       ├── application/
│       └── infrastructure/
│
├── docs/
│   └── wireframes/               # SVG 와이어프레임
│       ├── 01-initial-screen.svg
│       ├── 02-qa-screen.svg
│       ├── 03-completion-screen.svg
│       └── 04-sidebar.svg
│
├── config/
│   └── settings.py               # 환경 변수 관리
│
├── requirements.txt
├── docker-compose.yml
└── README.md
```

### Key Files Explained

- **[writer_agent.py](backend/domain/agents/writer_agent.py)**:
  - `_generate_tech_stack()`: 프로젝트 특성 기반 기술 스택 자동 선택 (390줄)
  - `_generate_test_scenarios()`: 8가지 패턴 인식 및 Gherkin 시나리오 생성 (230줄)

- **[requirement_workflow.py](backend/infrastructure/workflow/requirement_workflow.py)**:
  - LangGraph StateGraph 정의
  - 에이전트 간 라우팅 로직 (`route_after_judge`)

- **[app.py](frontend/app.py)**:
  - 3개 화면 관리 (Initial → QA → Completion)
  - Form-based input (Enter key support)
  - Iteration counter, Progress tracking

## 📊 개발 진행 상황 & 최근 업데이트

### Completed Features
| Task ID | Title | Status | Description |
|---------|-------|--------|-------------|
| T-01 | 도메인 모델 구현 | ✅ | RequirementState, SRSDocument Pydantic 모델 |
| T-02 | 인프라스트럭처 레이어 | ✅ | LangGraph Workflow, Session Store |
| T-03 | 에이전트 구현 | ✅ | Consultant, Judge, Writer 에이전트 |
| T-04 | 워크플로우 오케스트레이션 | ✅ | LangGraph StateGraph, 라우팅 로직 |
| T-05 | 유틸리티 서비스 | ✅ | SRS Formatter (JSON → Markdown) |
| T-06 | Application 레이어 | ✅ | Use Cases (Start/Continue Session) |
| T-07 | FastAPI 백엔드 API | ✅ | RESTful API 엔드포인트 |
| T-08 | Streamlit 프론트엔드 | ✅ | 3-screen UX, Form-based input |
| T-09 | 설정 및 환경 관리 | ✅ | Environment variables, Settings |
| T-10 | 통합 테스트 및 배포 | ✅ | 76 unit tests passing |
| **T-11** | **동적 기술 스택 생성** | ✅ | **키워드 기반 규칙 엔진으로 기술 자동 선택** |
| **T-12** | **동적 테스트 시나리오 생성** | ✅ | **8가지 패턴 인식 및 Gherkin 생성** |
| **T-13** | **UI/UX 개선** | ✅ | **Enter key 지원, 프리뷰 제거** |

### Recent Updates (2025-12-17)

#### 1. Dynamic Tech Stack Generation (`writer_agent.py`)
```python
def _generate_tech_stack(user_input, collected_info, scale, deployment, payment):
    # 프로젝트 특성 자동 분석
    is_large_scale = "대규모" in scale or "트래픽" in scale
    is_ecommerce = any(kw in user_input for kw in ["쇼핑", "결제", "주문"])
    is_realtime = any(kw in user_input for kw in ["실시간", "채팅"])

    # 백엔드 기술 자동 선택
    if is_large_scale or is_ecommerce:
        backend = ["Spring Boot", "Microservices", "Kafka"]
    elif is_realtime:
        backend = ["Node.js", "Socket.io", "MongoDB"]
    else:
        backend = ["FastAPI", "PostgreSQL"]
```

**Why**: 하드코딩된 기술 스택은 모든 프로젝트에 동일한 제안을 했음. 규모와 유형에 따라 적절한 기술을 자동 선택하도록 개선.

#### 2. Dynamic Test Scenario Generation (`writer_agent.py`)
```python
def _generate_test_scenarios(user_input, collected_info, auth_info, payment_info):
    # 8가지 프로젝트 패턴 인식
    is_ecommerce = "쇼핑" in user_input or "커머스" in user_input
    is_social = "소셜" in user_input or "커뮤니티" in user_input
    is_booking = "예약" in user_input
    is_realtime = "실시간" in user_input or "채팅" in user_input
    # ... 8 patterns total

    # 패턴별 맞춤형 시나리오 생성
    if is_ecommerce:
        scenarios.extend([
            GherkinScenario("상품 검색", ...),
            GherkinScenario("장바구니 관리", ...),
            GherkinScenario("결제 처리", ...)
        ])
```

**Why**: 템플릿 기반 시나리오는 프로젝트와 무관한 내용이 포함됨. 프로젝트 유형을 자동 인식하여 관련성 높은 테스트 시나리오 생성.

#### 3. UX Improvements (`frontend/app.py`)
- **Enter Key Support**: Form-based input으로 변경 (`st.form()`)
- **Preview Removal**: 완료 화면에서 문서 프리뷰 섹션 제거 (사용자 피드백 반영)
- **Color Consistency**: 전체 UI에서 파란색 테마 (#3b82f6) 일관성 유지

**Why**: 사용자 테스트 중 발견된 UX 이슈 해결 (입력 필드 지속성, 엔터키 미지원, 색상 불일치)

## 🎯 사용 방법

### User Flow
1. **프로젝트 시작**: 초기 아이디어 입력 (예: "음식 배달 서비스 앱을 개발하려고 합니다")
2. **AI 인터뷰**: Consultant 에이전트가 생성한 질문에 답변
   - "예상 사용자 규모는 어느 정도인가요?"
   - "어떤 클라우드 환경에 배포하실 계획인가요?"
   - "사용자 인증 방식은 무엇인가요?"
3. **자동 검증**: Judge 에이전트가 정보 충분성 평가 (최대 5회 iteration)
4. **SRS 생성**: Writer 에이전트가 최종 명세서 작성
   - 프로젝트 특성 분석 → 기술 스택 자동 선택
   - 프로젝트 유형 인식 → 테스트 시나리오 생성
5. **다운로드**: Markdown 또는 JSON 형식으로 다운로드

### Example Output

**Input**: "온라인 쇼핑몰을 만들고 싶습니다. 결제 기능이 필요합니다."

**Generated Tech Stack**:
- Backend: Spring Boot, Microservices, PostgreSQL, Redis, Kafka
- Frontend: Next.js, React, TypeScript, Tailwind CSS
- DevOps: AWS ECS, Docker, GitHub Actions
- Payment: PG 연동 API, 토스페이먼츠

**Generated Test Scenarios**:
- Feature: 상품 검색
  - Given: 사용자가 메인 페이지에 있다
  - When: 검색창에 상품명을 입력하고 검색 버튼을 클릭한다
  - Then: 검색 결과 페이지에 관련 상품 목록이 표시된다
- Feature: 장바구니 관리
- Feature: 결제 처리
- (총 8개 시나리오 생성)

## 🔄 API 엔드포인트

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/session/start` | 새 세션 시작 | `{"user_input": "..."}` | `{"session_id": "uuid", "questions": [...], "iteration_count": 0}` |
| POST | `/api/session/continue` | 세션 계속 | `{"session_id": "uuid", "user_answer": "..."}` | `{"is_complete": bool, "questions": [...], "iteration_count": int}` |
| GET | `/api/session/{id}/status` | 세션 상태 조회 | - | `{"is_complete": bool, "iteration_count": int}` |
| GET | `/api/srs/{id}` | SRS 문서 조회 | - | `{"final_srs": "JSON string"}` |
| POST | `/api/session/{id}/reset` | 세션 리셋 | - | `{"message": "Session reset"}` |
| GET | `/api/session/{id}/collected-info` | 수집된 정보 조회 | - | `{"collected_info": {...}}` |

### API Usage Example

```python
import requests

# 1. 세션 시작
response = requests.post("http://localhost:8000/api/session/start", json={
    "user_input": "온라인 쇼핑몰을 만들고 싶습니다"
})
session_id = response.json()["session_id"]
questions = response.json()["questions"]

# 2. 질문에 답변
response = requests.post("http://localhost:8000/api/session/continue", json={
    "session_id": session_id,
    "user_answer": "중소규모이며, 사용자는 약 1000명 정도입니다"
})
is_complete = response.json()["is_complete"]

# 3. SRS 문서 조회 (완료 후)
response = requests.get(f"http://localhost:8000/api/srs/{session_id}")
srs_json = response.json()["final_srs"]
```

## 🔮 향후 개선 계획

### Immediate (v2.0)
- [ ] **LLM 통합**: Google Gemini API 실제 연동 (현재 더미 구현)
- [ ] **데이터베이스**: PostgreSQL/Redis로 세션 영구 저장 (현재 In-Memory)
- [ ] **인증**: JWT 기반 사용자 인증

### Medium-term (v3.0)
- [ ] **ML 기반 기술 스택 추천**: 키워드 규칙 → 머신러닝 모델로 개선
- [ ] **히스토리 관리**: 이전 프로젝트 SRS 히스토리 조회 및 재사용
- [ ] **Export 확장**: PDF, DOCX 형식 지원

### Long-term (v4.0)
- [ ] **Jira/Notion 통합**: SRS → Jira Epic/Story 자동 변환
- [ ] **코드 생성**: SRS → 초기 프로젝트 스캐폴딩 자동화
- [ ] **협업 기능**: 팀 단위 SRS 공동 작성 및 리뷰

## 🤝 기여 가이드

### Code Contributions
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow Clean Architecture principles (Domain → Application → Infrastructure → Presentation)
4. Write unit tests (maintain 76/76 passing)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Coding Standards
- **Type Hints**: 모든 함수에 타입 힌트 추가
- **Pydantic Models**: 데이터 검증을 위해 Pydantic 사용
- **Docstrings**: Google 스타일 docstring 작성
- **Testing**: 새 기능은 반드시 unit test 포함

---

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **RANG** - Initial work - SpecPilot v1.0
- Contributors: See [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

**SpecPilot** - "From Vague Ideas to Concrete Specs." ✈️