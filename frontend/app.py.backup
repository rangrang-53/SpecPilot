"""SpecPilot Streamlit Frontend - Based on UX Wireframe"""
import streamlit as st
import json
from frontend.services.api_client import APIClient
from backend.utils.srs_formatter import SRSFormatter


# 페이지 설정
st.set_page_config(
    page_title="SpecPilot - AI SRS Generator",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Client 초기화
api_client = APIClient()

# 세션 상태 초기화
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_complete" not in st.session_state:
    st.session_state.is_complete = False
if "iteration_count" not in st.session_state:
    st.session_state.iteration_count = 0
if "current_stage" not in st.session_state:
    st.session_state.current_stage = "initial"


def render_sidebar():
    """사이드바 렌더링 (Wireframe 4)"""
    with st.sidebar:
        # 로고 및 타이틀
        st.title("✈️ SpecPilot")
        st.caption("AI-based SRS Generator")
        st.divider()

        # 프로젝트 정보
        st.subheader("📊 프로젝트 정보")
        if st.session_state.session_id:
            st.metric("세션 ID", st.session_state.session_id[:8] + "...", help="현재 세션의 고유 식별자")
        else:
            st.info("세션이 시작되지 않았습니다")

        st.divider()

        # 진행 단계 인디케이터
        st.subheader("📈 진행 단계")
        stages = [
            ("initial", "🔵 초기 입력", "프로젝트 아이디어 입력"),
            ("interview", "🟡 요구사항 수집", "AI와 대화 중"),
            ("complete", "🟢 문서 생성 완료", "SRS 문서 생성됨")
        ]

        for stage_key, stage_icon, stage_desc in stages:
            if st.session_state.current_stage == stage_key:
                st.markdown(f"**{stage_icon}** ← 현재")
                st.caption(stage_desc)
            else:
                st.markdown(f"{stage_icon}")

        st.divider()

        # Iteration 카운터
        st.subheader("🔄 반복 횟수")
        st.metric("Iteration", st.session_state.iteration_count,
                 help="AI와의 대화 반복 횟수 (질문-답변 사이클)")

        st.divider()

        # 세션 리셋 버튼
        if st.session_state.session_id:
            if st.button("🔄 새 세션 시작", use_container_width=True, type="primary"):
                st.session_state.session_id = None
                st.session_state.messages = []
                st.session_state.is_complete = False
                st.session_state.iteration_count = 0
                st.session_state.current_stage = "initial"
                st.rerun()

        st.divider()

        # 도움말 링크
        st.subheader("❓ 도움말")
        st.markdown("[📖 사용 가이드](https://github.com/anthropics/specpilot)")
        st.markdown("[💬 피드백 보내기](https://github.com/anthropics/specpilot/issues)")
        st.markdown("[🐛 버그 리포트](https://github.com/anthropics/specpilot/issues/new)")


def show_initial_screen():
    """초기 화면 (Wireframe 1)"""
    st.session_state.current_stage = "initial"

    # 헤더 - SpecPilot 로고 및 타이틀
    st.title("✈️ SpecPilot")
    st.caption("AI-based SRS Generator - From Vague Ideas to Concrete Specs")

    st.divider()

    # 메인 영역 - 환영 메시지
    st.markdown("""
    ### 👋 환영합니다!

    **SpecPilot**은 여러분의 모호한 아이디어를 구체적인 기술 명세서(SRS)로 변환해드립니다.

    #### 🚀 시작하기
    1. 아래 입력창에 프로젝트 아이디어를 간단히 설명해주세요
    2. AI가 필요한 정보를 질문합니다
    3. 질문에 답변하면 자동으로 SRS 문서가 생성됩니다

    #### 💡 예시
    - "온라인 쇼핑몰을 만들고 싶습니다"
    - "회사 내부 인사 관리 시스템이 필요합니다"
    - "블로그 플랫폼을 개발하려고 합니다"
    """)

    st.divider()

    # 입력창 - 초기 요구사항 입력
    st.subheader("📝 프로젝트 아이디어 입력")

    user_input = st.text_area(
        "프로젝트에 대해 설명해주세요",
        placeholder="예: 온라인 쇼핑몰을 만들고 싶습니다. 상품 관리, 결제, 주문 관리 기능이 필요합니다.",
        height=150,
        help="간단한 설명만으로도 충분합니다. AI가 추가 질문을 통해 상세 정보를 수집합니다.",
        key="initial_input"
    )

    if st.button("🚀 시작하기", use_container_width=True, type="primary"):
        if user_input.strip():
            with st.spinner("AI가 분석 중입니다..."):
                try:
                    result = api_client.start_session(user_input)
                    st.session_state.session_id = result["session_id"]
                    st.session_state.iteration_count = result.get("iteration_count", 0)
                    st.session_state.is_complete = result.get("is_complete", False)

                    # 메시지 추가
                    st.session_state.messages.append({
                        "role": "user",
                        "content": user_input
                    })

                    # AI 질문 추가 (하나씩만 표시)
                    questions = result.get("questions", [])
                    if questions:
                        # 첫 번째 질문만 표시
                        first_question = questions[0]
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": first_question
                        })

                    st.success("✅ 세션이 시작되었습니다!")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")
        else:
            st.warning("⚠️ 프로젝트 아이디어를 입력해주세요.")


