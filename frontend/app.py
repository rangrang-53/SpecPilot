"""SpecPilot Streamlit Frontend - Based on UX Wireframe"""
import streamlit as st
import json
from services.api_client import APIClient
from utils.srs_formatter import SRSFormatter


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

# Custom CSS based on SVG wireframes
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #f5f5f5;
    }

    /* Welcome Box (Blue) */
    .welcome-box {
        background-color: #eff6ff !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 25px !important;
        margin: 20px 0 !important;
    }

    /* Example Box (Gray) */
    .example-box {
        background-color: #f9fafb !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin: 20px 0 !important;
    }

    /* Question Card (Green) */
    .question-card {
        background-color: #f0fdf4 !important;
        border: 2px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
    }

    /* User Message (Blue) */
    .user-message {
        background-color: #eff6ff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }

    /* Success Banner (Green) */
    .success-banner {
        background-color: #d1fae5 !important;
        border: 2px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 30px !important;
        margin: 20px 0 !important;
        text-align: center;
    }

    /* Iteration Counter (Yellow) */
    .iteration-counter {
        background-color: #fef3c7 !important;
        border: 2px solid #f59e0b !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }

    /* Progress Steps */
    .step-complete {
        color: #10b981 !important;
        font-weight: bold;
    }
    .step-active {
        color: #3b82f6 !important;
        font-weight: bold;
    }
    .step-pending {
        color: #6b7280 !important;
    }

    /* Buttons */
    .stButton > button[kind="primary"] {
        background-color: #3b82f6 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Form Submit Button - Blue */
    .stFormSubmitButton > button {
        background-color: #3b82f6 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* Input Focus - Blue border to match theme */
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


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

        # 진행 단계 인디케이터 (와이어프레임 스타일)
        st.subheader("📈 진행 단계")

        # Step 1: 초기 입력
        if st.session_state.current_stage in ["interview", "complete"]:
            # Complete
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #10b981; border: 2px solid #059669; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: white; font-size: 14px; font-weight: bold;'>✓</span>
                </div>
                <span style='margin-left: 10px; color: #374151; font-size: 14px;'>초기 입력</span>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.current_stage == "initial":
            # Active
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #3b82f6; border: 3px solid #2563eb; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: white; font-size: 12px; font-weight: bold;'>1</span>
                </div>
                <span style='margin-left: 10px; color: #1e3a8a; font-size: 14px; font-weight: bold;'>초기 입력</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Pending
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #f3f4f6; border: 2px solid #d1d5db; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: #6b7280; font-size: 12px; font-weight: bold;'>1</span>
                </div>
                <span style='margin-left: 10px; color: #6b7280; font-size: 14px;'>초기 입력</span>
            </div>
            """, unsafe_allow_html=True)

        # Connector line
        st.markdown("<div style='width: 2px; height: 20px; background-color: #d1d5db; margin-left: 11px;'></div>", unsafe_allow_html=True)

        # Step 2: AI 질문
        if st.session_state.current_stage == "complete":
            # Complete
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #10b981; border: 2px solid #059669; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: white; font-size: 14px; font-weight: bold;'>✓</span>
                </div>
                <span style='margin-left: 10px; color: #374151; font-size: 14px;'>AI 질문</span>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.current_stage == "interview":
            # Active
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #3b82f6; border: 3px solid #2563eb; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: white; font-size: 12px; font-weight: bold;'>2</span>
                </div>
                <span style='margin-left: 10px; color: #1e3a8a; font-size: 14px; font-weight: bold;'>AI 질문 진행 중...</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Pending
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #e5e7eb; border: 2px solid #d1d5db; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: #6b7280; font-size: 12px; font-weight: bold;'>2</span>
                </div>
                <span style='margin-left: 10px; color: #6b7280; font-size: 14px;'>AI 질문</span>
            </div>
            """, unsafe_allow_html=True)

        # Connector line
        st.markdown("<div style='width: 2px; height: 20px; background-color: #d1d5db; margin-left: 11px;'></div>", unsafe_allow_html=True)

        # Step 3: 문서 생성
        if st.session_state.current_stage == "complete":
            # Complete
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #10b981; border: 2px solid #059669; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: white; font-size: 14px; font-weight: bold;'>✓</span>
                </div>
                <span style='margin-left: 10px; color: #374151; font-size: 14px;'>문서 생성</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Pending
            st.markdown("""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; border-radius: 50%; background-color: #e5e7eb; border: 2px solid #d1d5db; display: flex; align-items: center; justify-content: center;'>
                    <span style='color: #6b7280; font-size: 12px; font-weight: bold;'>3</span>
                </div>
                <span style='margin-left: 10px; color: #6b7280; font-size: 14px;'>문서 생성</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Iteration 카운터 (Yellow box with progress bar)
        st.subheader("🔄 Iteration Counter")
        iteration_pct = min((st.session_state.iteration_count / 10) * 100, 100)

        st.markdown(f"""
        <div class='iteration-counter'>
            <p style='font-size: 14px; color: #78350f; margin: 0; font-weight: bold;'>현재 반복:</p>
            <p style='font-size: 32px; color: #b45309; margin: 5px 0; font-weight: bold;'>
                {st.session_state.iteration_count}
                <span style='font-size: 18px; color: #92400e;'>/ 10</span>
            </p>
            <div style='background-color: #fde68a; height: 24px; border-radius: 4px; border: 1px solid #f59e0b; margin-top: 10px; position: relative;'>
                <div style='background-color: #f59e0b; height: 100%; width: {iteration_pct}%; border-radius: 4px;'></div>
                <span style='position: absolute; top: 3px; left: 50%; transform: translateX(-50%); font-size: 12px; color: #78350f; font-weight: bold;'>{int(iteration_pct)}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

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


def show_initial_screen():
    """초기 화면 (Wireframe 1)"""
    # current_stage는 세션이 없을 때만 설정
    if not st.session_state.session_id:
        st.session_state.current_stage = "initial"

    # 헤더 - SpecPilot 로고 및 타이틀
    st.title("✈️ SpecPilot")
    st.caption("AI-based SRS Generator - From Vague Ideas to Concrete Specs")

    st.divider()

    # 메인 영역 - 환영 메시지 (Blue Box)
    st.markdown("""
    <div class='welcome-box'>
        <h2 style='color: #1e3a8a; margin-top: 0;'>Welcome to SpecPilot! 👋</h2>
        <p style='color: #475569; font-size: 16px;'>AI 기반 요구사항 명세서 자동 생성 도구입니다.</p>
        <p style='color: #475569; font-size: 16px;'>프로젝트 아이디어를 입력하시면, AI가 질문을 통해</p>
        <p style='color: #475569; font-size: 16px;'>상세한 SRS 문서를 자동으로 작성합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 입력 가이드라인 (Gray Box)
    st.markdown("""
    <div class='example-box'>
        <p style='color: #1f2937; font-weight: bold; font-size: 15px; margin-top: 0;'>💡 입력 가이드라인</p>
        <p style='color: #6b7280; font-size: 13px; margin: 10px 0 5px 0;'>다음 정보를 포함하면 더 정확한 SRS를 생성할 수 있습니다:</p>
        <ul style='color: #374151; font-size: 13px; margin: 5px 0; padding-left: 20px;'>
            <li style='margin: 5px 0;'><strong>프로젝트 목적</strong>: 어떤 문제를 해결하려고 하나요?</li>
            <li style='margin: 5px 0;'><strong>주요 기능</strong>: 핵심 기능이나 특징은 무엇인가요?</li>
            <li style='margin: 5px 0;'><strong>사용자</strong>: 누가 이 시스템을 사용하나요?</li>
            <li style='margin: 5px 0;'><strong>규모</strong>: 예상 사용자 수나 트래픽은 어느 정도인가요?</li>
        </ul>
        <p style='color: #6b7280; font-weight: bold; font-size: 13px; margin-top: 15px; margin-bottom: 5px;'>입력 예시:</p>
        <p style='color: #374151; font-size: 13px; margin: 5px 0; padding: 8px; background-color: #f9fafb; border-left: 3px solid #3b82f6; border-radius: 4px;'>"온라인 쇼핑몰을 만들고 싶습니다. 의류와 액세서리를 판매하며, 월 1만 명 정도의 방문자를 예상합니다. 상품 검색, 장바구니, 결제 기능이 필요합니다."</p>
        <p style='color: #374151; font-size: 13px; margin: 5px 0; padding: 8px; background-color: #f9fafb; border-left: 3px solid #10b981; border-radius: 4px;'>"사내 인트라넷 시스템이 필요합니다. 직원 200명이 사용하며, 전자결재, 조직도, 공지사항, 회의실 예약 기능이 있어야 합니다."</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 입력창 - 초기 요구사항 입력
    st.subheader("📝 프로젝트 아이디어 입력")

    # Form을 사용하여 엔터키로 전송 가능하게 함
    with st.form(key="initial_input_form", clear_on_submit=True):
        user_input = st.text_area(
            "프로젝트에 대해 설명해주세요",
            placeholder="예: 온라인 쇼핑몰을 만들고 싶습니다. 상품 관리, 결제, 주문 관리 기능이 필요합니다.",
            height=150,
            help="간단한 설명만으로도 충분합니다. AI가 추가 질문을 통해 상세 정보를 수집합니다.",
            key="initial_input"
        )

        submit_button = st.form_submit_button("🚀 시작하기", use_container_width=True, type="primary")

    if submit_button:
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
    """질문-응답 화면 (Wireframe 2) - 02-qa-screen.svg 기반"""
    # current_stage는 is_complete가 아닐 때만 interview로 설정
    if not st.session_state.is_complete:
        st.session_state.current_stage = "interview"

    # 헤더
    st.title("✈️ SpecPilot")
    st.caption("AI Interview in Progress...")

    st.divider()

    # 채팅 히스토리 영역
    chat_container = st.container()

    with chat_container:
        for idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                # User Message - 파란색 박스 (우측 정렬)
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-end; margin: 15px 0;'>
                    <div style='background-color: #eff6ff; border: 1px solid #3b82f6; border-radius: 12px; padding: 15px; max-width: 70%;'>
                        <p style='font-size: 12px; color: #6b7280; margin: 0;'>👤 You</p>
                        <p style='font-size: 14px; color: #1e3a8a; margin-top: 8px; margin-bottom: 0;'>{msg["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # AI Question Card - 녹색 박스
                st.markdown(f"""
                <div style='background-color: #f0fdf4; border: 2px solid #10b981; border-radius: 12px; padding: 20px; margin: 15px 0;'>
                    <p style='font-size: 14px; color: #065f46; font-weight: bold; margin: 0;'>🧑‍✈️ Consultant Agent</p>
                    <p style='font-size: 13px; color: #374151; margin: 10px 0;'>추가 정보가 필요합니다. 다음 질문에 답변해 주세요:</p>
                    <div style='background-color: white; border: 1px solid #d1d5db; border-radius: 6px; padding: 12px; margin-top: 10px;'>
                        <p style='font-size: 14px; color: #374151; margin: 0;'>{msg["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Judge Thinking Indicator
        if st.session_state.iteration_count > 0 and not st.session_state.is_complete:
            st.markdown("""
            <div style='background-color: #fef3c7; border: 1px solid #f59e0b; border-radius: 6px; padding: 8px 15px; display: inline-block; margin: 10px 0;'>
                <span style='font-size: 12px; color: #92400e;'>⚖️ Judge evaluating...</span>
            </div>
            """, unsafe_allow_html=True)

    # 입력창 영역
    st.divider()

    # Form을 사용하여 엔터키로 전송 가능하게 함
    with st.form(key=f"qa_form_{len(st.session_state.messages)}", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])

        with col1:
            user_answer = st.text_input(
                "답변",
                placeholder="답변을 입력하세요...",
                label_visibility="collapsed"
            )

        with col2:
            send_button = st.form_submit_button("전송 →", use_container_width=True, type="primary")

    if send_button and user_answer.strip():
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_answer})

        # API 호출
        with st.spinner("⚖️ AI가 분석 중입니다..."):
            try:
                result = api_client.continue_session(
                    st.session_state.session_id,
                    user_answer
                )

                st.session_state.iteration_count = result.get("iteration_count", st.session_state.iteration_count)
                st.session_state.is_complete = result.get("is_complete", False)

                if st.session_state.is_complete:
                    # 완료 상태로 전환
                    st.session_state.current_stage = "complete"
                    # 완료 메시지
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "✅ 충분한 정보가 수집되었습니다! SRS 문서를 생성했습니다."
                    })
                    st.success("문서 생성 완료!")
                    st.rerun()
                else:
                    # 추가 질문
                    questions = result.get("questions", [])
                    if questions:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": questions[0]
                        })
                        st.rerun()

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
    elif send_button:
        st.warning("⚠️ 답변을 입력해주세요.")


def show_completion_screen():
    """문서 생성 완료 화면 (Wireframe 3) - 03-completion-screen.svg 기반"""
    st.session_state.current_stage = "complete"

    # 헤더
    st.title("✈️ SpecPilot")
    st.caption("SRS Generation Complete!")

    st.divider()

    # Success Banner - 녹색 완료 배너
    st.markdown("""
    <div class='success-banner'>
        <h1 style='color: #065f46; margin: 0; font-size: 28px;'>🎉 SRS 문서가 완성되었습니다!</h1>
        <p style='color: #374151; margin-top: 15px; font-size: 14px;'>아래에서 문서를 확인하고 다운로드하실 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

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


            # 다운로드 섹션 - Download Buttons
            st.subheader("📥 문서 다운로드")

            col1, col2, col3 = st.columns(3)

            with col1:
                # Markdown 다운로드 (파란색 버튼)
                formatter = SRSFormatter()
                markdown_content = formatter.to_markdown(srs_data)

                st.download_button(
                    label="📄 Markdown",
                    data=markdown_content,
                    file_name=f"{srs_data.get('project_name', 'project')}_SRS.md",
                    mime="text/markdown",
                    use_container_width=True,
                    type="primary"
                )

            with col2:
                # JSON 다운로드 (녹색 버튼)
                json_str = json.dumps(srs_data, ensure_ascii=False, indent=2)
                st.download_button(
                    label="{ } JSON",
                    data=json_str,
                    file_name=f"{srs_data.get('project_name', 'project')}_SRS.json",
                    mime="application/json",
                    use_container_width=True
                )

            with col3:
                # Copy 버튼 (회색)
                if st.button("📋 Copy", use_container_width=True):
                    st.info("📋 문서가 클립보드에 복사되었습니다!")

            st.divider()

            # Action Buttons
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                if st.button("← 대화 보기", use_container_width=True):
                    st.session_state.current_stage = "interview"
                    st.rerun()

            with col3:
                if st.button("+ 새 프로젝트", use_container_width=True, type="primary"):
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
