"""SpecPilot Streamlit Frontend"""
import streamlit as st
import json
from frontend.services.api_client import APIClient


# 페이지 설정
st.set_page_config(
    page_title="SpecPilot - AI SRS Generator",
    page_icon="✈️",
    layout="wide",
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


def main():
    """메인 애플리케이션"""
    st.title("✈️ SpecPilot: AI-based SRS Generator")
    st.markdown("**From Vague Ideas to Concrete Specs**")

    # 사이드바
    with st.sidebar:
        st.header("세션 정보")
        if st.session_state.session_id:
            st.success(f"세션 ID: {st.session_state.session_id[:8]}...")
            st.info(f"완료 여부: {'✅ 완료' if st.session_state.is_complete else '⏳ 진행 중'}")

            if st.button("새 세션 시작"):
                st.session_state.session_id = None
                st.session_state.messages = []
                st.session_state.is_complete = False
                st.rerun()
        else:
            st.info("새 프로젝트를 시작해주세요")

    # 메인 영역
    if st.session_state.is_complete:
        show_srs_view()
    else:
        show_chat_view()


def show_chat_view():
    """채팅 인터페이스"""
    st.header("💬 요구사항 수집 인터뷰")

    # 대화 히스토리 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    if prompt := st.chat_input("프로젝트에 대해 알려주세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # API 호출
        try:
            if st.session_state.session_id is None:
                # 새 세션 시작
                result = api_client.start_session(prompt)
                st.session_state.session_id = result["session_id"]
            else:
                # 세션 계속
                result = api_client.continue_session(
                    st.session_state.session_id,
                    prompt
                )

            # 응답 처리
            st.session_state.is_complete = result.get("is_complete", False)

            if st.session_state.is_complete:
                # 완료 메시지
                assistant_msg = "✅ 충분한 정보가 수집되었습니다! SRS 문서를 생성했습니다."
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_msg
                })
                with st.chat_message("assistant"):
                    st.markdown(assistant_msg)
                st.rerun()
            else:
                # 추가 질문
                questions = result.get("questions", [])
                if questions:
                    questions_text = "\\n\\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
                    assistant_msg = f"추가 정보가 필요합니다:\\n\\n{questions_text}"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_msg
                    })
                    with st.chat_message("assistant"):
                        st.markdown(assistant_msg)

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")


def show_srs_view():
    """SRS 문서 뷰"""
    st.header("📝 생성된 SRS 문서")

    try:
        # SRS 조회
        result = api_client.get_srs(st.session_state.session_id)
        srs_json = result.get("final_srs")

        if srs_json:
            # JSON 파싱
            srs_data = json.loads(srs_json)

            # 탭으로 구성
            tab1, tab2 = st.tabs(["📄 문서 뷰", "🔧 JSON 뷰"])

            with tab1:
                # 프로젝트 개요
                st.subheader(f"🚀 {srs_data.get('project_name', 'N/A')}")
                st.markdown(srs_data.get('overview', 'N/A'))

                # 기능 요구사항
                st.subheader("⚙️ 기능 요구사항")
                for req in srs_data.get('functional_requirements', []):
                    with st.expander(f"{req['id']}: {req['title']} (우선순위: {req['priority']})"):
                        st.markdown(req['description'])
                        if req.get('tech_suggestions'):
                            st.markdown(f"**기술 제안:** {', '.join(req['tech_suggestions'])}")

                # 비기능 요구사항
                nfr = srs_data.get('non_functional_requirements', [])
                if nfr:
                    st.subheader("📊 비기능 요구사항")
                    for item in nfr:
                        st.markdown(f"- {item}")

                # 기술 스택
                tech_stack = srs_data.get('tech_stack', [])
                if tech_stack:
                    st.subheader("🛠 기술 스택")
                    for tech in tech_stack:
                        st.markdown(f"**{tech['category']}**: {', '.join(tech['technologies'])}")
                        st.caption(tech['rationale'])

                # 테스트 시나리오
                scenarios = srs_data.get('test_scenarios', [])
                if scenarios:
                    st.subheader("🧪 테스트 시나리오")
                    for scenario in scenarios:
                        st.markdown(f"**{scenario['feature']}: {scenario['scenario']}**")
                        st.markdown(f"- Given: {scenario['given']}")
                        st.markdown(f"- When: {scenario['when']}")
                        st.markdown(f"- Then: {scenario['then']}")
                        st.markdown("---")

            with tab2:
                st.json(srs_data)

            # 다운로드 버튼
            st.download_button(
                label="📥 JSON 다운로드",
                data=srs_json,
                file_name=f"{srs_data.get('project_name', 'project')}_SRS.json",
                mime="application/json",
            )

        else:
            st.warning("SRS 문서가 아직 생성되지 않았습니다.")

    except Exception as e:
        st.error(f"SRS 조회 오류: {str(e)}")


if __name__ == "__main__":
    main()
