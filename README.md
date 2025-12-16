# ✈️ SpecPilot: AI-based SRS Automation Agent

> **"From Vague Ideas to Concrete Specs."**

SpecPilot은 모호한 아이디어를 명확한 기술 명세서(SRS)로 전환하는 AI 기반 요구사항 자동화 에이전트입니다.

## 🚀 주요 기능

- **AI 주도형 인터뷰**: Business Analyst처럼 스마트한 질문 생성
- **품질 검증**: Judge 에이전트를 통한 완전성 평가
- **자동 SRS 생성**: 개발 가능한 수준의 명세서 자동 작성
- **기술 스택 추천**: Cloud-Native 기술 스택 자동 제안
- **Gherkin 테스트 시나리오**: TDD를 위한 Given-When-Then 시나리오 생성

## 🏗 시스템 아키텍처

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
┌────────▼────────┐
│   FastAPI       │
│   Backend       │
└────────┬────────┘
         │
┌────────▼────────┐
│  Multi-Agent    │
│  Workflow       │
├─────────────────┤
│ • Consultant    │
│ • Judge         │
│ • Writer        │
└─────────────────┘
```

## 📋 기술 스택

- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Frontend**: Streamlit
- **AI**: Google Gemini 3 Pro (더미 구현)
- **Orchestration**: LangGraph, LangChain
- **Testing**: Pytest

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
│   ├── domain/          # 도메인 모델 및 에이전트
│   ├── application/     # Use Cases
│   ├── infrastructure/  # 외부 서비스, Workflow
│   ├── presentation/    # FastAPI 라우트
│   └── utils/           # 유틸리티
├── frontend/
│   ├── app.py          # Streamlit 메인 앱
│   └── services/       # API Client
├── tests/
│   └── backend/        # 백엔드 테스트
├── config/
│   └── settings.py     # 애플리케이션 설정
├── docs/               # 문서
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## 📊 개발 진행 상황

| Task ID | Title | Status |
|---------|-------|--------|
| T-01 | 도메인 모델 구현 | ✅ Completed |
| T-02 | 인프라스트럭처 레이어 | ✅ Completed |
| T-03 | 에이전트 구현 | ✅ Completed |
| T-04 | 워크플로우 오케스트레이션 | ✅ Completed |
| T-05 | 유틸리티 서비스 | ✅ Completed |
| T-06 | Application 레이어 | ✅ Completed |
| T-07 | FastAPI 백엔드 API | ✅ Completed |
| T-08 | Streamlit 프론트엔드 | ✅ Completed |
| T-09 | 설정 및 환경 관리 | ✅ Completed |
| T-10 | 통합 테스트 및 배포 | ✅ Completed |

## 🎯 사용 방법

1. **프로젝트 시작**: 초기 아이디어 입력 (예: "온라인 쇼핑몰을 만들고 싶습니다")
2. **대화형 인터뷰**: AI가 생성한 질문에 답변
3. **완전성 검증**: Judge 에이전트가 정보 충분성 평가
4. **SRS 생성**: Writer 에이전트가 최종 명세서 작성
5. **문서 다운로드**: JSON 형식으로 SRS 다운로드

## 🔄 API 엔드포인트

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/session/start` | 새 세션 시작 |
| POST | `/api/session/continue` | 세션 계속 |
| GET | `/api/session/{id}/status` | 세션 상태 조회 |
| GET | `/api/srs/{id}` | SRS 문서 조회 |
| POST | `/api/session/{id}/reset` | 세션 리셋 |
| GET | `/api/session/{id}/collected-info` | 수집된 정보 조회 |

## 🤝 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---