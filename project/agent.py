import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

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

# 전역 상태 변수
session_inputs = []     # 사용자 누적 문장
mbti_state = None       # 예측된 MBTI

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

def agent_chat(user_input: str, chat_history: list) -> tuple[str, bool]:
    global mbti_state
    
    # MBTI 미설정 상태일 때 (10개 미만의 문장을 받은 경우)
    if mbti_state is None:
        # 현재까지의 사용자 메시지 수 계산 (chat_history는 이미 이전까지의 메시지만 포함)
        user_message_count = len(chat_history) + 1  # 현재 입력 포함
        
        # 10개 미만인 경우
        if user_message_count < 10:
            return f"MBTI 분석을 위한 문장 {user_message_count}/10을 입력하셨습니다.\n{10 - user_message_count}개 더 입력해 주세요.", False
        
        # 10개 이상인 경우 (현재 입력 포함)
        elif user_message_count >= 10:
            # 현재 입력을 포함한 10개 메시지 가져오기
            all_user_messages = chat_history.copy()
            all_user_messages.append(user_input)
            user_texts = all_user_messages[-10:]  # 최근 10개 메시지만 사용
            
            # MBTI 분석
            mbti_state = analyze_mbti(user_texts)
            return f"MBTI 분석이 완료되었습니다! 당신의 MBTI는 {mbti_state}로 보입니다.\n이제 고민을 말씀해 주시면 감정 분석과 상담을 도와드리겠습니다.", True

    # MBTI 분석 후 상담 진행
    try:
        emotion = analyze_sentiment(user_input)
        counsel_response = generate_counseling_response(user_input, mbti_state, recommended_song)
        return f"[감정 분석 결과: {emotion}]\n{counsel_response}", True
    except Exception as e:
        return f"상담 중 오류가 발생했습니다: {str(e)}\n계속해서 이야기를 나눠보세요.", False

# 테스트
if __name__ == '__main__':
    while True:
        user_input = input("사용자 입력: ")
        response = agent_chat(user_input)
        print("\n[에이전트 응답]\n" + response + "\n")