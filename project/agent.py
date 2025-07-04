import os
import sys
import json
import tiktoken  # OpenAI 모델의 토큰을 계산하기 위한 라이브러리 (텍스트를 토큰 단위로 분리, 토큰 수를 계산하는데 사용)
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI

# 모델 설정
MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 16000  # gpt-3.5-turbo의 최대 토큰
SAFETY_MARGIN = 0.8  # 80%만 사용 (약 13,000 토큰)
RESPONSE_TOKENS = 1000  # 응답용으로 확보할 토큰
MAX_CONTEXT_TOKENS = int((MAX_TOKENS - RESPONSE_TOKENS) * SAFETY_MARGIN)

# 토큰 카운터 초기화
try:
    encoding = tiktoken.encoding_for_model(MODEL_NAME)
except KeyError:
    encoding = tiktoken.get_encoding("cl100k_base")  # gpt-3.5-turbo용 인코딩

# MBTI 예측 모듈 임포트
from mbti_predictor import predict_mbti

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# 로컬 모듈 임포트
from emotion import analyze_sentiment
from counsel import generate_counseling_response

# 환경변수 로드
env_path = project_root / '.env'
load_dotenv(env_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY가 환경변수에 설정되지 않았습니다.")

client = OpenAI(api_key=OPENAI_API_KEY)

def count_tokens(text: str) -> int:
    """텍스트의 토큰 수를 계산합니다."""
    return len(encoding.encode(text))

class ConversationManager:
    def __init__(self, max_history: int = 10):
        self.messages: List[Dict[str, str]] = []
        self.max_history = max_history
        self.mbti: Optional[str] = None
        self.token_count = 0
        
    def add_message(self, role: str, content: str) -> None:
        """대화 메시지를 추가하고 토큰 수를 업데이트합니다."""
        message = {"role": role, "content": content}
        message_tokens = count_tokens(f"{role}: {content}")
        
        # 토큰 제한을 초과하면 오래된 메시지부터 제거
        while self.token_count + message_tokens > MAX_CONTEXT_TOKENS and self.messages:
            removed = self.messages.pop(0)
            self.token_count -= count_tokens(f"{removed['role']}: {removed['content']}")
        
        self.messages.append(message)
        self.token_count += message_tokens
    
    def get_conversation_context(self) -> List[Dict[str, str]]:
        """토큰 제한 내에서 대화 맥락을 반환합니다."""
        # 이미 add_message에서 토큰 관리를 하므로 그대로 반환
        return self.messages
        
    def get_token_count(self) -> int:
        """현재 사용 중인 토큰 수를 반환합니다."""
        return self.token_count
    
    def set_mbti(self, mbti: str) -> None:
        """MBTI를 설정합니다."""
        self.mbti = mbti
    
    def get_mbti(self) -> Optional[str]:
        """MBTI를 반환합니다."""
        return self.mbti
    
    def get_user_messages(self) -> List[str]:
        """사용자 메시지만 반환합니다."""
        return [msg["content"] for msg in self.messages if msg["role"] == "user"]

# 전역 대화 관리자
conversation_manager = ConversationManager()

# 음악 추천 더미 값 (후에 연동 가능)
recommended_song = "IU - 밤편지"

def analyze_mbti(texts: list) -> str:
    """
    mbti_predictor를 사용하여 텍스트 목록을 분석하여 MBTI 유형을 예측합니다.
    """
    try:
        # 텍스트를 하나의 문자열로 결합
        combined_text = " ".join(texts)
        # mbti_predictor를 사용하여 MBTI 예측
        return predict_mbti(combined_text)
    except Exception as e:
        print(f"MBTI 분석 중 오류 발생: {e}")
        return "INTP"  # 오류 시 기본값

def trim_chat_history(chat_history: List[Tuple[str, str]]) -> List[Dict[str, str]]:
    """대화 기록을 토큰 제한 내에서 자릅니다."""
    total_tokens = 0
    trimmed_messages = []
    
    # 시스템 프롬프트 토큰 계산
    system_prompt = "당신은 친절한 상담사입니다. 이전 대화 맥락을 고려하여 답변해주세요."
    system_tokens = count_tokens(system_prompt)
    
    # 최신 메시지부터 추가 (역순으로 처리)
    for role, message in reversed(chat_history):
        message_content = f"{role}: {message}"
        message_tokens = count_tokens(message_content)
        
        if total_tokens + message_tokens + system_tokens > MAX_CONTEXT_TOKENS:
            break
            
        trimmed_messages.insert(0, {"role": "user" if role == "user" else "assistant", "content": message})
        total_tokens += message_tokens
    
    return trimmed_messages

def agent_chat(user_input: str, chat_history: list = None) -> tuple[str, bool]:
    """
    사용자 입력에 대한 응답을 생성합니다.
    
    Args:
        user_input: 사용자 입력 메시지
        chat_history: 이전 대화 기록 (호환성을 위해 유지)
        
    Returns:
        tuple: (응답 메시지, MBTI 분석 완료 여부)
    """
    global conversation_manager
    
    try:
        # 사용자 메시지 추가 (토큰 관리 포함)
        conversation_manager.add_message("user", user_input)
        
        # MBTI 미설정 상태일 때 (10개 미만의 문장을 받은 경우)
        if conversation_manager.get_mbti() is None:
            user_messages = conversation_manager.get_user_messages()
            user_message_count = len(user_messages)
            
            # 10개 미만인 경우
            if user_message_count < 10:
                progress_msg = f"MBTI 분석을 위한 문장 {user_message_count}/10을 입력하셨습니다.\n{10 - user_message_count}개 더 입력해 주세요."
                # 진행 상황을 시스템 메시지로 추가하여 유지
                conversation_manager.add_message("system", progress_msg)
                return progress_msg, False
            
            # 10개 이상인 경우 (현재 입력 포함)
            elif user_message_count >= 10:
                # 최근 10개 메시지만 사용
                user_texts = user_messages[-10:]
                
                # MBTI 분석
                mbti = analyze_mbti(user_texts)
                conversation_manager.set_mbti(mbti)
                
                # 대화 맥락에 MBTI 정보 추가
                conversation_manager.add_message(
                    "system", 
                    f"사용자의 MBTI는 {mbti}로 분석되었습니다. 이에 맞는 상담을 진행해주세요."
                )
                
                return (
                    f"MBTI 분석이 완료되었습니다! 당신의 MBTI는 {mbti}로 보입니다.\n"
                    "이제 고민을 말씀해 주시면 감정 분석과 상담을 도와드리겠습니다.", 
                    True
                )

        # MBTI 분석 후 상담 진행
        try:
            # 대화 맥락을 고려한 응답 생성
            emotion = analyze_sentiment(user_input)
            mbti = conversation_manager.get_mbti() or "UNKNOWN"
            counsel_response = generate_counseling_response(
                user_input, 
                mbti, 
                recommended_song
            )
            
            # 어시스턴트 응답을 대화 기록에 추가
            full_response = f"[감정 분석 결과: {emotion}]\n{counsel_response}"
            conversation_manager.add_message("assistant", full_response)
            
            return full_response, True
            
        except Exception as e:
            error_msg = f"상담 중 오류가 발생했습니다: {str(e)}\n계속해서 이야기를 나눠보세요."
            conversation_manager.add_message("system", f"오류 발생: {str(e)}")
            try:
                # 오류 메시지도 토큰 제한 내에서 추가
                conversation_manager.add_message("assistant", error_msg)
            except:
                pass
            return error_msg, True
            
    except Exception as e:
        error_msg = f"메시지 처리 중 오류가 발생했습니다: {str(e)}"
        print(error_msg)
        return error_msg, False

# 테스트
if __name__ == '__main__':
    while True:
        user_input = input("사용자 입력: ")
        response = agent_chat(user_input)
        print("\n[에이전트 응답]\n" + response + "\n")