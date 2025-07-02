import joblib
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from mbti_predictor import predict_from_texts
from emotion import analyze_sentiment
from counsel import generate_counseling_response

# -------------------------------
# 모델 로딩
# -------------------------------
# 감정 분석 모델
emotion_model = joblib.load("emotion_model.pkl")
vectorizer_emotion = joblib.load("emotion_vectorizer.pkl")

# 상담 생성 모델 (GPT 기반은 별도 처리)
counsel_model = load_model("counsel_model_keras.h5")
with open("keras_tokenizer.pkl", "rb") as f:
    counsel_tokenizer = pickle.load(f)
MAX_LEN_COUNSEL = 50

# MBTI 예측 모델
mbti_model = load_model("mbti_predictor.h5")
with open("mbti_tokenizer.pkl", "rb") as f:
    mbti_tokenizer = pickle.load(f)
MAX_LEN_MBTI = 100

idx2mbti = {
    0: "INFP", 1: "ENFP", 2: "INFJ", 3: "ENFJ",
    4: "INTP", 5: "ENTP", 6: "INTJ", 7: "ENTJ",
    8: "ISFP", 9: "ESFP", 10: "ISTP", 11: "ESTP",
    12: "ISFJ", 13: "ESFJ", 14: "ISTJ", 15: "ESTJ"
}


# 기능 함수
def predict_mbti_tool(user_inputs: list) -> str:
    if len(user_inputs) < 5:
        return "문장은 최소 5개 이상 필요합니다."
    return predict_from_texts(user_inputs)

def predict_emotion_tool(user_text: str) -> str:
    return analyze_sentiment(user_text)

def generate_counsel_tool(user_text: str, mbti: str, song: str) -> str:
    return generate_counseling_response(user_text, mbti, song)


# Agent 도구 리스트
tools = [
    {
        "type": "function",
        "function": predict_mbti_tool,
        "name": "predict_mbti",
        "description": "5개 문장을 기반으로 MBTI 성격 유형을 예측합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_inputs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "사용자가 입력한 5개의 문장 리스트"
                }
            },
            "required": ["user_inputs"]
        }
    },
    {
        "type": "function",
        "function": predict_emotion_tool,
        "name": "predict_emotion",
        "description": "사용자 입력 문장에서 감정을 분류합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_text": {
                    "type": "string",
                    "description": "사용자가 입력한 텍스트"
                }
            },
            "required": ["user_text"]
        }
    },
    {
        "type": "function",
        "function": generate_counsel_tool,
        "name": "generate_counsel",
        "description": "MBTI와 감정 기반으로 상담 응답을 생성합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_text": {"type": "string", "description": "사용자의 고민 문장"},
                "mbti": {"type": "string", "description": "예측된 MBTI 유형"},
                "song": {"type": "string", "description": "추천 음악 제목"}
            },
            "required": ["user_text", "mbti", "song"]
        }
    }
]

if __name__ == '__main__':
    # 예시 테스트 흐름
    user_inputs = [
        "나는 혼자 있는 시간이 편해.",
        "다른 사람을 도울 때 보람을 느껴.",
        "가끔 감정 기복이 심한 편이야.",
        "계획보다는 즉흥적인 결정을 많이 해.",
        "사람들과 깊은 대화를 나누는 걸 좋아해."
    ]
    mbti = predict_mbti_tool(user_inputs)
    print(f"[MBTI 예측 결과] {mbti}")

    user_text = "진로에 대한 고민이 많고 요즘 불안해서 잠도 안 와."
    emotion = predict_emotion_tool(user_text)
    print(f"[감정 분석 결과] {emotion}")

    counseling = generate_counsel_tool(user_text, mbti, "IU - 밤편지")
    print("[상담 응답]")
    print(counseling)