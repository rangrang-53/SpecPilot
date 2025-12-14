# SpecPilot API 명세서

## 1. 세션 시작

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/session/start` |
| **HTTP 메서드** | `POST` |
| **요청 파라미터** | `initial_input` (string, required): 초기 요구사항 |
| **요청 예시** | ```json<br/>{<br/>  "initial_input": "온라인 쇼핑몰을 만들고 싶습니다"<br/>}<br/>``` |
| **응답 구조** | ```json<br/>{<br/>  "session_id": "string",<br/>  "questions": ["string"],<br/>  "is_complete": false,<br/>  "iteration_count": 1<br/>}<br/>``` |

---

## 2. 세션 계속

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/session/continue` |
| **HTTP 메서드** | `POST` |
| **요청 파라미터** | `session_id` (string, required): 세션 ID<br/>`user_response` (string, required): 사용자 답변 |
| **요청 예시** | ```json<br/>{<br/>  "session_id": "default_session_001",<br/>  "user_response": "결제는 카드와 가상계좌를 지원하고, 하루 주문은 1000건 정도입니다"<br/>}<br/>``` |
| **응답 구조** | ```json<br/>{<br/>  "session_id": "string",<br/>  "questions": ["string"],<br/>  "is_complete": false,<br/>  "judge_feedback": "string",<br/>  "iteration_count": 2,<br/>  "final_srs": null<br/>}<br/>``` |

---

## 3. SRS 문서 조회

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/srs/{session_id}` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | `session_id` (path, required): 세션 ID<br/>`format` (query, optional): 문서 형식 (json, markdown) |
| **요청 예시** | ```<br/>GET /api/srs/default_session_001?format=json<br/>``` |
| **응답 구조** | ```json<br/>{<br/>  "session_id": "string",<br/>  "project_name": "string",<br/>  "overview": "string",<br/>  "functional_requirements": [<br/>    {<br/>      "id": "string",<br/>      "title": "string",<br/>      "description": "string",<br/>      "priority": "High|Medium|Low",<br/>      "tech_suggestions": ["string"]<br/>    }<br/>  ],<br/>  "non_functional_requirements": ["string"],<br/>  "tech_stack": [<br/>    {<br/>      "category": "string",<br/>      "technologies": ["string"],<br/>      "rationale": "string"<br/>    }<br/>  ],<br/>  "test_scenarios": [<br/>    {<br/>      "feature": "string",<br/>      "scenario": "string",<br/>      "given": "string",<br/>      "when": "string",<br/>      "then": "string"<br/>    }<br/>  ],<br/>  "assumptions": ["string"]<br/>}<br/>``` |

---

## 4. 세션 상태 조회

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/session/{session_id}/status` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | `session_id` (path, required): 세션 ID |
| **요청 예시** | ```<br/>GET /api/session/default_session_001/status<br/>``` |
| **응답 구조** | ```json<br/>{<br/>  "session_id": "string",<br/>  "is_complete": false,<br/>  "iteration_count": 2,<br/>  "current_step": "consultant|judge|writer",<br/>  "created_at": "2025-12-14T17:30:00Z",<br/>  "updated_at": "2025-12-14T17:35:00Z"<br/>}<br/>``` |

---

## 5. 세션 리셋

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/session/{session_id}/reset` |
| **HTTP 메서드** | `POST` |
| **요청 파라미터** | `session_id` (path, required): 세션 ID |
| **요청 예시** | ```<br/>POST /api/session/default_session_001/reset<br/>``` |
| **응답 구조** | ```json<br/>{<br/>  "message": "Session reset successfully",<br/>  "session_id": "string"<br/>}<br/>``` |

---

## 6. 대화 히스토리 조회

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/session/{session_id}/messages` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | `session_id` (path, required): 세션 ID<br/>`limit` (query, optional): 메시지 수 제한<br/>`offset` (query, optional): 오프셋 |
| **요청 예시** | ```<br/>GET /api/session/default_session_001/messages?limit=10&offset=0<br/>``` |
| **응답 구조** | ```json<br/>{<br/>  "session_id": "string",<br/>  "messages": [<br/>    {<br/>      "role": "user|assistant|system",<br/>      "content": "string",<br/>      "timestamp": "2025-12-14T17:30:00Z"<br/>    }<br/>  ],<br/>  "total_count": 10<br/>}<br/>``` |

---

## 7. SRS 다운로드

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/srs/{session_id}/download` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | `session_id` (path, required): 세션 ID<br/>`format` (query, required): 다운로드 형식 (json, markdown) |
| **요청 예시** | ```<br/>GET /api/srs/default_session_001/download?format=markdown<br/>``` |
| **응답 구조** | ```<br/>Content-Type: application/octet-stream<br/>Content-Disposition: attachment; filename="project_name_SRS.md"<br/><br/>[파일 바이너리 데이터]<br/>``` |

---

## 8. 수집된 정보 조회

| 항목 | 내용 |
|------|------|
| **엔드포인트 URL** | `/api/session/{session_id}/collected-info` |
| **HTTP 메서드** | `GET` |
| **요청 파라미터** | `session_id` (path, required): 세션 ID |
| **요청 예시** | ```<br/>GET /api/session/default_session_001/collected-info<br/>``` |
| **응답 구조** | ```json<br/>{<br/>  "session_id": "string",<br/>  "collected_info": {<br/>    "payment_methods": ["string"],<br/>    "expected_users": 1000,<br/>    "authentication": "string",<br/>    "deployment": "string"<br/>  }<br/>}<br/>``` |
