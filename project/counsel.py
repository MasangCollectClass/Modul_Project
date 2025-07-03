import openai
import requests
import json
from datetime import datetime
from typing import List, Dict

# OpenAI 및 SerpAPI 키 설정
openai.api_key = "YOUR_OPENAI_API_KEY"
serpapi_key = "YOUR_SERPAPI_KEY"

# 대화 이력 및 감정 로그 초기화
chat_history: List[Dict[str, str]] = []
emotion_log: List[List[str]] = []

# 유효한 MBTI 목록
VALID_MBTI_TYPES = {
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
}

# MBTI 유형별 말투 설명
MBTI_TONE = {
    "ISTJ": "신중하고 책임감 있는 말투입니다.",
    "ISFJ": "배려 깊고 따뜻한 말투입니다.",
    "INFJ": "차분하고 통찰력 있는 말투입니다.",
    "INTJ": "분석적이고 간결한 말투입니다.",
    "ISTP": "간단명료하고 실용적인 말투입니다.",
    "ISFP": "조용하고 감성적인 말투입니다.",
    "INFP": "섬세하고 감정에 공감하는 말투입니다.",
    "INTP": "논리적이고 객관적인 말투입니다.",
    "ESTP": "직설적이고 현실적인 말투입니다.",
    "ESFP": "활기차고 친근한 말투입니다.",
    "ENFP": "감정 풍부하고 창의적인 말투입니다.",
    "ENTP": "재치 있고 논리적인 말투입니다.",
    "ESTJ": "확신 있고 구조적인 말투입니다.",
    "ESFJ": "상냥하고 배려 깊은 말투입니다.",
    "ENFJ": "공감 능력 뛰어난 따뜻한 말투입니다.",
    "ENTJ": "목표 지향적이고 단호한 말투입니다."
}

# MBTI 궁합 추천 매핑
MBTI_COMPATIBILITY_MAP = {
    "ISTJ": "ESFP", "ISFJ": "ENFP", "INFJ": "ENFP", "INTJ": "ENFP",
    "ISTP": "ESFJ", "ISFP": "ENFJ", "INFP": "ENFJ", "INTP": "ENTP",
    "ESTP": "ISFJ", "ESFP": "ISFJ", "ENFP": "INFJ", "ENTP": "INFJ",
    "ESTJ": "ISFP", "ESFJ": "ISFP", "ENFJ": "INFP", "ENTJ": "INTP"
}

# 감정 키워드 목록
BASIC_EMOTION_KEYWORDS = {
    "슬픔": ["슬퍼", "속상해", "눈물", "울고 싶어", "허전해", "상실감", "우울", "비참해", "허무해"],
    "불안": ["불안", "초조", "걱정", "긴장돼", "두려워", "조마조마", "위태로워", "불편해"],
    "화남": ["화나", "짜증", "분노", "억울해", "열받아", "성질나", "기분 나빠"],
    "무기력": ["지쳐", "무기력", "의욕 없어", "아무것도 하기 싫어", "기운 없어", "버겁다"],
    "외로움": ["외로워", "고독", "소외감", "혼자", "텅 빈", "마음이 비어"],
    "혼란": ["혼란", "헷갈려", "복잡해", "갈피 못 잡아", "정리가 안 돼"],
    "죄책감": ["미안해", "후회", "자책", "내 탓", "잘못했어", "부끄러워"],
    "자존감 저하": ["자신 없어", "열등감", "무가치해", "존재감 없어", "비교돼", "나는 안 돼"],
    "불만": ["불공평해", "억지 같아", "차별 받은 느낌", "나만 손해보는 기분"],
    "기쁨": ["기뻐", "좋아", "행복해", "웃음", "즐거워", "만족스러워", "뿌듯해", "신나", "행복하다"],
    "설렘": ["설레", "기대돼", "두근두근", "좋은 예감", "가슴이 뛰어", "떨리는데 좋아"],
    "감사": ["고마워", "감사해", "덕분에", "다행이야", "배려에 감동했어"],
    "안정감": ["편안해", "마음이 놓여", "안정돼", "차분해", "따뜻해", "평온해"]
}

# 감정별 기본 응답 템플릿
EMOTION_TEMPLATES = {
    "슬픔": "그 마음, 정말 힘드셨을 것 같아요. 충분히 슬퍼하셔도 괜찮아요.",
    "불안": "지금 마음이 많이 흔들리시나봐요. 불안한 감정은 누구에게나 찾아와요.",
    "화남": "마음속에 쌓인 감정이 많이 억눌렸을지도 모르겠어요. 분노도 자연스러운 감정이에요.",
    "무기력": "기운이 나지 않는 시기에는, 잠깐 멈춰서 숨 고르기가 필요해요.",
    "외로움": "혼자라고 느껴질 땐, 그 감정을 들어주는 것만으로도 큰 위로가 되곤 해요.",
    "혼란": "생각이 너무 많으면 마음이 무거울 수 있어요. 천천히 정리해봐도 괜찮아요.",
    "죄책감": "그렇게 느끼는 당신은 이미 충분히 따뜻한 사람이에요.",
    "자존감 저하": "당신은 존재 자체로 소중해요. 그 마음을 외면하지 않을게요.",
    "불만": "그럴 수 있어요. 억울함과 불편함은 정당한 감정이에요.",
    "기쁨": "그 기쁜 마음이 계속 이어졌으면 좋겠어요. 당신의 웃음은 정말 소중해요.",
    "설렘": "설레는 마음이 느껴지네요. 그 감정에 솔직해지는 순간들이 너무 좋아요.",
    "감사": "그 고마움을 표현해줘서 정말 따뜻하게 느껴져요.",
    "안정감": "지금처럼 편안하고 안정된 상태가 계속되길 바랄게요."
}

