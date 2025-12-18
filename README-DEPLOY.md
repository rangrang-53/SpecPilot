# SpecPilot Streamlit Cloud 배포 가이드

## 단일 앱 배포 (프론트엔드 + 백엔드 통합)

SpecPilot은 프론트엔드와 백엔드가 **하나의 Streamlit 앱**으로 통합되어 있습니다.
별도의 백엔드 서버 없이 Streamlit Cloud에 바로 배포할 수 있습니다!

## 배포 단계

### 1. Streamlit Cloud 배포 설정

Streamlit Cloud에 배포할 때 다음 설정을 사용하세요:

```
Main file path: frontend/app.py
Python version: 3.11 (또는 3.10)
```

### 2. 환경 변수 설정 (선택사항)

현재는 더미 데이터로 작동하므로 특별한 환경 변수가 필요하지 않습니다.

향후 실제 LLM API를 사용할 경우, Streamlit Cloud 대시보드의 **Settings > Secrets**에서:

```toml
# Google Gemini API (향후 사용 시)
GOOGLE_API_KEY = "your-api-key-here"
```

### 3. 로컬 테스트

배포 전 로컬에서 테스트:

```bash
# 프로젝트 루트에서 실행
streamlit run frontend/app.py
```

브라우저에서 `http://localhost:8501` 접속

## 아키텍처 설명

### 통합 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit App                             │
│                  (frontend/app.py)                           │
│                                                              │
│  ┌────────────────┐         ┌──────────────────┐           │
│  │  Streamlit UI  │ ──────▶ │   APIClient      │           │
│  │  (3 screens)   │         │  (Direct calls)  │           │
│  └────────────────┘         └────────┬─────────┘           │
│                                      │                      │
│                                      ▼                      │
│                          ┌───────────────────┐             │
│                          │  Backend Use Cases│             │
│                          │  - StartSession   │             │
│                          │  - ContinueSession│             │
│                          │  - GetSRS         │             │
│                          └─────────┬─────────┘             │
│                                    │                        │
│                                    ▼                        │
│                          ┌───────────────────┐             │
│                          │  Domain Agents    │             │
│                          │  - Consultant     │             │
│                          │  - Judge          │             │
│                          │  - Writer         │             │
│                          └───────────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 변경 사항

#### 1. API Client 변경 ([frontend/services/api_client.py](frontend/services/api_client.py))

**변경 전** (HTTP 기반):
```python
import requests

class APIClient:
    def start_session(self, initial_input):
        response = requests.post(f"{self.base_url}/api/session/start", ...)
        return response.json()
```

**변경 후** (직접 호출):
```python
from backend.application.use_cases.start_session_use_case import StartSessionUseCase

class APIClient:
    def __init__(self):
        self.start_session_uc = StartSessionUseCase()

    def start_session(self, initial_input):
        return self.start_session_uc.execute(initial_input)
```

#### 2. 경로 설정 자동화

`api_client.py`에서 프로젝트 루트를 자동으로 `sys.path`에 추가:

```python
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
```

이를 통해 `backend` 모듈을 어디서든 import 가능합니다.

## 해결된 문제들

### ✅ ModuleNotFoundError 해결

**원래 에러:**
```
ModuleNotFoundError: No module named 'frontend.services.api_client'
```

**해결 방법:**
1. `frontend/app.py`의 import를 상대 경로로 변경:
   ```python
   from services.api_client import APIClient  # frontend. 제거
   from utils.srs_formatter import SRSFormatter  # backend. 제거
   ```

2. `backend/utils/srs_formatter.py`를 `frontend/utils/`로 복사
   - backend 의존성 제거

3. `api_client.py`에서 프로젝트 루트를 `sys.path`에 추가
   - backend 모듈을 직접 import 가능

### ✅ 백엔드 API 서버 불필요

**변경 전:**
- FastAPI 백엔드 서버 필요
- HTTP 통신 오버헤드
- 별도 배포 및 관리 필요

**변경 후:**
- 프론트엔드에서 백엔드 Use Case 직접 호출
- 단일 Streamlit 앱으로 배포
- 관리 포인트 단순화

## 배포 체크리스트

배포하기 전에 확인하세요:

- [ ] `requirements.txt`에 필요한 패키지가 모두 포함되어 있는지 확인
- [ ] `frontend/app.py`가 정상 작동하는지 로컬 테스트
- [ ] GitHub 저장소에 코드 푸시
- [ ] Streamlit Cloud에서 앱 생성 (Main file: `frontend/app.py`)
- [ ] 배포 후 정상 작동 확인

## 필수 패키지

배포에 필요한 최소 패키지 ([requirements.txt](requirements.txt)):

```txt
# LangChain & LangGraph
langchain
langgraph
langchain-google-genai
google-generativeai

# Web Framework
streamlit

# Data Validation
pydantic
pydantic-settings

# Utilities
python-dotenv
```

## 문제 해결

### 1. Import 에러 발생 시

```python
ModuleNotFoundError: No module named 'backend'
```

**해결:** `frontend/services/api_client.py`에서 프로젝트 루트가 제대로 추가되었는지 확인

### 2. Streamlit Cloud 빌드 실패

- `requirements.txt`의 패키지 버전 충돌 확인
- Python 버전이 3.10 이상인지 확인

### 3. 세션 상태 초기화 문제

- 브라우저 새로고침으로 세션 리셋
- "새 세션 시작" 버튼 클릭

## 로컬 개발 워크플로우

```bash
# 1. 저장소 클론
git clone https://github.com/your-repo/SpecPilot.git
cd SpecPilot

# 2. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. Streamlit 실행
streamlit run frontend/app.py
```

## 참고 링크

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [SpecPilot GitHub Repository](https://github.com/your-repo/SpecPilot)

---

**이제 Streamlit Cloud에 배포할 준비가 완료되었습니다!** 🚀
