import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 모델 및 토크나이저 경로
model_paths = {
    "ei": ("ei_bilstm_model2.h5", "ei_tokenizer2.pkl"),
    "ns": ("ns_bilstm_model.h5", "ns_tokenizer.pkl"),
    "tf": ("tf_bilstm_model.h5", "tf_tokenizer.pkl"),
    "jp": ("jp_bilstm_model.h5", "jp_tokenizer.pkl"),
}

# 모델 및 토크나이저 로딩
models = {}
tokenizers = {}
max_len = 300

for trait, (model_file, tokenizer_file) in model_paths.items():
    models[trait] = tf.keras.models.load_model(model_file)
    with open(tokenizer_file, "rb") as f:
        tokenizers[trait] = pickle.load(f)

# 텍스트 전처리 함수
def preprocess(text, tokenizer):
    seq = tokenizer.texts_to_sequences([text])
    pad = pad_sequences(seq, maxlen=max_len, padding='post')
    return pad

# MBTI 예측 함수
def predict_mbti(text: str) -> str:
    result = ""
    label_pairs = {
        "ei": ("E", "I"),
        "ns": ("N", "S"),
        "tf": ("T", "F"),
        "jp": ("J", "P"),
    }
    for trait in ["ei", "ns", "tf", "jp"]:
        x = preprocess(text, tokenizers[trait])
        pred = models[trait].predict(x)[0][0]
        pos, neg = label_pairs[trait]
        label = pos if round(pred) == 1 else neg
        result += label
    return result


# 사용자 입력 누적 리스트
session_inputs = []

# 문장 누적 함수
def add_user_text(text: str):
    session_inputs.append(text)
    print(f"현재 누적 문장 수: {len(session_inputs)}")
    
    if len(session_inputs) >= 5:
        combined = ' '.join(session_inputs)
        mbti = predict_mbti(combined)
        print(f"[예측된 MBTI] → {mbti}")
        return mbti
    else:
        print("문장을 5개 이상 입력하면 MBTI를 예측합니다.")
        return None


def predict_from_texts(text_list):
    combined = ' '.join(text_list)
    return predict_mbti(combined)

# 사용 예시
if __name__ == '__main__':
    test_inputs = [
        "혼자 있는 게 싫어요.",
        "사람 많은 곳이 좋아요.",
        "감정 표현은 잘 안 하는 편이에요.",
        "계획보다 즉흥을 좋아해요.",
        "생각이 많아지는 밤이 싫지 않아요."
    ]
    # 예측 수행
    predicted_mbti = predict_from_texts(test_inputs)

    # 출력
    print(f"[예측된 MBTI] → {predicted_mbti}")