def show_qa_screen():
    """질문-응답 화면 (Wireframe 2)"""
    st.session_state.current_stage = "interview"

    # 헤더
    st.title("💬 요구사항 수집 인터뷰")

    # 진행 상태 표시
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"AI와 대화하며 프로젝트 요구사항을 구체화합니다")
    with col2:
        st.metric("반복 횟수", st.session_state.iteration_count)

    st.divider()

    # 채팅 히스토리
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                # Consultant 질문 카드 - 강조 표시
                st.markdown("#### 🤔 Consultant의 질문")
                st.info(msg["content"])
            else:
                st.markdown(msg["content"])

    # 입력창 - 사용자 답변 입력
    if prompt := st.chat_input("답변을 입력해주세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # API 호출
        with st.spinner("AI가 분석 중입니다..."):
            try:
                result = api_client.continue_session(
                    st.session_state.session_id,
                    prompt
                )

                st.session_state.iteration_count = result.get("iteration_count", st.session_state.iteration_count)
                st.session_state.is_complete = result.get("is_complete", False)

                if st.session_state.is_complete:
                    # 완료 메시지
                    assistant_msg = "✅ 충분한 정보가 수집되었습니다! SRS 문서를 생성했습니다."
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_msg
                    })
                    with st.chat_message("assistant"):
                        st.success(assistant_msg)
                    st.rerun()
                else:
                    # 추가 질문 (하나씩만 표시)
                    questions = result.get("questions", [])
                    if questions:
                        # 첫 번째 질문만 표시
                        first_question = questions[0]
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": first_question
                        })
                        with st.chat_message("assistant"):
                            st.markdown("#### 🤔 Consultant의 질문")
                            st.info(first_question)
                        st.rerun()

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")


