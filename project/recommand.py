import streamlit as st

st.header("당신에게 추천드려요!")

# 탭
tabs = st.tabs(["여행지 추천", "노래 추천"])

# 여행지 추천 탭
with tabs[0]:
    cols = st.columns(3)
    with cols[0].container(border=False):
        st.header("여행지")
        st.markdown("*제주도*")
        st.subheader("추천 이유")
        st.markdown("*넓은 바다와 멋진 풍경!*")
    with cols[1].container(border=True):
        st.image("project/images/jeju.jpg", use_container_width=False)
        st.link_button("링크", url="https://visitjeju.net/kr", icon=":material/open_in_new:")

# 노래 추천 탭
with tabs[1]:
    st.container(border=True).video(
        "https://www.youtube.com/watch?v=-xDt6P58tt0&list=RD-xDt6P58tt0&start_radio=1", autoplay=False
    )