# 특정 감정 조합에 대한 공감 응답 템플릿
COMBINED_EMOTION_TEMPLATES = {
    ("기쁨", "슬픔"): "기쁜 순간인데도 마음 어딘가에 슬픔이 함께 있다는 건, 그 기쁨이 얼마나 소중한지를 보여줘요.",
    ("설렘", "불안"): "설레는 기대감과 함께 불안도 찾아오는 건 아주 자연스러운 일이에요.",
    ("감사", "죄책감"): "감사함 속에 죄책감이 섞여 있다면, 마음이 깊고 따뜻한 사람이란 뜻이에요."
}

# 사용자가 입력한 MBTI가 유효한지 확인
def is_valid_mbti(mbti: str) -> bool:
    return mbti.strip().upper() in VALID_MBTI_TYPES

# MBTI 유형에 따른 말투를 반환
def get_mbti_tone(mbti: str) -> str:
    mbti = mbti.strip().upper()
    return MBTI_TONE.get(mbti, "중립적이고 차분한 말투로 응답합니다.")

# MBTI 유형에 맞는 궁합형을 반환
def get_compatible_mbti(mbti: str) -> str:
    mbti = mbti.strip().upper()
    return MBTI_COMPATIBILITY_MAP.get(mbti, "ISFJ")

# MBTI의 T/F 성향을 추출
def get_tf_trait(mbti: str) -> str:
    mbti = mbti.strip().upper()
    if len(mbti) >= 3 and mbti[2] == "F":
        return "F"
    else:
        return "T"

# 감정 조합 또는 개별 감정에 따른 공감 문구를 응답에 삽입
def insert_emotion_templates(response: str, emotions: List[str]) -> str:
    if not emotions:
        return response

    top2 = tuple(sorted(emotions[:2]))
    combined = COMBINED_EMOTION_TEMPLATES.get(top2)
    if combined:
        return combined + "\n\n" + response

    templates = []
    for e in emotions[:2]:
        template = EMOTION_TEMPLATES.get(e)
        if template:
            templates.append(template)
        else:
            templates.append(f"그 감정 '{e}'도 충분히 이해해요.")

    return "\n".join(templates) + "\n\n" + response

# 특정 감정에 따라 말투나 응답 스타일을 보정
def adjust_style_by_emotion(response: str, emotions: List[str]) -> str:
    if not emotions:
        return response
    core = emotions[0]
    if core in ["불안", "무기력", "혼란", "자존감 저하"]:
        return response[:300]
    elif core in ["기쁨", "감사", "설렘"]:
        return response + "\n\n지금 그 감정, 충분히 누릴 자격이 있어요."
    elif core in ["화남", "불만"]:
        return "지금 그 감정, 충분히 그럴 수 있어요.\n\n" + response
    else:
        return response

# 대화 이력에서 주요 감정 흐름을 요약 (빈도 기준)
def summarize_emotion_flow(log: List[List[str]]) -> str:
    from collections import Counter
    flat = [e for group in log for e in group]
    if not flat:
        return ""
    count = Counter(flat).most_common(2)
    return "최근 주요 감정: " + ", ".join([f"{e}({n}회)" for e, n in count])

# 감정 키워드를 기준으로 사용자 입력에서 감정 분류
def extract_emotions(user_input: str) -> List[str]:
    detected = []
    for emotion, keywords in BASIC_EMOTION_KEYWORDS.items():
        if any(k in user_input for k in keywords):
            detected.append(emotion)
    return detected

# GPT-3.5 기반 상담 응답 생성 함수
def generate_counseling_response(user_input: str, mbti: str, topic: str, emotions: List[str]) -> str:
    tone = get_mbti_tone(mbti)
    tf = get_tf_trait(mbti)
    compatible = get_compatible_mbti(mbti)

    system_prompt = (
        f"당신은 {mbti} 유형의 말투와 {tf} 성향을 지닌 심리상담 챗봇입니다. "
        "정서 공감을 중심으로 따뜻하게 반응해주세요. 텍스트에 이모티콘이나 해시태그는 포함하지 말고, "
        "너무 공식적이거나 어색한 문체는 피해주세요."
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages += [{"role": m["role"], "content": m["content"]} for m in compress_history(chat_history)]
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6,
            max_tokens=600
        )
        content = response.choices[0].message["content"].strip()
        response_with_template = insert_emotion_templates(content, emotions)
        styled_response = adjust_style_by_emotion(response_with_template, emotions)

        if len(chat_history) >= 10:
            summary = summarize_emotion_flow(emotion_log)
            if summary:
                styled_response += "\n\n" + summary

        return styled_response

    except Exception:
        return "죄송해요. 상담 응답을 생성하는 데 문제가 발생했어요."

