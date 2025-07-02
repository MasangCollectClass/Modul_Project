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
MBTI_TONE = {
    "ENFP": "따뜻하고 유쾌하며 이모티콘을 자주 사용합니다.",
    "ISTJ": "분석적이고 신중하며 단정한 말투입니다.",
    "INFP": "섬세하고 감정에 공감하는 부드러운 말투입니다.",
    "ESTJ": "단호하고 체계적이며 사실 위주의 말투입니다.",
    "INTP": "논리적이고 중립적인 말투입니다.",
    "ESFJ": "친근하고 배려심 많은 말투로 위로를 잘 전합니다.",
    "ENTP": "재치 있고 유머러스하며 아이디어를 자유롭게 표현합니다.",
    "ISFJ": "조용하지만 따뜻하고 배려 깊은 말투로 상대를 존중합니다.",
    "INFJ": "직관적이며 깊이 있는 표현과 따뜻한 공감이 어우러진 말투입니다.",
    "ESTP": "직설적이고 에너지 넘치며 상황 중심적으로 조언합니다.",
    "ISFP": "차분하고 부드러우며 감정에 민감하게 반응합니다.",
    "INTJ": "간결하고 직관적인 말투이며 효율 중심적으로 접근합니다.",
    "ENTJ": "자신감 있고 목표 지향적이며 명확한 표현을 사용합니다.",
    "ENFJ": "따뜻하고 포용적인 말투로 감정에 깊이 공감합니다.",
    "ISTP": "과묵하고 실용적인 조언 위주로 핵심만 전달합니다.",
    "ESFP": "밝고 생동감 있는 말투로 친근하고 즉흥적인 표현을 자주 사용합니다."
}
# mbti 분석 툴
def predict_mbti_tool(user_inputs: list) -> str:
    if len(user_inputs) < 5:
        return "문장은 최소 5개 이상 필요합니다."
    return predict_from_texts(user_inputs)

# 감정 분석 함수(연동용)
def detect_emotion_tool(text: str) -> str:
    return analyze_sentiment(text)

# 상담 응답 생성 함수
def generate_counsel_response(user_text: str, mbti: str) -> str:
    seq = counsel_tokenizer.texts_to_sequences([user_text])
    pad = pad_sequences(seq, maxlen=MAX_LEN_COUNSEL, padding='post')
    response_idx = counsel_model.predict(pad).argmax(axis=1)[0]
    tone = MBTI_TONE.get(mbti, "공감하는 말투")
    return f"[{tone}] {response_idx}번 유형의 상담 응답입니다. (예시 응답 연결 필요)"
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
# 상담 툴
counsel_tools = [
    {
        "type": "function",
        "function": generate_counsel_response,
        "name": "generate_counsel_response",
        "description": "MBTI와 감정을 반영하여 상담 응답을 생성합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_text": {"type": "string", "description": "사용자 문장"},
                "mbti": {"type": "string", "description": "예측된 MBTI"}
            },
            "required": ["user_text", "mbti"]
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