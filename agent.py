import os
from dotenv import load_dotenv
from openai import OpenAI
from mbti_predictor import predict_mbti
from emotion import analyze_sentiment
from counsel import generate_counseling_response

# 환경변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# 전역 상태 변수
session_inputs = []     # 사용자 누적 문장
mbti_state = None       # 예측된 MBTI

# 음악 추천 더미 값 (후에 연동 가능)
recommended_song = "IU - 밤편지"

def agent_chat(user_input: str) -> str:
    global session_inputs, mbti_state

    # MBTI 미예측 상태일 때
    if mbti_state is None:
        session_inputs.append(user_input)
        if len(session_inputs) < 5:
            return f"현재 입력하신 문장은 총 {len(session_inputs)}개입니다. 5개가 되면 MBTI를 예측합니다."
        
        # 5문장 누적 완료/MBTI 예측
        combined_text = " ".join(session_inputs)
        mbti_state = predict_mbti(combined_text)
        return f"MBTI 예측이 완료되었습니다: {mbti_state}\n이제 고민을 말씀해 주세요. 감정 분석과 상담이 진행됩니다."

    # MBTI 예측이 끝난 후 감정 분석/상담 진행
    emotion = analyze_sentiment(user_input)
    counsel_response = generate_counseling_response(user_input, mbti_state, recommended_song)
    return f"[감정 분석 결과: {emotion}]\n{counsel_response}"

# 테스트
if __name__ == '__main__':
    while True:
        user_input = input("사용자 입력: ")
        response = agent_chat(user_input)
        print("\n[에이전트 응답]\n" + response + "\n")