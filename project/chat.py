import streamlit as st
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))
from mbti_counsel_agent import agent_chat, conversation_manager     # agent에서 mbti_counsel_agent로 변경

st.set_page_config(page_title="Chat", page_icon="💬")
st.title('MBTI 분석 챗봇')
st.caption('10개의 문장을 입력하시면 MBTI를 분석해 드립니다.')
with st.expander("MBTI 유형 선택"):
    mbti_choice = st.radio(
        "유형을 선택하세요",
        options=["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
                    "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"],
        horizontal=True
    )
    st.write(f"선택한 MBTI: {mbti_choice}")


# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.mbti_detected = False
    st.session_state.mbti_type = None
    st.session_state.conversation_id = None  # 대화 ID (필요시 사용)
    
    # 첫 번째 MBTI 분석 질문 추가
    first_question = "안녕하세요! MBTI 분석을 도와드리겠습니다.\n\n" \
                     "자, 첫 번째 질문이에요.\n" \
                     "주말에 시간이 생기면 주로 무엇을 하시나요? (예: 집에서 휴식하기, 친구 만나기, 새로운 취미 활동하기 등)"
    
    st.session_state.chat_history.append(("assistant", first_question))
    conversation_manager.add_message("assistant", first_question)

# 사이드바 상태 표시
with st.sidebar:
    st.subheader("MBTI 분석 상태")
    
    # MBTI 분석 상태 표시
    if st.session_state.mbti_detected and st.session_state.mbti_type:
        st.success(f"MBTI 분석 완료: {st.session_state.mbti_type}")
        st.write("이제 고민을 말씀해 주시면 상담을 도와드리겠습니다.")
    else:
        # 현재까지의 사용자 메시지 수 계산 (현재 입력 전까지)
        # conversation_manager에서 직접 사용자 메시지 수 가져오기
        user_message_count = conversation_manager.get_user_message_count()      # 수정된 코드(25.07.03 18:52)
        # user_message_count = len([msg for msg in st.session_state.chat_history if msg[0] == "user"])  # 기존 코드
        st.info(f"MBTI 분석 중... ({min(user_message_count, 10)}/10)")
        progress_value = min(user_message_count / 10, 1.0)
        st.progress(progress_value)
        st.write("MBTI를 분석하기 위해 10개의 문장이 필요합니다.")
        st.write("자유롭게 대화를 이어가 주세요!")
    
    # 대화 초기화 버튼
    if st.button("대화 초기화", use_container_width=True, type="primary"):
        # 세션 상태 초기화
        st.session_state.clear()
        # conversation_manager도 초기화
        from mbti_counsel_agent import conversation_manager     # agent에서 mbti_counsel_agent로 변경
        conversation_manager.messages = []
        conversation_manager.mbti = None
        conversation_manager.token_count = 0
        st.rerun()

# 채팅 메시지 표시
for role, message in st.session_state.chat_history:
    # 시스템 메시지도 어시스턴트 아이콘으로 표시
    display_role = "assistant" if role == "system" else role
    with st.chat_message(display_role):
        st.write(message)

# 대화 기록 동기화 함수
def sync_conversation_to_ui():
    """대화 관리자의 메시지를 UI에 반영합니다."""
    st.session_state.chat_history = [
        (msg["role"], msg["content"]) 
        for msg in conversation_manager.get_conversation_context()
        if msg["role"] in ["user", "assistant", "system"]
    ]
    
    # MBTI 상태 업데이트
    mbti = conversation_manager.get_mbti()
    if mbti and not st.session_state.mbti_detected:
        st.session_state.mbti_detected = True
        st.session_state.mbti_type = mbti

# 사용자 입력 처리
if prompt := st.chat_input("무엇이든 말씀해 주세요..." if not st.session_state.mbti_detected else "무엇이 고민이신가요?"):
    # 사용자 메시지 추가
    with st.chat_message("user"):
        st.write(prompt)
    
    # 채팅 응답 생성 (이전 대화 맥락은 agent_chat 내부에서 처리)
    # response, is_mbti_analyzed = agent_chat(prompt)   # 기존 코드
    response = agent_chat(prompt)                     # 수정된 코드(25.07.03 18:52)
    is_mbti_analyzed = conversation_manager.get_mbti() is not None

    # MBTI 분석 완료 상태 업데이트
    st.session_state.mbti_detected = is_mbti_analyzed
    
    # 응답 표시 (MBTI 분석 중인 경우 진행 상황 메시지 포함)
    with st.chat_message("assistant"):
        st.write(response)
    
    # MBTI 유형이 응답에 포함되어 있는지 확인
    if is_mbti_analyzed and not st.session_state.mbti_type:
        for mbti in ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
                    "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]:
            if mbti in response:
                st.session_state.mbti_type = mbti
                break
    
    # 대화 기록 동기화
    sync_conversation_to_ui()
    
    # 화면 갱신
    st.rerun()
else:
    # 페이지 로드 시 대화 기록 동기화
    sync_conversation_to_ui()

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

    /* 대화 초기화 버튼 스타일 */
    .stButton>button {
        width: 100%;
        margin-top: 1em;
    }
</style>
""", unsafe_allow_html=True)