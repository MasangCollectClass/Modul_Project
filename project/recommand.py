import streamlit as st
from travel import recommend_places_by_mbti
from music import recommend_music_by_emotion
from mbti_counsel_agent import conversation_manager

# MBTI가 세션 상태에 없으면 접근 막기
if not st.session_state.get("mbti_type"):
    st.error("MBTI가 선택되거나 분석되지 않았습니다. 먼저 MBTI를 선택하거나 분석해 주세요.")
    st.stop()

# 감정 가져오기
emotion = None
if conversation_manager.current_concern and conversation_manager.emotion_analyzed:
    emotion = conversation_manager.current_concern.get("emotion", None)

st.header(f"당신의 MBTI는 {st.session_state['mbti_type']} 입니다!")

st.header(f"{st.session_state['mbti_type']}인 당신에게 추천드려요!")

mbti = st.session_state['mbti_type']

# 탭 구성
tabs = st.tabs(["🌍 여행지 추천", "🎵 노래 추천"])

# 여행지 추천 탭
with tabs[0]:
    with st.container():
        st.subheader("🔍 맞춤 여행지 추천")
        places_text = recommend_places_by_mbti(mbti)
        st.markdown("#### 📌 추천 리스트")
        st.code(places_text, language='text')

# 노래 추천 탭
with tabs[1]:
    with st.container():
        st.subheader("🎵 감정 기반 노래 추천")

        if emotion:
            st.success(f"감정 분석 결과: **{emotion}**", icon="💡")
        else:
            st.warning("아직 감정 분석이 이루어지지 않았습니다.", icon="⚠️")
            st.info("노래 추천은 감정 분석 이후 가능합니다!")

        if emotion:
            st.markdown("#### 🎧 추천 곡 리스트")
            for music in recommend_music_by_emotion(emotion):
                with st.expander(f"🎵 {music['title']}"):
                    st.video(music['url'])
