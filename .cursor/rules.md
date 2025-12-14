# 개발 원칙 및 가이드라인
1. SOLID 원칙 지키기
2. Clean Architecture 따르기
3. 파일과 함수는 최대한 작은 단위로

# 태스크별 필수 개발 프로세스 (TDD)
1. 개발 시작
 - 1.1. 테스트 코드 작성
 - 1.2. 코딩
 - 1.3. 테스트 시작
 - 1.4. 테스트 에러 없을때까지 반복 수정
2. 현재 태스크의 전체 파일 작성 완료하면 현재 태스크에 포함된 모든 테스트 진행
 - 2.1. 테스트 에러 없을때까지 반복 수정

---

# 프로젝트 폴더 구조

```
SpecPilot/
├── backend/
│   ├── __init__.py
│   ├── presentation/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── session_routes.py
│   │   │   │   └── srs_routes.py
│   │   │   └── schemas/
│   │   │       ├── __init__.py
│   │   │       ├── request_schemas.py
│   │   │       └── response_schemas.py
│   │   └── main.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── session_service.py
│   │   │   └── srs_service.py
│   │   └── use_cases/
│   │       ├── __init__.py
│   │       ├── start_session_use_case.py
│   │       ├── continue_session_use_case.py
│   │       └── generate_srs_use_case.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── state.py
│   │   │   ├── srs.py
│   │   │   └── agent_response.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── consultant_agent.py
│   │   │   ├── judge_agent.py
│   │   │   └── writer_agent.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       └── session_repository.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   └── openai_client.py
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   ├── workflow.py
│   │   │   └── executor.py
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── checkpointer.py
│   │   │   └── state_store.py
│   │   └── prompts/
│   │       ├── __init__.py
│   │       ├── consultant_prompt.py
│   │       ├── judge_prompt.py
│   │       └── writer_prompt.py
│   └── utils/
│       ├── __init__.py
│       ├── info_extractor.py
│       ├── srs_formatter.py
│       └── quality_metrics.py
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── chat_interface.py
│   │   └── srs_preview.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── api_client.py
│   └── utils/
│       ├── __init__.py
│       └── formatters.py
├── tests/
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_agents.py
│   │   ├── test_services.py
│   │   └── test_workflow.py
│   └── frontend/
│       ├── __init__.py
│       └── test_components.py
├── docs/
│   ├── api-specification.md
│   └── ux-wireframe.md
├── wireframes/
│   ├── 01-initial-screen.svg
│   ├── 02-qa-screen.svg
│   ├── 03-completion-screen.svg
│   └── 04-sidebar.svg
├── tasks/
│   ├── 00-task-summary.md
│   ├── 01-project-setup.md
│   └── ...
├── config/
│   └── settings.py
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
├── README.md
├── prd.md
├── system-architecture.md
└── user-scenario.md
```
