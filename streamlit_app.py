import streamlit as st
import pandas as pd
import numpy as np
from cards import (
    chat_card,
    mbti_list,
)

# 한번만 초기화 작업수행 (변화 상태 유지용)
if "init" not in st.session_state:
    st.session_state.init = True

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
]

page = st.navigation(pages)
page.run()

# 사이드바 하단 컨테이너
with st.sidebar.container(height=310):
    if page.title == "Chat":
        chat_card()
    elif page.title == "MBTI List":
        mbti_list()
    else:
        st.page_link("home.py", label="Home", icon=":material/home:")
        st.write("마상수거반 홈페이지 입니다.")
        st.write(
            "메뉴를 클릭하면"
            "해당 페이지의 썸네일이 표시됩니다."
        )

# 사이드바 하단 캡션
st.sidebar.caption(
    "SK 쉴더스 26기 TEAM 6" 
    "mbti 상담소 마음 수거함 입니다"
)