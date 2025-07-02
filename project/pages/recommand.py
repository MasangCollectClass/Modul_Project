import streamlit as st

st.header("당신에게 추천드려요!")

# 탭
tabs = st.tabs(["여행지 추천", "노래 추천"])

# 여행지 추천 탭
with tabs[0]:
    st.container(border=True).video(
        "https://www.youtube.com/watch?v=exJF_Y3QFbg", autoplay=False
    )

# 노래 추천 탭
with tabs[1]:
    st.container(border=True).video(
        "https://www.youtube.com/watch?v=-xDt6P58tt0&list=RD-xDt6P58tt0&start_radio=1", autoplay=False
    )
