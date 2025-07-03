import streamlit as st
import sys
from pathlib import Path
from cards import (
    chat_card,
    mbti_list,
    recommand
)

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# 한번만 초기화 작업수행 (변화 상태 유지용)
# if "init" not in st.session_state:
#     st.session_state.init = True

# 사이드바 페이지 네비게이션
pages = [
    st.Page(
        "home.py",
        title="Home",
        icon=":material/home:"
    ),
    st.Page(
        "chat.py",
        title="Chat",
        icon=":material/chat:"
    ),
    st.Page(
        "mbti_list.py",
        title="MBTI List",
        icon=":material/favorite:"
    ),
    st.Page(
        "recommand.py",
        title="Recommand",
        icon=":material/thumb_up:"
    ),
]

page = st.navigation(pages)
page.run()

# 사이드바 하단 컨테이너
with st.sidebar.container(height=310):
    if page.title == "Chat":
        chat_card()
    elif page.title == "MBTI List":
        mbti_list()
    elif page.title == "Recommand":
        recommand()
    else:
        st.page_link("home.py", label="Home", icon=":material/home:")
        st.write("마음 수거함 홈페이지 입니다.")
        st.write(
            "MBTI 유형을 기반으로 한 심리 상담 서비스입니다." 
            "당신의 감정과 고민을 편안하게 나눠보세요."
        )

# 사이드바 하단 캡션
st.sidebar.caption(
    "© 2024 SK 쉴더스 26기 TEAM 6"
)