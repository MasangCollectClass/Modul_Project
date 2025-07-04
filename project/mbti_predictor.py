import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ============ 설정 ============
MODEL_PATHS = {
    "ei": ("project/models/ei_bilstm_model2.h5", "project/tokenizers/ei_tokenizer2.pkl"),
    "ns": ("project/models/ns_bilstm_model2.h5", "project/tokenizers/ns_tokenizer2.pkl"),
    "tf": ("project/models/tf_bilstm_model2.h5", "project/tokenizers/tf_tokenizer2.pkl"),
    "jp": ("project/models/jp_final.h5", "project/tokenizers/jp_final.pkl"),
}
THRESHOLDS = {"ei": 0.40, "ns": 0.85, "tf": 0.62, "jp": 0.50}
LABEL_PAIRS = {
    "ei": ("E", "I"),
    "ns": ("N", "S"),
    "tf": ("T", "F"),
    "jp": ("J", "P"),
}
MAX_LEN = 300

# ============ 모델 및 토크나이저 로딩 ============
models, tokenizers = {}, {}

for trait, (model_file, tokenizer_file) in MODEL_PATHS.items():
    models[trait] = tf.keras.models.load_model(model_file)
    with open(tokenizer_file, "rb") as f:
        tokenizers[trait] = pickle.load(f)

# ============ 전처리 및 예측 ============
def preprocess(text, tokenizer):
    seq = tokenizer.texts_to_sequences([text])
    return pad_sequences(seq, maxlen=MAX_LEN, padding='post')

def predict_mbti(text: str) -> str:
    result = ""
    for trait in ["ei", "ns", "tf", "jp"]:
        x = preprocess(text, tokenizers[trait])
        pred = models[trait].predict(x)[0][0]
        threshold = THRESHOLDS.get(trait, 0.5)
        label = LABEL_PAIRS[trait][0] if pred >= threshold else LABEL_PAIRS[trait][1]
        result += label
    return result

# ============ 사용자 입력 ============
if __name__ == '__main__':
    print("MBTI 예측을 위해 아래에 문장을 10개 입력해주세요.\n")
    session_inputs = []
    while len(session_inputs) < 10:
        text = input(f"{len(session_inputs)+1}번째 문장을 입력하세요: ").strip()
        if text:
            session_inputs.append(text)
        else:
            print("빈 문장은 입력할 수 없습니다. 다시 입력해주세요.")

    combined = ' '.join(session_inputs)
    mbti_result = predict_mbti(combined)

    print("\n[최종 예측된 MBTI] →", mbti_result)