def show_completion_screen():
    """문서 생성 완료 화면 (Wireframe 3)"""
    st.session_state.current_stage = "complete"

    # 완료 알림 - SRS 생성 완료 메시지
    st.success("### 🎉 SRS 문서 생성 완료!")
    st.markdown("AI가 수집한 정보를 바탕으로 전문적인 SRS 문서를 생성했습니다.")

    st.divider()

    try:
        # SRS 조회
        result = api_client.get_srs(st.session_state.session_id)
        srs_json = result.get("final_srs")

        if srs_json:
            # final_srs가 이미 문자열이므로 JSON 파싱
            if isinstance(srs_json, str):
                srs_data = json.loads(srs_json)
            else:
                # 이미 딕셔너리인 경우 그대로 사용
                srs_data = srs_json

            # 문서 미리보기 - 생성된 SRS 내용 요약
            st.subheader("📄 문서 미리보기")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("프로젝트명", srs_data.get('project_name', 'N/A'))
            with col2:
                st.metric("기능 요구사항", len(srs_data.get('functional_requirements', [])))
            with col3:
                st.metric("기술 스택", len(srs_data.get('tech_stack', [])))

            # 개요
            with st.expander("📝 프로젝트 개요", expanded=True):
                st.markdown(srs_data.get('overview', 'N/A'))

            # 기능 요구사항 요약
            with st.expander("⚙️ 기능 요구사항 요약"):
                for req in srs_data.get('functional_requirements', []):
                    st.markdown(f"**{req['id']}**: {req['title']} (우선순위: {req['priority']})")

            st.divider()

            # 다운로드 버튼 - Markdown/JSON 형식 선택
            st.subheader("📥 다운로드")

            col1, col2, col3 = st.columns(3)

            with col1:
                # Markdown 변환 (기본 다운로드)
                formatter = SRSFormatter()
                markdown_content = formatter.to_markdown(srs_data)

                st.download_button(
                    label="📝 Markdown 다운로드",
                    data=markdown_content,
                    file_name=f"{srs_data.get('project_name', 'project')}_SRS.md",
                    mime="text/markdown",
                    use_container_width=True,
                    type="primary"
                )

            with col2:
                # JSON 다운로드용 문자열 생성
                json_str = json.dumps(srs_data, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📄 JSON 다운로드",
                    data=json_str,
                    file_name=f"{srs_data.get('project_name', 'project')}_SRS.json",
                    mime="application/json",
                    use_container_width=True
                )

            with col3:
                # 새 세션 시작 버튼
                if st.button("🔄 새 세션 시작", use_container_width=True):
                    st.session_state.session_id = None
                    st.session_state.messages = []
                    st.session_state.is_complete = False
                    st.session_state.iteration_count = 0
                    st.session_state.current_stage = "initial"
                    st.rerun()

            st.divider()

            # 상세 문서 뷰
            st.subheader("📋 상세 문서")

            tab1, tab2 = st.tabs(["📄 구조화된 뷰", "🔧 JSON 뷰"])

            with tab1:
                # 기능 요구사항
                st.markdown("### ⚙️ 기능 요구사항")
                for req in srs_data.get('functional_requirements', []):
                    with st.expander(f"{req['id']}: {req['title']} (우선순위: {req['priority']})"):
                        st.markdown(req['description'])
                        if req.get('tech_suggestions'):
                            st.markdown(f"**💡 기술 제안**: {', '.join(req['tech_suggestions'])}")

                # 비기능 요구사항
                nfr = srs_data.get('non_functional_requirements', [])
                if nfr:
                    st.markdown("### 📊 비기능 요구사항")
                    for item in nfr:
                        st.markdown(f"- {item}")

                # 기술 스택
                tech_stack = srs_data.get('tech_stack', [])
                if tech_stack:
                    st.markdown("### 🛠 기술 스택")
                    for tech in tech_stack:
                        st.markdown(f"**{tech['category']}**: {', '.join(tech['technologies'])}")
                        st.caption(tech['rationale'])

                # 테스트 시나리오
                scenarios = srs_data.get('test_scenarios', [])
                if scenarios:
                    st.markdown("### 🧪 테스트 시나리오 (Gherkin)")
                    for scenario in scenarios:
                        st.markdown(f"**{scenario['feature']}: {scenario['scenario']}**")
                        st.code(f"""
Given {scenario['given']}
When {scenario['when']}
Then {scenario['then']}
                        """, language="gherkin")

            with tab2:
                st.json(srs_data)

        else:
            st.warning("⚠️ SRS 문서가 아직 생성되지 않았습니다.")

    except json.JSONDecodeError as e:
        st.error(f"❌ JSON 파싱 오류: {str(e)}")
        st.write("DEBUG - srs_json:", srs_json if 'srs_json' in locals() else "N/A")
    except KeyError as e:
        st.error(f"❌ 필수 필드 누락: {str(e)}")
        st.write("DEBUG - srs_data keys:", srs_data.keys() if 'srs_data' in locals() else "N/A")
    except Exception as e:
        st.error(f"❌ SRS 조회 오류: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


def main():
    """메인 애플리케이션"""
    # 사이드바 렌더링
    render_sidebar()

    # 메인 영역 - 현재 상태에 따라 화면 전환
    if st.session_state.is_complete:
        show_completion_screen()
    elif st.session_state.session_id:
        show_qa_screen()
    else:
        show_initial_screen()


if __name__ == "__main__":
    main()
