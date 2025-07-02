import pickle, os
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

model_paths = {
    "ei": ("models/ei_bilstm_model2.h5", "tokenizers/ei_tokenizer2.pkl"),
    "ns": ("models/ns_bilstm_model2.h5", "tokenizers/ns_tokenizer2.pkl"),
    "tf": ("models/tf_bilstm_model.h5", "tokenizers/tf_tokenizer.pkl"),
    "jp": ("models/jp_bilstm_model.h5", "tokenizers/jp_tokenizer.pkl"),
}

models, tokenizers = {}, {}
MAX_LEN = 300
thresholds = {"ei": 0.40, "ns": 0.85, "tf": 0.62, "jp": 0.50}
label_pairs = {"ei": ("E", "I"), "ns": ("N", "S"), "tf": ("T", "F"), "jp": ("J", "P")}

for trait, (model_file, tokenizer_file) in model_paths.items():
    models[trait] = tf.keras.models.load_model(model_file)
    with open(tokenizer_file, "rb") as f:
        tokenizers[trait] = pickle.load(f)

def predict_mbti(sentences: list[str]) -> str:
    text = " ".join(sentences)
    result = ""
    for trait in ["ei", "ns", "tf", "jp"]:
        tokenizer = tokenizers[trait]
        model = models[trait]
        seq = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=MAX_LEN, padding='post')
        prob = model.predict(padded)[0][0]
        label = label_pairs[trait][0] if prob >= thresholds[trait] else label_pairs[trait][1]
        result += label
    return result