{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "653cb854",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pickle, os\n",
    "import tensorflow as tf\n",
    "from tensorflow.keras.preprocessing.sequence import pad_sequences\n",
    "\n",
    "model_paths = {\n",
    "    \"ei\": (\"models/ei_bilstm_model2.h5\", \"tokenizers/ei_tokenizer2.pkl\"),\n",
    "    \"ns\": (\"models/ns_bilstm_model2.h5\", \"tokenizers/ns_tokenizer2.pkl\"),\n",
    "    \"tf\": (\"models/tf_bilstm_model.h5\", \"tokenizers/tf_tokenizer.pkl\"),\n",
    "    \"jp\": (\"models/jp_bilstm_model.h5\", \"tokenizers/jp_tokenizer.pkl\"),\n",
    "}\n",
    "\n",
    "models, tokenizers = {}, {}\n",
    "MAX_LEN = 300\n",
    "thresholds = {\"ei\": 0.40, \"ns\": 0.85, \"tf\": 0.62, \"jp\": 0.50}\n",
    "label_pairs = {\"ei\": (\"E\", \"I\"), \"ns\": (\"N\", \"S\"), \"tf\": (\"T\", \"F\"), \"jp\": (\"J\", \"P\")}\n",
    "\n",
    "for trait, (model_file, tokenizer_file) in model_paths.items():\n",
    "    models[trait] = tf.keras.models.load_model(model_file)\n",
    "    with open(tokenizer_file, \"rb\") as f:\n",
    "        tokenizers[trait] = pickle.load(f)\n",
    "\n",
    "def predict_mbti(sentences: list[str]) -> str:\n",
    "    text = \" \".join(sentences)\n",
    "    result = \"\"\n",
    "    for trait in [\"ei\", \"ns\", \"tf\", \"jp\"]:\n",
    "        tokenizer = tokenizers[trait]\n",
    "        model = models[trait]\n",
    "        seq = tokenizer.texts_to_sequences([text])\n",
    "        padded = pad_sequences(seq, maxlen=MAX_LEN, padding='post')\n",
    "        prob = model.predict(padded)[0][0]\n",
    "        label = label_pairs[trait][0] if prob >= thresholds[trait] else label_pairs[trait][1]\n",
    "        result += label\n",
    "    return result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "73547e62",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
