# counsel.py
import os
import time
import openai
import re
from dotenv import load_dotenv
from openai import OpenAI
from serpapi import GoogleSearch

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
serpapi_key = os.getenv("SERPAPI_API_KEY")
client = OpenAI(api_key=api_key)

# 검색 제한 관리용 전역 변수
last_search_time = None
search_count = 0

MBTI_COMPATIBILITY_MAP = {
    "INTP": "INFJ", "INFJ": "ENFP", "ENFP": "INTJ", "INTJ": "ENFP",
    "ISFJ": "ESTP", "ESTP": "ISFJ", "ISTJ": "ESFP", "ESFP": "ISTJ",
    "INFP": "ENFJ", "ENFJ": "INFP", "ISFP": "ENTJ", "ENTJ": "ISFP",
    "ENTP": "ISFJ", "ESFJ": "INTP", "ESTJ": "INFP", "ISTP": "ENFJ"
}

MBTI_TONE = {
    "INTP": "논리적이고 차분하며 객관적인 말투입니다.",
    "INFJ": "깊이 있고 섬세하며 조용한 공감을 전하는 말투입니다.",
    "INFP": "감성적이고 따뜻하며 부드러운 말투입니다.",
    "INTJ": "간결하고 계획적이며 통찰력 있는 말투입니다.",
    "ISTJ": "신중하고 분석적이며 단정한 말투입니다.",
    "ISFJ": "조용하지만 배려심 깊고 다정한 말투입니다.",
    "ISTP": "간단명료하고 실용적인 조언을 주는 말투입니다.",
    "ISFP": "차분하고 부드러우며 감정에 섬세하게 반응하는 말투입니다.",
    "ENTP": "유쾌하고 재치 있으며 자유로운 아이디어를 표현하는 말투입니다.",
    "ENFP": "따뜻하고 유쾌하며 격려와 지지를 아끼지 않는 말투입니다.",
    "ENTJ": "분명하고 목표 지향적이며 명확한 의견을 전달하는 말투입니다.",
    "ENFJ": "포용적이고 섬세하며 감정에 깊이 공감하는 말투입니다.",
    "ESTP": "직설적이고 에너지 넘치며 실용적인 조언을 전하는 말투입니다.",
    "ESFP": "명랑하고 친근하며 생동감 있는 표현을 즐기는 말투입니다.",
    "ESTJ": "단호하고 체계적이며 현실적인 말투입니다.",
    "ESFJ": "배려 깊고 친근하며 공감과 위로에 능한 말투입니다."
}

COUNSELING_TOPICS = {
    "전문상담": ["우울증", "공황장애", "불면증", "자해", "자살", "약물", "정신병원", "과호흡", "웹", "인터넷", "검색", "찾아줘"],
    "관계상담": ["연애", "이별", "짝사랑", "왕따", "가족", "갈등"],
    "진로상담": ["진로", "이직", "퇴사", "입시", "진학"],
    "학업상담": ["공부", "성적", "과제", "시험"],
    "자기이해": ["자존감", "열등감", "자기혐오", "정체성"],
    "라이프스타일": ["휴가", "취미", "일상 변화", "생활 루틴"],
    "경제고민": ["돈", "월세", "대출", "알바"],
    "미래불안": ["불안감", "계획 없음", "비전 없음"],
    "감정불안정": ["무기력", "감정 기복", "멘탈 흔들림"]
}

def detect_topics(user_input: str) -> list:
    detected = []
    for topic, keywords in COUNSELING_TOPICS.items():
        for word in keywords:
            if re.search(rf"\\b{re.escape(word)}\\b", user_input):
                detected.append(topic)
                break
    return list(set(detected)) or ["일반"]

def can_search():
    global last_search_time, search_count
    now = time.time()
    if last_search_time and now - last_search_time > 3600:
        last_search_time = now
        search_count = 0
    if search_count < 20:
        search_count += 1
        return True
    return False

def search_expert_knowledge(query: str) -> str:
    if not can_search():
        return "[검색 제한 초과로 웹 검색을 생략합니다.]"
    try:
        search = GoogleSearch({"q": query, "api_key": serpapi_key})
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        return "\n".join([r["snippet"] for r in organic_results if "snippet" in r][:3])
    except Exception as e:
        return f"[웹 검색 실패: {str(e)}]"

def generate_counseling_response(user_input: str, user_mbti: str, recommended_song: str) -> str:
    mbti = user_mbti.upper()
    companion = MBTI_COMPATIBILITY_MAP.get(mbti)
    tone = MBTI_TONE.get(companion, "따뜻하고 진심 어린 말투입니다.")
    topics = detect_topics(user_input)

    expert_info = ""
    if "전문상담" in topics:
        expert_info = search_expert_knowledge(user_input)
        system_prompt = (
            f"당신은 MBTI {companion} 유형의 상담가입니다.\n"
            f"말투: {tone}\n"
            "심각도에 따라 1~3단계 중 판단하여 대응해주세요:\n"
            "- 1단계: 부드러운 공감\n- 2단계: 공식기관 언급 포함\n- 3단계: 즉각적 조치 유도 + 기관 안내 포함\n"
            f"\n※ 참고 정보:\n{expert_info[:1000]}"
        )
    else:
        topic_str = ", ".join(topics)
        topic_guidance = "\n".join([f"- {t}에 대한 공감을 포함해주세요." for t in topics])
        system_prompt = (
            f"당신은 MBTI {companion} 유형의 상담가입니다.\n"
            f"말투: {tone}\n"
            f"고민 주제: {topic_str}\n"
            f"{topic_guidance}\n"
            f"감정을 2~4개 키워드로 정리해 주세요.\n"
            f"[추천 음악: {recommended_song}]"
        )

    user_prompt = f'고민 내용: "{user_input}"\nMBTI: {mbti}'

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=700
    )
    return response.choices[0].message.content.strip()

def summarize_counseling_response(response_text: str) -> str:
    system_prompt = (
        "당신은 섬세하고 따뜻한 심리 상담가입니다.\n"
        "다음 텍스트를 읽고 감정 키워드와 공감 문장으로 요약해주세요.\n"
        "말투는 진심 어린 존댓말로 작성해주세요."
    )
    user_prompt = f"상담 응답 내용:\n{response_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6,
        max_tokens=500
    )
    return response.choices[0].message["content"].strip()