# 사용자의 요청이 정보요청인지 감정상담인지 구분
def detect_intent(user_input: str) -> str:
    info_keywords = ["알려줘", "무엇", "이유", "정의", "정보", "검색", "어떻게", "예시", "란", "vs", "비교"]
    return "정보요청" if any(k in user_input for k in info_keywords) else "감정상담"

# 전문 상담, 진로 상담 등 주제 분류를 키워드로 분석
def detect_topic(user_input: str) -> str:
    COUNSELING_TOPICS = {
        "전문상담": ["우울증", "불안장애", "ADHD", "자살", "조현병", "PTSD", "공황", "트라우마", "자해", "강박"],
        "진로상담": ["진로", "이직", "적성", "전공", "진학", "퇴사", "커리어", "취업"],
        "관계상담": ["연애", "이별", "가족", "친구", "직장", "대인기피", "갈등", "짝사랑", "의사소통"],
        "자기이해": ["자존감", "자기혐오", "무기력", "감정기복", "혼란", "자기통제", "의욕 없음", "불안정"],
        "정체성상담": ["정체성", "삶의 의미", "목표 상실", "자기탐색", "존재감", "방황", "가치관"],
        "학업상담": ["공부", "시험", "수능", "졸업", "논문", "성적", "학습", "집중력"],
        "경제고민": ["돈", "월세", "지출", "부채", "용돈", "빚", "적금", "생활비", "알바"],
        "건강상담": ["불면증", "수면", "식사", "운동", "피로", "체력", "건강염려", "생활습관"]
    }

    for topic, keywords in COUNSELING_TOPICS.items():
        if any(k in user_input for k in keywords):
            return topic
    return "일반"

# 웹 검색 결과를 반환 (SerpAPI 사용)
def search_web(query: str) -> str:
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": serpapi_key,
        "engine": "google",
        "hl": "ko",
        "gl": "kr"
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        results = data.get("organic_results", [])
        if results:
            snippet = results[0].get("snippet") or results[0].get("title")
            return snippet if snippet else "검색 결과 요약을 찾을 수 없었어요."
        else:
            return "검색 결과가 없습니다."
    except Exception:
        return "웹 검색 중 문제가 발생했어요."

# 감정 기반 또는 키워드 기반 음악 검색
def search_music(query: str) -> str:
    return search_web(query + " 음악 추천")

# 웹 검색 기반 정보요청 응답 생성
def generate_information_response(user_input: str) -> str:
    topic = detect_topic(user_input)
    if topic == "전문상담":
        web_result = search_web(user_input)
        return f"{web_result}\n\n전문적인 도움이 필요하다면 상담센터나 정신건강의학과에 문의해보는 것도 권장돼요."

    web_result = search_web(user_input)
    if "검색 결과" in web_result or "문제" in web_result:
        try:
            system_prompt = (
                "당신은 친절하고 정확한 정보를 제공하는 챗봇입니다. "
                "질문에 대해 간결하게 요약하고, 불필요한 말은 하지 마세요."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.4,
                max_tokens=500
            )
            return response.choices[0].message["content"].strip()
        except Exception:
            return "정보 응답을 생성하는 데 문제가 발생했어요."
    else:
        return web_result

# 사용자 입력에 따라 상담 또는 정보 응답 생성
def process_user_input(user_input: str, mbti: str) -> str:
    intent = detect_intent(user_input)
    emotions = extract_emotions(user_input)
    if emotions:
        emotion_log.append(emotions)

    if intent == "정보요청":
        response = generate_information_response(user_input)
    else:
        topic = detect_topic(user_input)
        response = generate_counseling_response(user_input, mbti, topic, emotions)

    if len(response.strip()) < 20:
        if intent == "정보요청":
            response = generate_information_response(user_input)
        else:
            response = generate_counseling_response(user_input, mbti, topic, emotions)

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})
    return response

# 세션 로그를 JSON 파일로 저장
def save_session_log(mbti: str):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"session_{mbti}_{now}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "mbti": mbti,
            "chat_history": chat_history,
            "emotion_log": emotion_log
        }, f, ensure_ascii=False, indent=2)

# 상담 챗봇 메인 실행 루프
def start_counseling_session():
    print("[MBTI 상담 챗봇 시작]")
    while True:
        mbti = input("MBTI를 입력해주세요 (예: INFP): ").strip().upper()
        if is_valid_mbti(mbti):
            break
        print("올바른 MBTI 유형이 아닙니다.")
    print(f"\n{mbti} 유형으로 상담을 시작합니다. 종료하려면 '종료' 입력\n")

    while True:
        user_input = input("당신: ").strip()
        if user_input.lower() in ["종료", "exit", "quit"]:
            print("\n상담을 종료합니다. 감사합니다.")
            save_session_log(mbti)
            break
        bot_response = process_user_input(user_input, mbti)
        print(f"\n챗봇: {bot_response}\n")
