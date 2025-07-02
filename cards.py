import streamlit as st

# 사이드메뉴 하단에 표시되는 작은 미리보기 칸 입니다.

def chat_card():
    st.page_link("chat.py", label="Chat", icon=":material/chat:")
    st.chat_message("user").write("상담해주세요")
    st.chat_message("assistant").write("언제든지요!")
    st.chat_input("Type something")

def mbti_list():
    st.page_link("mbti_list.py", label="MBTI List", icon=":material/favorite:")
    st.container(border=True).video("https://www.youtube.com/watch?v=Y8P1Bp_X1Ts", autoplay=False)