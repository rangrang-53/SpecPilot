# SpecPilot 개발 태스크 정의

| Task ID | Title | Description | Status | Dependencies | Priority | Details | Test Strategy |
|---------|-------|-------------|--------|--------------|----------|---------|---------------|
| **T-01** | **도메인 모델 구현** | Pydantic 기반 핵심 데이터 모델 정의 (RequirementState, Message, SRSDocument 등) | ✅ Completed | None | High | - Message, RequirementState 모델<br>- ConsultantResponse, JudgeResponse<br>- FunctionalRequirement, TechStackRecommendation<br>- GherkinScenario, SRSDocument | Unit tests for all models with validation scenarios |
| **T-02** | **인프라스트럭처 레이어** | OpenAI Client, Checkpointer, StateStore 더미 구현 | ✅ Completed | T-01 | High | - DummyOpenAIClient<br>- DummyCheckpointer (세션 저장)<br>- DummyStateStore (키-값 저장소)<br>- Prompt 템플릿 (consultant, judge, writer) | Unit tests for infrastructure components |
| **T-03** | **에이전트 구현** | Consultant, Judge, Writer 에이전트 더미 구현 | ✅ Completed | T-01, T-02 | High | - consultant_agent: 질문 생성<br>- judge_agent: 완전성 평가<br>- writer_agent: SRS 문서 생성 | Unit tests for each agent with various input scenarios |
| **T-04** | **워크플로우 오케스트레이션** | LangGraph 기반 multi-agent workflow 구현 | ✅ Completed | T-03 | High | - DummyWorkflow: 에이전트 체이닝<br>- DummyExecutor: 세션 관리<br>- DummySessionRepository: 영속성 | Integration tests for workflow execution paths |
| **T-05** | **유틸리티 서비스** | 정보 추출, SRS 포매팅, 품질 메트릭 계산 유틸리티 | ✅ Completed | T-01 | Medium | - InfoExtractor: 사용자 입력에서 정보 추출<br>- SRSFormatter: SRS 문서 포맷팅 (JSON → Markdown)<br>- QualityMetrics: 요구사항 품질 점수 계산 | Unit tests with mock data |
| **T-06** | **Application 레이어** | Use Case 및 비즈니스 로직 구현 | ✅ Completed | T-04, T-05 | Medium | - StartSessionUseCase<br>- ContinueSessionUseCase<br>- GetSRSUseCase<br>- ResetSessionUseCase | Use case tests with mocked dependencies |
| **T-07** | **FastAPI 백엔드 API** | RESTful API 엔드포인트 구현 | ✅ Completed | T-06 | High | - POST /api/session/start<br>- POST /api/session/continue<br>- GET /api/srs/{session_id}<br>- GET /api/session/{session_id}/status<br>- POST /api/session/{session_id}/reset<br>- GET /api/session/{session_id}/collected-info | API integration tests with TestClient |
| **T-08** | **Streamlit 프론트엔드** | 대화형 UI 구현 | ✅ Completed | T-07 | High | - 채팅 인터페이스<br>- 세션 관리 UI<br>- SRS 문서 미리보기<br>- 다운로드 기능<br>- 대화 히스토리 표시 | Manual UI testing + E2E tests |
| **T-09** | **설정 및 환경 관리** | 환경 변수, 설정 파일, 로깅 구현 | ✅ Completed | None | Medium | - Pydantic Settings 기반 config<br>- 환경별 설정 파일 (.env)<br>- API 키 관리 | Configuration validation tests |
| **T-10** | **통합 테스트 및 배포** | E2E 테스트, Docker 컨테이너화, CI/CD 파이프라인 | ✅ Completed | T-08, T-09 | High | - Dockerfile (backend, frontend)<br>- docker-compose.yml<br>- README.md<br>- 배포 문서 | E2E tests covering full user journeys |

---

## 태스크 현황 요약

```
✅ Completed Tasks: 10/10 (100%)
⏳ Pending Tasks: 0/10 (0%)

🎉 전체 개발 완료!
✅ 76개 백엔드 테스트 모두 통과
```

---

## 태스크 의존성 그래프

```
T-01 (Domain Models) ✅
  ├─→ T-02 (Infrastructure) ✅
  │    └─→ T-03 (Agents) ✅
  │         └─→ T-04 (Workflow) ✅
  │              └─→ T-06 (Application Layer)
  │                   └─→ T-07 (FastAPI Backend)
  │                        └─→ T-08 (Streamlit Frontend)
  │                             └─→ T-10 (Integration & Deployment)
  ├─→ T-05 (Utils)
  │    └─→ T-06 (Application Layer)
  └─→ T-09 (Configuration)
       └─→ T-10 (Integration & Deployment)
```

---

## 우선순위별 태스크

**High Priority (즉시 진행):**
- T-05: 유틸리티 서비스
- T-07: FastAPI 백엔드 API
- T-08: Streamlit 프론트엔드
- T-10: 통합 테스트 및 배포

**Medium Priority (순차 진행):**
- T-06: Application 레이어
- T-09: 설정 및 환경 관리

---

## 진행 상황

### Phase 1-4 완료 (T-01 ~ T-04) ✅

**완료된 구현:**
- ✅ 47개 테스트 통과
- ✅ 도메인 모델 (13 tests)
- ✅ 인프라스트럭처 (9 tests)
- ✅ 에이전트 (8 tests)
- ✅ 워크플로우 (17 tests)

**생성된 파일:**
- `backend/domain/models/` - 모든 도메인 모델
- `backend/domain/agents/` - 3개 에이전트
- `backend/infrastructure/llm/` - OpenAI 클라이언트
- `backend/infrastructure/persistence/` - 체크포인터, 스토어
- `backend/infrastructure/prompts/` - 프롬프트 템플릿
- `backend/infrastructure/graph/` - 워크플로우, 실행기, 저장소

### 🎊 전체 개발 완료!

**구현 완료 항목:**
- ✅ 도메인 모델 (13 tests)
- ✅ 인프라스트럭처 (9 tests)
- ✅ 에이전트 (8 tests)
- ✅ 워크플로우 (17 tests)
- ✅ 유틸리티 (11 tests)
- ✅ Use Cases (12 tests)
- ✅ FastAPI API (6 tests)
- ✅ Streamlit Frontend
- ✅ 설정 관리
- ✅ Docker & README

**테스트 결과:** 76/76 통과 ✅

**실행 방법:**
```bash
# 백엔드 실행
uvicorn backend.presentation.main:app --reload

# 프론트엔드 실행
streamlit run frontend/app.py

# Docker로 실행
docker-compose up
```
