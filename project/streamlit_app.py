import streamlit as st
from pathlib import Path
import sys

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# 페이지 설정
st.set_page_config(
    page_title="MBTI 상담소 - 마음 수거함",
    page_icon="💭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 페이지 스타일 적용
st.markdown("""
<style>
    /* 메인 컨텐츠 영역 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f6f9fc 0%, #eef2f5 100%);
        border-right: 1px solid #e0e0e0;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        margin: 4px 0;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #f0f2f6;
    }
    
    footer {
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바에 페이지 링크 추가
with st.sidebar:
    st.image("https://via.placeholder.com/200x60?text=MBTI+상담소", use_column_width=True)
    st.markdown("## 메뉴")
    
    # 페이지 이동 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("홈", use_container_width=True):
            st.session_state.page = "home"
        if st.button("Chat", use_container_width=True):
            st.session_state.page = "chat"
    
    with col2:
        if st.button("MBTI 유형", use_container_width=True):
            st.session_state.page = "mbti"
        if st.button("추천 콘텐츠", use_container_width=True):
            st.session_state.page = "recommend"
    
    st.markdown("---")
    st.markdown("""
    ### 마음 수거함이란?
    MBTI 유형을 기반으로 한 심리 상담 서비스입니다.
    당신의 감정과 고민을 편안하게 나눠보세요.
    """)
    
    # 푸터
    st.markdown("---")
    st.caption("© 2024 SK 쉴더스 26기 TEAM 6")

# 페이지별 컨텐츠 표시
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.title("마음 수거함에 오신 것을 환영합니다!")
    st.markdown("""
    ### MBTI 기반 심리 상담 서비스
    
    이 서비스는 여러분의 MBTI 유형을 분석하고, 그에 맞는 맞춤형 상담을 제공합니다.
    
    - **Chat**: MBTI 분석을 위한 대화를 나눠보세요.
    - **MBTI 유형**: 다양한 MBTI 유형별 특징을 확인하세요.
    - **추천 콘텐츠**: 당신의 MBTI에 맞는 추천 콘텐츠를 만나보세요.
    
    왼쪽 사이드바에서 원하는 메뉴를 선택해 주세요.
    """)

elif st.session_state.page == "chat":
    st.switch_page("pages/chat.py")

elif st.session_state.page == "mbti":
    st.switch_page("pages/mbti_list.py")

elif st.session_state.page == "recommend":
    st.switch_page("pages/recommand.py")