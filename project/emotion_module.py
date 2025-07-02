import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

allowed_emotions = [ ... ]  # 생략 가능, 앞서 작성한 목록과 동일

def analyze_sentiment(user_text: str) -> str:
    prompt = [
        {"role": "system", "content": f"너는 감정 분석가야. 다음 중 하나의 감정만 반환해: {', '.join(allowed_emotions)}."},
        {"role": "user", "content": f"사용자 문장: '{user_text}'"}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=prompt,
            temperature=0.0,
            max_tokens=5
        )
        sentiment = response.choices[0].message.content.strip()
        return sentiment if sentiment in allowed_emotions else "중립"
    except:
        return "중립"