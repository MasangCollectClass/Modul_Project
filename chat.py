import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

st.title('마음 상담소')

with st.expander("상담 받을 MBTI 유형 선택"):
    mbti_choice = st.radio(
        "유형을 선택하세요",
        options=["ESTP", "ESFP", "ENFP","ENTP","ESTJ","ESFJ","ENFJ","ENTJ","ISTJ","ISFJ","INFJ","INTJ","ISTP","ISFP","INFP","INTP"],
        horizontal=True
    )

    # 라디오 버튼으로 선택할때, 처리할 프로세스
    # if mbti_choice == "ESTP":
    #     st.write("옵션 1이 선택되었습니다.")
    st.write(f"선택한 MBTI는 {mbti_choice} 입니다.")


# st.session_state : 세션에 키-값 형식으로 데이터를 저장하는 변수
# openai_model => str , message => []
if 'openai_model' not in st.session_state:
    st.session_state.openai_model = 'gpt-4.1'

# 메세지 세션 초기화
if 'message' not in st.session_state:
    st.session_state.message = []

# 기존의 메세지가 있다면 출력
for msg in st.session_state.message:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# prompt => 사용자 입력창
if prompt := st.chat_input('메세지를 입력하세요'):
    # messages => [], 대화 내용 추가
    st.session_state.message.append({
        'role': 'user',
        'content': prompt
    })

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        stream = client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=[
                {
                    'role': m['role'],
                    'content': m['content']
                }
                for m in st.session_state.message
            ],
            stream=True
        )
        response = st.write_stream(stream)

    st.session_state.message.append({
        'role': 'assistant',
        'content': response
    })  
