import streamlit as st
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))
from agent import agent_chat

st.set_page_config(page_title="Chat", page_icon="💬")
st.title('MBTI 분석 챗봇')
st.caption('10개의 문장을 입력하시면 MBTI를 분석해 드립니다.')

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.mbti_detected = False
    st.session_state.mbti_type = None

# 사이드바 상태 표시
with st.sidebar:
    st.subheader("MBTI 분석 상태")
    
    if st.session_state.mbti_detected and st.session_state.mbti_type:
        st.success(f"MBTI 분석 완료: {st.session_state.mbti_type}")
        st.write("이제 고민을 말씀해 주시면 상담을 도와드리겠습니다.")
    else:
        # 현재까지의 사용자 메시지 수 계산 (현재 입력 전까지)
        user_message_count = len([msg for msg in st.session_state.chat_history if msg[0] == "user"])
        st.info(f"MBTI 분석 중... ({min(user_message_count, 10)}/10)")
        # 진행률이 1.0을 초과하지 않도록 조정
        progress_value = min(user_message_count / 10, 1.0)
        st.progress(progress_value)
        st.write("MBTI를 분석하기 위해 10개의 문장이 필요합니다.")
        st.write("자유롭게 대화를 이어가 주세요!")

# 채팅 메시지 표시
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

# 사용자 입력
if prompt := st.chat_input("무엇이든 말씀해 주세요..." if not st.session_state.mbti_detected else "무엇이 고민이신가요?"):
    # 이전까지의 사용자 메시지만 추출 (현재 입력 제외)
    previous_user_messages = [msg[1] for msg in st.session_state.chat_history if msg[0] == "user"]
    
    # 사용자 메시지를 채팅 히스토리에 먼저 추가
    st.session_state.chat_history.append(("user", prompt))
    
    # 채팅 응답 생성 (이전 메시지만 전달)
    response, is_mbti_analyzed = agent_chat(prompt, previous_user_messages)
    
    # 어시스턴트 응답을 채팅 히스토리에 추가
    st.session_state.chat_history.append(("assistant", response))
    
    # MBTI가 분석되었는지 확인하고 상태 업데이트
    if is_mbti_analyzed and "MBTI 분석이 완료" in response:
        st.session_state.mbti_detected = True
        # 응답에서 MBTI 유형 추출 (예: "MBTI 분석이 완료되었습니다! 당신의 MBTI는 INTJ로 보입니다.")
        for mbti in ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
                     "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]:
            if mbti in response:
                st.session_state.mbti_type = mbti
                break
    
    # 채팅 새로고침
    st.rerun()

# 스타일 적용
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .stChatMessage {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)
