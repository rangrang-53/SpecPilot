# 🤖 Google Gemini LLM 통합 가이드

SpecPilot이 **실제 AI**를 사용하도록 업그레이드되었습니다! 🎉

## 변경 사항 요약

### ✅ 통합된 기능

| 컴포넌트 | 이전 (Dummy) | 현재 (LLM 통합) |
|----------|--------------|------------------|
| **Consultant Agent** | 하드코딩된 5개 질문 | **동적 질문 생성** - 사용자 입력 분석하여 맞춤형 질문 |
| **Judge Agent** | 단순 카운트 (5개 이상) | **지능형 평가** - 정보 완전성, 기술적 실현 가능성 평가 |
| **Writer Agent** | 규칙 기반 SRS 생성 | **유지** (이미 훌륭한 동적 생성 로직) |
| **LLM Client** | 더미 응답 반환 | **Google Gemini API** 실제 호출 |

## 파일 변경 사항

### 1. 새로 생성된 파일

#### [`backend/infrastructure/llm/gemini_client.py`](backend/infrastructure/llm/gemini_client.py)
```python
class GeminiClient:
    """실제 Gemini API 클라이언트"""
    - generate(): 텍스트 응답 생성
    - generate_json(): JSON 응답 생성
    - generate_with_context(): 시스템 프롬프트 + 사용자 메시지
    - 재시도 로직 (최대 3회, 지수 백오프)
    - JSON 파싱 (마크다운 코드 블록 제거)

class DummyGeminiClient:
    """API 키 없이 개발/테스트용 더미 클라이언트"""

def get_gemini_client():
    """API 키 있으면 실제, 없으면 더미 클라이언트 반환"""
```

### 2. 업데이트된 파일

#### [`backend/domain/agents/consultant_agent.py`](backend/domain/agents/consultant_agent.py)
**변경 전**:
```python
# 하드코딩된 질문 리스트
question_sequence = [
    ("project_name", "프로젝트 이름은 무엇인가요?"),
    ("payment", "결제 수단은..."),
    # ...
]
```

**변경 후**:
```python
# LLM을 사용한 동적 질문 생성
llm_client = get_gemini_client()
response = llm_client.generate_with_context(
    system_prompt=CONSULTANT_SYSTEM_PROMPT,
    user_message=user_prompt
)
# 응답 파싱하여 질문 추출 (1-5개)
```

**장점**:
- ✅ 프로젝트 컨텍스트에 맞는 질문
- ✅ 사용자 답변 기반 후속 질문
- ✅ 더 자연스러운 대화 흐름

#### [`backend/domain/agents/judge_agent.py`](backend/domain/agents/judge_agent.py)
**변경 전**:
```python
# 단순 카운트 체크
info_count = len(state.collected_info)
if info_count >= 5:
    state.is_complete = True
```

**변경 후**:
```python
# LLM 기반 지능형 평가
response = llm_client.generate_with_context(
    system_prompt=JUDGE_SYSTEM_PROMPT,
    user_message=user_prompt
)
# decision: approve/reject
# completeness_score: 0.0 ~ 1.0
# feedback: 구체적인 피드백
```

**장점**:
- ✅ 정보의 **질** 평가 (단순 개수가 아님)
- ✅ 기능적 명확성, 기술적 실현 가능성, NFR, 테스트 가능성 평가
- ✅ 부족한 영역에 대한 구체적인 피드백

#### [`.env.example`](.env.example)
```bash
# Google Gemini API 키 추가
GOOGLE_API_KEY=your-google-api-key-here
MODEL_NAME=gemini-1.5-pro  # 모델명 업데이트
```

## 사용 방법

### 1. API 키 받기 (무료!)

1. https://makersuite.google.com/app/apikey 접속
2. Google 계정 로그인
3. "Create API Key" 클릭
4. API 키 복사

**참고**: Gemini API는 generous free tier를 제공합니다!

### 2. 로컬 개발

```bash
# 1. .env 파일 생성
cp .env.example .env

# 2. API 키 추가
echo "GOOGLE_API_KEY=your-actual-key-here" >> .env

# 3. 앱 실행
streamlit run frontend/app.py
```

### 3. Streamlit Cloud 배포

1. Streamlit Cloud 대시보드 → Settings → Secrets
2. 다음 추가:
```toml
GOOGLE_API_KEY = "your-actual-key-here"
```
3. Deploy!

## Fallback 메커니즘

API 키가 없거나 LLM 호출 실패 시, 자동으로 **더미 응답**으로 전환됩니다:

