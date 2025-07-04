import streamlit as st
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))
from mbti_counsel_agent import agent_chat, conversation_manager, ConversationManager

# 페이지 설정
st.set_page_config(page_title="Chat", page_icon="💬")
st.title('MBTI 분석 챗봇')
st.caption('10개의 문장을 입력하시면 MBTI를 분석해 드립니다.')

# MBTI 유형 목록
MBTI_TYPES = [
    'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
    'ISTP', 'ISFP', 'INFP', 'INTP',
    'ESTP', 'ESFP', 'ENFP', 'ENTP',
    'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
]

def initialize_session():
    """세션 상태를 초기화합니다."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.chat_history = []
        st.session_state.mbti_detected = False
        st.session_state.mbti_type = None
        st.session_state.selected_mbti = '자동 분석'
        st.session_state.prev_selected_mbti = '자동 분석'
        st.session_state.conversation_id = None
        
        # 초기 인사말 설정
        initial_greeting = get_initial_greeting()
        st.session_state.chat_history = [("assistant", initial_greeting)]
        conversation_manager.messages = [{"role": "assistant", "content": initial_greeting}]
        conversation_manager.mbti = None
        conversation_manager.token_count = 0
        conversation_manager.last_question_index = 0  # 첫 번째 질문 시작을 1로 표시하기 위해 0으로 초기화

def get_initial_greeting(mbti_type: Optional[str] = None) -> str:
    """MBTI 유형에 따른 초기 인사말을 반환합니다."""
    if mbti_type and mbti_type != "자동 분석":
        return f"안녕하세요! {mbti_type} 유형으로 상담을 시작하겠습니다.\n\n" \
               f"무엇이든 편하게 말씀해 주세요. {mbti_type} 유형에 맞는 조언을 도와드리겠습니다."
    else:
        return "안녕하세요! MBTI 분석을 도와드리겠습니다.\n\n" \
               "위에서 MBTI 유형을 선택하시면 해당 유형으로 상담을 시작합니다.\n" \
               "선택하지 않으시면 10개의 질문을 통해 MBTI를 분석해 드립니다.\n\n" \
               "자, 첫 번째 질문이에요.\n" \
               "주말에 시간이 생기면 주로 무엇을 하시나요? (예: 집에서 휴식하기, 친구 만나기, 새로운 취미 활동하기 등)"

# 세션 상태 초기화
initialize_session()

# MBTI 선택 섹션
with st.expander("MBTI 유형 선택 (선택사항)"):
    # MBTI 선택기
    selected_mbti = st.radio(
        "MBTI 유형을 선택해주세요 (선택하지 않으면 자동으로 분석됩니다)",
        options=["자동 분석"] + MBTI_TYPES,
        index=0 if st.session_state.selected_mbti == "자동 분석" else MBTI_TYPES.index(st.session_state.selected_mbti) + 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # MBTI 선택이 변경된 경우
    if selected_mbti != st.session_state.prev_selected_mbti:
        # MBTI 설정 업데이트
        if selected_mbti != "자동 분석":
            conversation_manager.set_mbti(selected_mbti)
            st.session_state.mbti_type = selected_mbti
            st.session_state.mbti_detected = True
            
            # 새 인사말로 채팅 기록 업데이트
            new_greeting = get_initial_greeting(selected_mbti)
            st.session_state.chat_history = [("assistant", new_greeting)]
            conversation_manager.messages = [{"role": "assistant", "content": new_greeting}]
            
            st.success(f"MBTI가 {selected_mbti}로 설정되었습니다.")
        else:
            # 자동 분석 모드로 전환
            if 'mbti_type' in st.session_state:
                del st.session_state.mbti_type
            st.session_state.mbti_detected = False
            conversation_manager.mbti = None
            
            # 초기 인사말로 채팅 기록 업데이트
            new_greeting = get_initial_greeting()
            st.session_state.chat_history = [("assistant", new_greeting)]
            conversation_manager.messages = [{"role": "assistant", "content": new_greeting}]
        
        # 선택 상태 업데이트
        st.session_state.selected_mbti = selected_mbti
        st.session_state.prev_selected_mbti = selected_mbti
        
        # UI 업데이트를 위한 리렌더링
        st.rerun()

# 사이드바 상태 표시
with st.sidebar:
    st.header("MBTI 분석 상태")
    
    if st.session_state.get('mbti_detected', False) and st.session_state.get('mbti_type'):
        st.success(f"MBTI 분석 완료: {st.session_state.mbti_type}")
        st.write("자유롭게 대화를 이어가 주세요!")
    elif 'mbti_type' in st.session_state and st.session_state.mbti_type and st.session_state.mbti_type != "자동 분석":
        st.success(f"MBTI가 {st.session_state.mbti_type}로 설정되었습니다.")
        st.write("자유롭게 대화를 이어가 주세요!")
    else:
        # 현재까지의 사용자 메시지 수 계산
        user_message_count = conversation_manager.get_user_message_count()
        
        # 진행 상황 표시 (0에서 10 사이로 제한)
        progress_count = max(0, min(user_message_count, 10))  # 0부터 시작
        
        # 진행 상황 표시 (최소 0, 최대 10)
        st.info(f"MBTI 분석 중... ({progress_count}/10)")
        
        # 진행률 계산 (0.0에서 1.0 사이로 제한)
        progress_value = max(0.0, min(progress_count / 10, 1.0))
        st.progress(progress_value)
        
        st.write("MBTI를 분석하기 위해 10개의 문장이 필요합니다.")
        st.write("자유롭게 대화를 이어가 주세요!")
    
    # 대화 초기화 버튼
    if st.button("대화 초기화", use_container_width=True, type="primary", key="reset_button"):
        # conversation_manager 초기화
        from mbti_counsel_agent import conversation_manager
        
        # conversation_manager의 모든 상태 초기화
        conversation_manager.messages = []
        conversation_manager.mbti = None
        conversation_manager.token_count = 0
        conversation_manager.current_concern = None
        conversation_manager.concern_history = []
        conversation_manager.emotion_analyzed = False
        conversation_manager.current_question = None
        conversation_manager.last_question_index = 0  # 진행 상황 초기화
        conversation_manager.clarifying_question = False
        
        # 세션 상태 초기화
        st.session_state.chat_history = []
        st.session_state.mbti_detected = False
        st.session_state.mbti_type = None
        st.session_state.selected_mbti = "자동 분석"
        
        # 초기 인사말 설정 (자동 분석 모드)
        first_question = "안녕하세요! MBTI 분석을 도와드리겠습니다.\n\n" \
                       "위에서 MBTI 유형을 선택하시면 해당 유형으로 상담을 시작합니다.\n" \
                       "선택하지 않으시면 10개의 질문을 통해 MBTI를 분석해 드립니다.\n\n" \
                       "자, 첫 번째 질문이에요.\n" \
                       "주말에 시간이 생기면 주로 무엇을 하시나요? (예: 집에서 휴식하기, 친구 만나기, 새로운 취미 활동하기 등)"
        
        st.session_state.chat_history = [("assistant", first_question)]
        conversation_manager.messages = [{"role": "assistant", "content": first_question}]
        
        # 이전 선택값 초기화
        if 'prev_selected_mbti' in st.session_state:
            st.session_state.prev_selected_mbti = "자동 분석"
            
        # UI 업데이트를 위해 리렌더링
        st.rerun()
        
        # 사이드바 상태 초기화
        st.session_state.sidebar_updated = False
        
        # 페이지 새로고침을 통해 라디오 버튼 상태 업데이트
        st.rerun()

def display_chat_messages():
    """채팅 메시지를 표시하는 함수"""
    # 채팅 컨테이너 생성
    chat_container = st.container()
    
    with chat_container:
        # 중복 메시지 방지를 위한 집합
        displayed_messages = set()
        
        # 메시지 표시
        for role, message in st.session_state.chat_history:
            # 시스템 메시지는 어시스턴트로 표시
            display_role = "assistant" if role == "system" else role
            message_key = f"{display_role}:{message}"
            
            if message_key not in displayed_messages:
                with st.chat_message(display_role):
                    st.write(message)
                displayed_messages.add(message_key)

def handle_user_input():
    """사용자 입력을 처리하는 함수"""
    # 채팅 입력 프롬프트 설정
    chat_input_text = "무엇이든 말씀해 주세요..."
    if st.session_state.get('mbti_detected', False) and st.session_state.get('mbti_type'):
        chat_input_text = f"{st.session_state.mbti_type} 유형에 대해 무엇이든 물어보세요!"
    
    # 사용자 입력 처리
    if prompt := st.chat_input(chat_input_text):
        # 동일한 메시지가 연속으로 오는 경우 무시
        if st.session_state.chat_history and st.session_state.chat_history[-1][1] == prompt:
            return
            
        # 사용자 메시지 추가
        st.session_state.chat_history.append(("user", prompt))
        
        # 챗봇 응답 생성
        with st.spinner("답변을 생성 중입니다..."):
            response = agent_chat(prompt)
        
        # MBTI 감지 상태 업데이트
        if not st.session_state.get('mbti_detected', False):
            is_mbti_analyzed = conversation_manager.get_mbti() is not None
            st.session_state.mbti_detected = is_mbti_analyzed
            if is_mbti_analyzed:
                st.session_state.mbti_type = conversation_manager.get_mbti()
        
        # 응답에서 MBTI 유형 감지 (필요한 경우)
        for mbti in MBTI_TYPES:
            if mbti in response:
                st.session_state.mbti_type = mbti
                st.session_state.mbti_detected = True
                conversation_manager.set_mbti(mbti)
                break
        
        # 챗봇 응답 추가
        st.session_state.chat_history.append(("assistant", response))
        
        # 화면 갱신
        st.rerun()

# 대화 기록 동기화 함수
def sync_conversation_to_ui():
    """대화 관리자의 메시지를 UI에 반영합니다."""
    # 대화 관리자에서 메시지 가져오기
    new_messages = [
        (msg["role"], msg["content"]) 
        for msg in conversation_manager.get_conversation_context()
        if msg["role"] in ["user", "assistant", "system"]
    ]
    
    # 기존 메시지와 새 메시지 병합 (중복 제거)
    existing_messages = set(f"{role}:{msg}" for role, msg in st.session_state.chat_history)
    
    for role, message in new_messages:
        message_key = f"{role}:{message}"
        if message_key not in existing_messages:
            st.session_state.chat_history.append((role, message))
    
    # MBTI 상태 업데이트
    mbti = conversation_manager.get_mbti()
    if mbti and not st.session_state.mbti_detected:
        st.session_state.mbti_detected = True
        st.session_state.mbti_type = mbti

# 채팅 메시지 표시
display_chat_messages()

# 사용자 입력 처리
handle_user_input()

# 대화 기록 동기화
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