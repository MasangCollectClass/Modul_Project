import streamlit as st
from cards import (
    chat_card,
    mbti_list,
)

st.title("마상 수거반")

st.markdown(
    "안녕하세요 마상 수거반입니다. 당신의 감정을 마음껏 표현해 주세요"
)

# 홈 화면에 띄울 미니카드
cols = st.columns(2)
with cols[0].container(height=310):
    chat_card()
with cols[1].container(height=310):
    mbti_list()