```python
try:
    return GeminiClient()
except ValueError:
    print("⚠️ Falling back to DummyGeminiClient")
    return DummyGeminiClient()
```

- ✅ 개발 중 API 키 없이도 테스트 가능
- ✅ API 장애 시에도 앱 크래시 방지
- ✅ 사용자에게 경고 메시지 표시

## LLM 호출 흐름

```
User Input
    │
    ▼
┌──────────────────────────────────────┐
│  1. Consultant Agent                 │
│     ┌─────────────────────────┐      │
│     │ LLM: 질문 생성          │      │
│     │ Input: collected_info   │      │
│     │        user_input       │      │
│     │ Output: 3-5 questions   │      │
│     └─────────────────────────┘      │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│  2. Judge Agent                      │
│     ┌─────────────────────────┐      │
│     │ LLM: 완전성 평가        │      │
│     │ Input: collected_info   │      │
│     │        conversation     │      │
│     │ Output: approve/reject  │      │
│     │         completeness    │      │
│     │         feedback        │      │
│     └─────────────────────────┘      │
└────────────────┬─────────────────────┘
                 │
                 ▼ (if approved)
┌──────────────────────────────────────┐
│  3. Writer Agent                     │
│     규칙 기반 SRS 생성               │
│     (이미 동적이므로 LLM 불필요)     │
└──────────────────────────────────────┘
```

## 프롬프트 엔지니어링

### Consultant 프롬프트
```python
CONSULTANT_SYSTEM_PROMPT = """
당신은 경험 많은 Business Analyst(BA)입니다.
사용자의 요구사항을 듣고, 개발 가능한 수준의 SRS를 작성하기 위해
필요한 정보를 수집해야 합니다.

**질문 작성 가이드라인:**
- Yes/No 질문보다는 구체적인 답변을 유도하는 질문
- 기술적 세부사항 (인증 방식, 예상 트래픽, 데이터 구조 등)
- 우선순위가 높은 정보부터 질문
"""
```

### Judge 프롬프트
```python
JUDGE_SYSTEM_PROMPT = """
당신은 엄격한 품질 관리자(QA)이자 PM입니다.

**평가 기준:**
1. 기능적 명확성 (Functional Clarity)
2. 기술적 실현 가능성 (Technical Feasibility)
3. 비기능 요구사항 (NFR)
4. 테스트 가능성 (Testability)

**결정 규칙:**
- 위 4가지 중 3개 이상 만족 → APPROVE
- 그 외 → REJECT (부족한 영역과 이유 명시)
"""
```

## 성능 최적화

### 재시도 로직
```python
def generate(self, prompt, max_retries=3, retry_delay=1.0):
    for attempt in range(max_retries):
        try:
            return self.model.generate_content(prompt)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))  # 지수 백오프
```

### JSON 파싱
```python
# 마크다운 코드 블록 자동 제거
if "```json" in response_text:
    response_text = response_text.split("```json")[1].split("```")[0]
```

## 비용 관리

Google Gemini API **무료 할당량** (2024년 기준):
- **60 requests/minute** (RPM)
- **1,500 requests/day** (RPD)
- **1 million tokens/month**

SpecPilot 예상 사용량:
- 세션당 ~5-10 요청 (Consultant 질문 생성 + Judge 평가)
- 요청당 ~500-1000 tokens

**→ 무료 티어로 충분합니다!** 🎉

## 문제 해결

### Q: "API key not found" 에러
**A**: `.env` 파일에 `GOOGLE_API_KEY` 추가 또는 Streamlit Secrets 설정

### Q: "ModuleNotFoundError: No module named 'google.generativeai'"
**A**: `pip install google-generativeai` 실행 (requirements.txt에 포함됨)

### Q: 더미 응답만 반환됨
**A**: API 키가 올바르게 설정되었는지 확인. 콘솔에 "⚠️ Using DummyGeminiClient" 메시지 확인

### Q: JSON 파싱 에러
**A**: 프롬프트에서 JSON 형식을 명확히 요청. `generate_json()` 메서드 사용

## 다음 단계

### 즉시 개선 가능:
- [ ] 스트리밍 응답 (실시간 UI 업데이트)
- [ ] 프롬프트 캐싱 (비용 절감)
- [ ] 멀티모달 입력 (이미지, 파일 업로드)

### 장기 개선:
- [ ] Writer Agent도 LLM 기반으로 전환 (더 창의적인 SRS)
- [ ] Few-shot learning (예시 SRS 제공)
- [ ] RAG (Retrieval Augmented Generation) - 이전 SRS 참고

---

**이제 SpecPilot은 진짜 AI 기반 SRS 생성기입니다!** 🚀
