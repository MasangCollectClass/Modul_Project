import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from mbti_predictor import predict_from_texts
from emotion import analyze_sentiment             # 감정 분석 함수
# 감정분석기
emotion_model = joblib.load("emotion_model.pkl")
vectorizer_emotion = joblib.load("emotion_vectorizer.pkl")

# 상담
counsel_model = load_model("counsel_model_keras.h5")
with open("keras_tokenizer.pkl", "rb") as f:
    counsel_tokenizer = pickle.load(f)
MAX_LEN_COUNSEL = 50

# MBTI예측모델
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

def predict_mbti_tool(user_inputs: list) -> str:
    if len(user_inputs) < 5:
        return "문장은 최소 5개 이상 필요합니다."
    return predict_from_texts(user_inputs)

# 감정 분석 함수(연동용)
def detect_emotion_tool(text: str) -> str:
    return analyze_sentiment(text)

# mbti 툴 분석
mbti_tools = [
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
    }
]

# 감정 분석 툴
emotion_tools = [
    {
        "type": "function",
        "function": detect_emotion_tool,
        "name": "analyze_emotion",
        "description": "입력 문장에 대해 감정을 분류합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "감정을 분석할 사용자 문장"
                }
            },
            "required": ["text"]
        }
    }
]

if __name__ == '__main__':
    sample_sentences = [
        "혼자 있는 게 편해요.",
        "사람 많은 곳은 금방 지쳐요.",
        "감정 표현은 잘 안 하는 편이에요.",
        "계획보다 즉흥을 좋아해요.",
        "생각이 많아지는 밤이 싫지 않아요."
    ]
    mbti_result = predict_mbti_tool(sample_sentences)
    print(f"[MBTI 예측 결과] {mbti_result}")

    emotion_result = detect_emotion_tool("정말 속상하고 억울해")
    print(f"[감정 분석 결과] {emotion_result}")