from fastapi import FastAPI
from pydantic import BaseModel
from mbti_module import predict_mbti
from emotion_module import analyze_sentiment
from counsel_module import generate_response

app = FastAPI()

class MBTIRequest(BaseModel):
    sentences: list[str]

class CounselRequest(BaseModel):
    text: str
    mbti: str

@app.post("/predict-mbti")
def predict_mbti_route(data: MBTIRequest):
    mbti = predict_mbti(data.sentences)
    return {"mbti": mbti}

@app.post("/analyze-emotion")
def analyze_emotion_route(data: CounselRequest):
    emotion = analyze_sentiment(data.text)
    return {"emotion": emotion}

@app.post("/counsel")
def counsel_route(data: CounselRequest):
    response = generate_response(data.text, data.mbti)
    return {"response": response}