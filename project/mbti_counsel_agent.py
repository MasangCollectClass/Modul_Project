import os
import json
import tiktoken
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


# 환경 변수 로드
project_root = Path(__file__).parent.absolute()
env_path = project_root / '.env'
load_dotenv(env_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY가 환경변수에 설정되지 않았습니다.")

# 상수 정의
MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 16000
SAFETY_MARGIN = 0.8
RESPONSE_TOKENS = 1000
MAX_CONTEXT_TOKENS = int((MAX_TOKENS - RESPONSE_TOKENS) * SAFETY_MARGIN)

# 토큰 카운터 초기화
try:
    encoding = tiktoken.encoding_for_model(MODEL_NAME)
except KeyError:
    encoding = tiktoken.get_encoding("cl100k_base")

# 로컬 모듈 임포트
from mbti_predictor import predict_mbti
from emotion import analyze_sentiment
from counsel import generate_counseling_response


client = OpenAI(api_key=OPENAI_API_KEY)

def count_tokens(text: str) -> int:
    """텍스트의 토큰 수를 계산합니다."""
    return len(encoding.encode(text))

class ConversationManager:
    def __init__(self, max_history: int = 20):
        self.messages: List[Dict[str, str]] = []
        self.max_history = max_history
        self.mbti: Optional[str] = None
        self.token_count = 0
        self.current_concern = None  # 현재 다루고 있는 고민
        self.concern_history = []    # 고민 이력
        self.emotion_analyzed = False  # 현재 고민에 대한 감정 분석 여부
        self.current_question = None  # 현재 질문
        self.last_question_index = -1  # 마지막으로 물어본 질문 인덱스
        self.clarifying_question = False  # 현재 명확한 질문을 요청 중인지 여부

    def get_user_message_count(self) -> int:
        """유효한 사용자 응답의 개수를 반환합니다."""
        # 초기 상태인 경우 0 반환
        if not self.messages or len(self.messages) <= 1:  # 초기 메시지만 있는 경우
            return 0
            
<<<<<<< HEAD
        # 명확한 질문을 요청하는 메시지는 카운트하지 않음
        clarification_keywords = ["이해가 안돼", "무슨 말이야", "다시 말해줘", "설명해줘", "질문을 모르겠어", "무슨 상황"]
        
        # 모든 사용자 메시지 중에서 유효한 응답만 필터링
        valid_responses = [
            msg for msg in self.messages 
            if msg["role"] == "user" and 
            not any(keyword in msg["content"].lower() for keyword in clarification_keywords)
        ]
        
        # 명확한 질문을 요청한 경우에는 진행 상황 유지 (클라이언트 측에서만 표시용)
        if self.clarifying_question:
            return max(0, self.last_question_index)  # 최소 0 반환
            
        # 진행 상황 반환 (0부터 시작, last_question_index를 우선 사용)
        return min(max(0, self.last_question_index), 10)
=======
        # 명확한 질문을 요청하는 메시지 패턴
        clarification_keywords = [
            "이해가 안돼", "무슨 말이야", "다시 말해줘", 
            "설명해줘", "질문을 모르겠어", "무슨 상황", 
            "무슨 뜻이야", "다시 질문해줘", "다시 말씀해 주세요",
            "다시 한번 말씀해 주시겠어요?", "다시 말씀해 주실 수 있을까요?"
        ]
        
        # 모든 사용자 메시지 가져오기
        user_messages = [msg for msg in self.messages if msg["role"] == "user"]
        
        # 유효한 응답만 필터링 (명확한 질문을 요청하는 메시지 제외)
        valid_responses = []
        for msg in user_messages:
            content = msg["content"].lower()
            # 명확한 질문을 요청하는 메시지가 아닌 경우에만 카운트
            if not any(keyword in content for keyword in clarification_keywords):
                valid_responses.append(msg)
        
        # 마지막 응답이 명확한 질문을 요청하는 경우, 진행 상황 유지
        if user_messages and any(keyword in user_messages[-1]["content"].lower() 
                               for keyword in clarification_keywords):
            return max(0, len(valid_responses) - 1)  # 현재 메시지는 제외
            
        # 진행 상황 반환 (최대 10)
        return min(len(valid_responses), 10)
>>>>>>> api-integrator

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
    
    def start_new_concern(self, concern_text: str) -> None:
        """새로운 고민 세션을 시작합니다."""
        self.current_concern = {
            "topic": concern_text,
            "start_time": datetime.now(),
            "emotion": None,
            "messages": []
        }
        self.emotion_analyzed = False
        self.concern_history.append(self.current_concern)
    
    def is_new_concern(self, user_input: str) -> bool:
        """새로운 고민인지 판단합니다."""
        if not self.current_concern:
            return True
            
        # 간단한 키워드 기반 판단
        new_topic_keywords = ["다른", "새로운", "다시", "추가로", "그런데", "아니"]     # 키워드 개선 필요함..!
        if any(keyword in user_input for keyword in new_topic_keywords):
            return True
            
        # 문장 길이 기반 판단
        if len(user_input.split()) > 20:
            return True
            
        return False
    
    def analyze_concern_emotion(self, user_input: str) -> str:
        """현재 고민에 대한 감정을 분석합니다."""
        if not self.current_concern or self.emotion_analyzed:
            return self.current_concern.get("emotion", "중립")
            
        emotion = analyze_sentiment(user_input)
        self.current_concern["emotion"] = emotion
        self.emotion_analyzed = True
        return emotion
    
    def get_conversation_context(self) -> List[Dict[str, str]]:
        """토큰 제한 내에서 대화 맥락을 반환합니다."""
        return self.messages[-10:]  # 최근 10개 메시지만 반환
    
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

def generate_mbti_question(previous_messages: List[str]) -> str:
    """MBTI 분석을 위한 질문을 생성합니다."""
    prompt = f"""
    다음은 사용자의 이전 대화 내용입니다. MBTI를 분석하기 위한 질문을 하나 생성해주세요.
    이전 대화: {previous_messages[-3:] if len(previous_messages) > 3 else previous_messages}
    
    MBTI 유형을 파악하기 위한 적절한 질문을 자연스럽게 해주세요.
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"MBTI 질문 생성 중 오류: {e}")
        return "MBTI를 더 잘 이해하기 위해 더 많은 대화를 나눠볼까요?"


def continue_counseling(user_input: str, context: List[Dict[str, str]], concern: dict, mbti: str) -> str:
    """이미 분석된 고민에 대한 후속 대화를 처리합니다."""
    prompt = f"""
    당신은 따뜻한 심리 상담가입니다. 
    MBTI: {mbti}
    현재 다루고 있는 주제: {concern['topic']}
    이전 감정 분석 결과: {concern.get('emotion', '중립')}
    
    다음 사용자 메시지에 대해 공감과 이해를 바탕으로 대화를 이어가세요.
    """
    
    try:
        messages = [{"role": "system", "content": prompt}]
        messages.extend(context)
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"상담 응답 생성 중 오류: {e}")
        return "이해하는 데 어려움이 있네요. 조금 더 자세히 말씀해 주시겠어요?"

def agent_chat(user_input: str) -> str:
    """
    사용자 입력에 대한 응답을 생성합니다.
    """
    global conversation_manager

    try:
        # 1. 새로운 고민인지 확인
        if conversation_manager.is_new_concern(user_input):
            conversation_manager.start_new_concern(user_input)
        
        # 2. 사용자 메시지 추가 (이미 추가된 메시지는 추가하지 않음)
        if not any(msg.get('content') == user_input and msg.get('role') == 'user' 
                  for msg in conversation_manager.messages[-3:]):
            conversation_manager.add_message("user", user_input)
        
        # 3. MBTI 분석이 안된 경우
        if conversation_manager.get_mbti() is None:
            user_messages = conversation_manager.get_user_messages()
            
            # 명확한 질문을 요청하는 경우 (질문을 이해하지 못했을 때)
            clarification_keywords = ["이해가 안돼", "무슨 말이야", "다시 말해줘", "설명해줘", "질문을 모르겠어", "무슨 상황"]
            if any(keyword in user_input.lower() for keyword in clarification_keywords) and conversation_manager.current_question:
                # 이전 질문을 다시 물어보고 진행 상황은 유지
                response = f"죄송합니다. 질문이 명확하지 않았나요?\n\n{conversation_manager.current_question}"
                conversation_manager.clarifying_question = True
                # 이미 추가된 메시지가 아닌 경우에만 추가
                if not any(msg.get('content') == response and msg.get('role') == 'assistant' 
                          for msg in conversation_manager.messages[-3:]):
                    conversation_manager.add_message("assistant", response)
                return response
            
            # 명확한 질문을 요청하는 메시지가 아닌 경우 (유효한 답변)
            if not any(keyword in user_input.lower() for keyword in clarification_keywords):
                # 이전에 명확한 질문을 요청한 경우 (이제 유효한 답변을 받음)
                if conversation_manager.clarifying_question:
                    conversation_manager.clarifying_question = False
                    # 진행 상황 업데이트 (이전 질문에 대한 답변이므로 인덱스 증가)
                    conversation_manager.last_question_index = min(
                        conversation_manager.last_question_index + 1,
                        10  # 최대 10개 질문
                    )
                # 새로운 정상적인 답변인 경우
                elif not conversation_manager.clarifying_question:
                    # 질문 인덱스 증가 (최대 10)
                    conversation_manager.last_question_index = min(
                        conversation_manager.last_question_index + 1,
                        10  # 최대 10개 질문
                    )
            
            # 3-1. 충분한 메시지가 쌓이지 않은 경우
<<<<<<< HEAD
            if len(user_messages) < 10:
                # 진행 상황 안내 메시지 (실제 답변한 질문 수 기준)
                current_progress = min(conversation_manager.last_question_index, 10)
                remaining = max(0, 10 - current_progress)
                progress_msg = f"[진행 상황: {current_progress}/10] MBTI 분석을 위해 {remaining}개 더 입력해주세요."
=======
            valid_message_count = conversation_manager.get_user_message_count()
            if valid_message_count < 10:
                # 진행 상황 안내 메시지 (유효한 답변 수 기준)
                remaining = 10 - valid_message_count
                progress_msg = f"[진행 상황: {valid_message_count}/10] MBTI 분석을 위해 {remaining}개 더 입력해주세요."
>>>>>>> api-integrator
                
                # MBTI 분석을 위한 질문 생성 (이미 생성된 질문이 없을 때만 새로 생성)
                if not conversation_manager.current_question or not conversation_manager.clarifying_question:
                    mbti_question = generate_mbti_question(user_messages)
                    conversation_manager.current_question = mbti_question
                else:
                    mbti_question = conversation_manager.current_question
                
                # 진행 상황과 질문을 결합하여 반환
                response = f"{progress_msg}\n\n{mbti_question}"
                
                # 이미 추가된 메시지가 아닌 경우에만 추가
                if not any(msg.get('content') == response and msg.get('role') == 'assistant' 
                          for msg in conversation_manager.messages[-3:]):
                    conversation_manager.add_message("assistant", response)
                
                conversation_manager.clarifying_question = False  # 명확한 질문 플래그 초기화
                return response
            
            # 3-2. MBTI 분석 수행 (유효한 메시지가 10개 이상인 경우)
            else:
                # 유효한 메시지만 필터링 (명확한 질문 요청 메시지 제외)
                clarification_keywords = ["이해가 안돼", "무슨 말이야", "다시 말해줘", "설명해줘", "질문을 모르겠어", "무슨 상황"]
                valid_user_messages = [
                    msg for msg in user_messages 
                    if not any(keyword in msg.lower() for keyword in clarification_keywords)
                ][-10:]  # 최근 10개 유효한 메시지만 사용
                
                if len(valid_user_messages) < 10:
                    # 충분한 유효한 메시지가 없으면 계속 진행
                    remaining = 10 - len(valid_user_messages)
                    progress_msg = f"[진행 상황: {len(valid_user_messages)}/10] MBTI 분석을 위해 {remaining}개 더 입력해주세요."
                    mbti_question = generate_mbti_question(valid_user_messages)
                    conversation_manager.current_question = mbti_question
                    response = f"{progress_msg}\n\n{mbti_question}"
                    conversation_manager.add_message("assistant", response)
                    return response
                
                user_texts = valid_user_messages  # 유효한 메시지만 사용
                mbti = predict_mbti(" ".join(user_texts))
                conversation_manager.set_mbti(mbti)
                
                welcome_msg = (
                    f"MBTI 분석이 완료되었습니다! 당신의 MBTI는 {mbti}로 보입니다.\n"
                    "이제 고민을 말씀해 주시면 감정 분석과 상담을 도와드리겠습니다.\n\n"
                    f"🌍 여행지 추천을 원하시면 '여행지 추천'이라고 말씀해 주세요!"
                )
                conversation_manager.add_message("assistant", welcome_msg)
                return welcome_msg
        
        # 4. MBTI 분석 완료 후 상담 진행
        current_concern = conversation_manager.current_concern
        
        # 4-1. 현재 고민에 대한 감정 분석이 안된 경우
        if not conversation_manager.emotion_analyzed:
            emotion = conversation_manager.analyze_concern_emotion(user_input)
            mbti = conversation_manager.get_mbti() or "UNKNOWN"
            # 상담 응답 생성
            counsel_response = generate_counseling_response(user_input, mbti, emotion)
<<<<<<< HEAD
            response = f"{counsel_response}"
            
            # 고민 정보 업데이트
=======

            response = f"{counsel_response}"
>>>>>>> api-integrator
            current_concern["emotion"] = emotion
            conversation_manager.emotion_analyzed = True
        else:
            response = continue_counseling(
                user_input,
                conversation_manager.messages[-5:],
                current_concern,
                conversation_manager.get_mbti() or "UNKNOWN"
            )
        
        # 어시스턴트 응답을 대화 기록에 추가
        conversation_manager.add_message("assistant", response)
        return response
        
    except Exception as e:
        error_msg = f"상담 중 오류가 발생했습니다: {str(e)}\n계속해서 이야기를 나눠보세요."
        conversation_manager.add_message("system", f"오류 발생: {str(e)}")
        return error_msg

# 테스트 코드
if __name__ == '__main__':
    print("상담을 시작합니다. '종료'를 입력하면 끝납니다.")
    print("-" * 50)
    
    while True:
        user_input = input("당신: ")
        if user_input.lower() in ['종료', '끝', 'exit', 'quit']:
            print("상담을 종료합니다.")
            break
            
        response = agent_chat(user_input)
        print(f"\n상담사: {response}\n")