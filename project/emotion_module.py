{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c34a91df",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "from dotenv import load_dotenv\n",
    "from openai import OpenAI\n",
    "\n",
    "load_dotenv()\n",
    "client = OpenAI(api_key=os.getenv(\"OPENAI_API_KEY\"))\n",
    "\n",
    "allowed_emotions = [ ... ]  # 생략 가능, 앞서 작성한 목록과 동일\n",
    "\n",
    "def analyze_sentiment(user_text: str) -> str:\n",
    "    prompt = [\n",
    "        {\"role\": \"system\", \"content\": f\"너는 감정 분석가야. 다음 중 하나의 감정만 반환해: {', '.join(allowed_emotions)}.\"},\n",
    "        {\"role\": \"user\", \"content\": f\"사용자 문장: '{user_text}'\"}\n",
    "    ]\n",
    "    try:\n",
    "        response = client.chat.completions.create(\n",
    "            model=\"gpt-4\",\n",
    "            messages=prompt,\n",
    "            temperature=0.0,\n",
    "            max_tokens=5\n",
    "        )\n",
    "        sentiment = response.choices[0].message.content.strip()\n",
    "        return sentiment if sentiment in allowed_emotions else \"중립\"\n",
    "    except:\n",
    "        return \"중립\""
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
