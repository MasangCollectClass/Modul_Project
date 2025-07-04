import streamlit as st

# MBTI가 세션 상태에 없으면 접근 막기
if not st.session_state.get("mbti_type"):
    st.error("MBTI가 선택되거나 분석되지 않았습니다. 먼저 MBTI를 선택하거나 분석해 주세요.")
    st.stop()

# MBTI 표시
st.header(f"당신의 MBTI는 {st.session_state['mbti_type']} 입니다!")

st.header(f"{st.session_state['mbti_type']}인 당신에게 추천드려요!")

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
