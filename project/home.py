import streamlit as st
from cards import (
    chat_card,
    recommand,
    mbti_list,
)

st.title("마음 수거함 홈페이지 입니다")

st.markdown(
    "MBTI 유형을 기반으로 한 심리 상담 서비스입니다." 
    "당신의 감정과 고민을 편안하게 나눠보세요."
)

# 홈 화면에 띄울 미니카드
cols = st.columns(2)
with cols[0].container(height=310):
    chat_card()
with cols[1].container(height=310):
    mbti_list()

cols2 = st.columns(2)
with cols2[0].container(height=310):
    recommand()