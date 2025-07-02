{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "65a3df11",
   "metadata": {},
   "outputs": [],
   "source": [
    "from fastapi import FastAPI\n",
    "from pydantic import BaseModel\n",
    "from mbti_module import predict_mbti\n",
    "from emotion_module import analyze_sentiment\n",
    "from counsel_module import generate_response\n",
    "\n",
    "app = FastAPI()\n",
    "\n",
    "class MBTIRequest(BaseModel):\n",
    "    sentences: list[str]\n",
    "\n",
    "class CounselRequest(BaseModel):\n",
    "    text: str\n",
    "    mbti: str\n",
    "\n",
    "@app.post(\"/predict-mbti\")\n",
    "def predict_mbti_route(data: MBTIRequest):\n",
    "    mbti = predict_mbti(data.sentences)\n",
    "    return {\"mbti\": mbti}\n",
    "\n",
    "@app.post(\"/analyze-emotion\")\n",
    "def analyze_emotion_route(data: CounselRequest):\n",
    "    emotion = analyze_sentiment(data.text)\n",
    "    return {\"emotion\": emotion}\n",
    "\n",
    "@app.post(\"/counsel\")\n",
    "def counsel_route(data: CounselRequest):\n",
    "    response = generate_response(data.text, data.mbti)\n",
    "    return {\"response\": response}"
   ]
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
