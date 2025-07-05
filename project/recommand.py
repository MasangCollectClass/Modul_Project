import streamlit as st
from travel import recommend_places_by_mbti
from music import recommend_music_by_emotion
from mbti_counsel_agent import conversation_manager
# MBTI가 세션 상태에 없으면 접근 막기
if not st.session_state.get("mbti_type"):
    st.error("MBTI가 선택되거나 분석되지 않았습니다. 먼저 MBTI를 선택하거나 분석해 주세요.")
    st.stop()

<<<<<<< HEAD
# MBTI가 세션 상태에 없으면 접근 막기
if not st.session_state.get("mbti_type"):
    st.error("MBTI가 선택되거나 분석되지 않았습니다. 먼저 MBTI를 선택하거나 분석해 주세요.")
    st.stop()

# MBTI 표시
st.header(f"당신의 MBTI는 {st.session_state['mbti_type']} 입니다!")

st.header(f"{st.session_state['mbti_type']}인 당신에게 추천드려요!")
=======
# 감정 가져오기
emotion = None
if conversation_manager.current_concern and conversation_manager.emotion_analyzed:
    emotion = conversation_manager.current_concern.get("emotion", None)
>>>>>>> api-integrator

# Streamlit 출력 확인
if emotion:
    st.info(f"감정 분석 결과: **{emotion}**")
else:
    st.warning("아직 감정 분석이 이루어지지 않았습니다.")
# MBTI 표시
st.header(f"당신의 MBTI는 {st.session_state['mbti_type']} 입니다!")

st.header(f"{st.session_state['mbti_type']}인 당신에게 추천드려요!")

mbti = st.session_state['mbti_type']
# 탭
tabs = st.tabs(["여행지 추천", "노래 추천"])

# 여행지 추천 탭
with tabs[0]:
<<<<<<< HEAD
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
=======
    st.subheader("🔍 맞춤 여행지 추천")
    places_text = recommend_places_by_mbti(mbti)
    st.markdown(f"```\n{places_text}\n```")

# 노래 추천 탭
with tabs[1]:
    st.subheader("🎵 감정 기반 노래 추천")

    if emotion:
        music_list = recommend_music_by_emotion(emotion)
        for music in music_list:
            st.markdown(f"**{music['title']}**")
            st.video(music['url'])
>>>>>>> api-integrator
