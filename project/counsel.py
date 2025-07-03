# 상담 챗봇 핵심 코드 정리
import openai
import os
from dotenv import load_dotenv
from typing import List, Tuple, Dict
from datetime import datetime
import json
from openai import OpenAI

# .env에서 OpenAI API 키 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 전역 상태
chat_history: List[Dict[str, str]] = []
emotion_log: List[List[str]] = []

# 유효한 MBTI 목록
VALID_MBTI_TYPES = {
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
}

# MBTI 관련 매핑
MBTI_TONE = { 
  "ENFP": "따뜻하고 유쾌하며 이모티콘을 자주 사용합니다.",
    "ISTJ": "분석적이고 신중하며 단정한 말투입니다.",
    "INFP": "섬세하고 감정에 공감하는 부드러운 말투입니다.",
    "ESTJ": "단호하고 체계적이며 사실 위주의 말투입니다.",
    "INTP": "논리적이고 중립적인 말투입니다.",
    "ESFJ": "친근하고 배려심 많은 말투로 위로를 잘 전합니다.",
    "ENTP": "재치 있고 유머러스하며 아이디어를 자유롭게 표현합니다.",
    "ISFJ": "조용하지만 따뜻하고 배려 깊은 말투로 상대를 존중합니다.",
    "INFJ": "직관적이며 깊이 있는 표현과 따뜻한 공감이 어우러진 말투입니다.",
    "ESTP": "직설적이고 에너지 넘치며 상황 중심적으로 조언합니다.",
    "ISFP": "차분하고 부드러우며 감정에 민감하게 반응합니다.",
    "INTJ": "간결하고 직관적인 말투이며 효율 중심적으로 접근합니다.",
    "ENTJ": "자신감 있고 목표 지향적이며 명확한 표현을 사용합니다.",
    "ENFJ": "따뜻하고 포용적인 말투로 감정에 깊이 공감합니다.",
    "ISTP": "과묵하고 실용적인 조언 위주로 핵심만 전달합니다.",
    "ESFP": "밝고 생동감 있는 말투로 친근하고 즉흥적인 표현을 자주 사용합니다."
}
MBTI_COMPATIBILITY_MAP = {
    "ISTJ": "ISFJ", "ISFJ": "ISTJ",
    "INFJ": "ENFP", "INTJ": "ENFP",
    "ISTP": "ESTP", "ISFP": "ESFP",
    "INFP": "ENFJ", "INTP": "ENTP",
    "ESTP": "ISFP", "ESFP": "ISFP",
    "ENFP": "INFJ", "ENTP": "INFJ",
    "ESTJ": "ESFJ", "ESFJ": "ISFJ",
    "ENFJ": "INFP", "ENTJ": "INTP"
}

# 감정 키워드 사전
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

# 상담 주제 키워드 분류
COUNSELING_TOPICS = {    "전문상담": [
        "우울증", "불안장애", "강박", "자살", "자해", "조현병", "PTSD", "공황장애", "ADHD", "트라우마"
    ],
    "진로상담": [
        "진로", "취업", "이직", "적성", "전공", "진학", "퇴사", "커리어", "포트폴리오"
    ],
    "관계상담": [
        "연애", "이별", "짝사랑", "가족", "친구", "의사소통", "직장 상사", "대인기피", "외로움", "갈등"
    ],
    "자기이해": [
        "자존감", "감정기복", "무기력", "자기혐오", "혼란", "의욕 없음", "자기통제", "완벽주의", "불안정함"
    ],
    "학업상담": [
        "공부", "성적", "시험", "수능", "집중력", "학습법", "학원", "졸업", "학점", "논문"
    ],
    "경제고민": [
        "돈", "월세", "지출", "부채", "알바", "생활비", "소비습관", "빚", "용돈", "적금"
    ],
    "건강상담": [
        "불면증", "수면", "식사", "운동", "피로", "체력", "건강염려", "생활습관"
    ],
    "정체성상담": [
        "정체성", "삶의 의미", "자기탐색", "존재감", "목표 상실", "방황", "가치관", "자기이해"
    ]
}

# 감정 템플릿
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
COMBINED_EMOTION_TEMPLATES = {
    ("기쁨", "슬픔"): (
        "기쁜 순간인데도 마음 어딘가에 슬픔이 함께 있다는 건, 그 기쁨이 얼마나 소중한지를 보여줘요. "
        "두 감정 모두 당신 안에서 자연스럽게 공존할 수 있어요."
    ),
    ("설렘", "불안"): (
        "설레는 기대감과 함께 불안도 찾아오는 건 아주 자연스러운 일이에요. "
        "당신이 지금 진심으로 무언가를 마주하고 있다는 증거일지도 몰라요."
    ),
    ("감사", "죄책감"): (
        "감사함 속에 죄책감이 섞여 있다면, 마음이 깊고 따뜻한 사람이란 뜻이에요. "
        "스스로를 너무 몰아세우지 않아도 괜찮아요."
    )  
}

# 의도 분석
def detect_intent(user_input: str) -> str:
    info_keywords = ["알려줘", "정보", "무엇", "왜", "수치", "정리", "방법"]
    return "정보요청" if any(k in user_input for k in info_keywords) else "감정상담"

# 주제 분류 (키워드 + GPT 병합)
def classify_topic_nlp(user_input: str) -> str:
    system_prompt = "당신은 임상심리사이며, 사용자의 문장을 보고 적절한 상담 주제를 분류합니다."
    user_prompt = (
        f"다음 문장을 읽고 어떤 유형의 심리상담 주제에 해당하는지 한 단어로만 판단해주세요. "
        f"가능한 범주는 '전문상담', '진로상담', '관계상담', '자기이해', '학업상담', '경제고민', '건강상담', '정체성상담'입니다.\n\n"
        f"문장: {user_input}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=10
    )

    topic = response.choices[0].message["content"].strip().replace("'", "").replace("\"", "").replace(".", "")
    return topic if topic in COUNSELING_TOPICS else "일반"

def detect_topic(user_input: str) -> str:
    matched_topic = None
    keyword_matches = []

    # 키워드 기반 매칭 탐색
    for topic, keywords in COUNSELING_TOPICS.items():
        if any(k in user_input for k in keywords):
            keyword_matches.append(topic)

    if keyword_matches:
        # 동일 문장에서 여러 카테고리 키워드가 나올 경우 첫 번째 우선
        matched_topic = keyword_matches[0]

    # 키워드 기반 예측과 GPT 예측 병합
    gpt_topic = classify_topic_nlp(user_input)

    if matched_topic == gpt_topic:
        return matched_topic
    elif matched_topic and gpt_topic == "일반":
        return matched_topic
    elif gpt_topic and gpt_topic != "일반":
        return gpt_topic
    else:
        return matched_topic or "일반"

# 감정 추출
def extract_emotions_keywords(user_input: str) -> List[str]:
    detected = []
    for emotion, keywords in BASIC_EMOTION_KEYWORDS.items():
        if any(k in user_input for k in keywords):
            detected.append(emotion)
    return detected

def classify_emotions_nlp(user_input: str) -> List[str]:
    prompt = (
        "다음 문장에서 사용자가 표현한 감정을 분류해주세요. "
        "가능한 감정: 슬픔, 불안, 화남, 무기력, 외로움, 혼란, 죄책감, 자존감 저하, 불만, "
        "기쁨, 설렘, 감사, 안정감. 감정명만 콤마로 구분해서 출력해주세요.\n\n"
        f"문장: {user_input}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 감정 분석 전문가입니다. 감정명만 정확히 추출하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=60
        )
        content = response.choices[0].message["content"].strip()
        emotions = [e.strip() for e in content.replace("\n", ",").split(",")]
        return [e for e in emotions if e in BASIC_EMOTION_KEYWORDS]
    except Exception:
        return []

def extract_emotions(user_input: str) -> List[str]:
    emotions = classify_emotions_nlp(user_input)
    return emotions if emotions else extract_emotions_keywords(user_input)

# MBTI 유틸

def is_valid_mbti(mbti: str) -> bool:
    return mbti.upper() in VALID_MBTI_TYPES

def get_mbti_tone(mbti: str) -> str:
    mbti = mbti.strip().upper()
    if mbti not in VALID_MBTI_TYPES:
        return "중립적이고 차분한 말투로 응답합니다."  # fallback tone
    return MBTI_TONE[mbti]

def get_tf_trait(mbti: str) -> str:
    return "F" if len(mbti) >= 3 and mbti[2].upper() == "F" else "T"

def get_compatible_mbti(mbti: str) -> str:
    mbti = mbti.strip().upper()
    if mbti not in VALID_MBTI_TYPES:
        return "ISFJ"  # fallback match
    return MBTI_COMPATIBILITY_MAP.get(mbti, "ISFJ")

# 감정 삽입/스타일 조정

def insert_emotion_templates(response: str, emotions: List[str]) -> str:
    if not emotions:
        return response
    top2 = tuple(sorted(emotions[:2]))
    combined = COMBINED_EMOTION_TEMPLATES.get(top2)
    if combined:
        return combined + "\n\n" + response
    templates = [EMOTION_TEMPLATES[e] for e in emotions if e in EMOTION_TEMPLATES]
    return "\n".join(templates[:2]) + "\n\n" + response

def adjust_style_by_emotion(response: str, emotions: List[str]) -> str:
    if not emotions:
        return response

    core = emotions[0]

    if core in ["불안", "무기력", "혼란", "자존감 저하"]:
        # 짧고 안정적인 위로 중심
        return "\n".join(line.strip() for line in response.split("\n") if line.strip())[:300]
    elif core in ["기쁨", "감사", "설렘"]:
        # 밝고 따뜻한 말투 강조
        return response + "\n\n지금 그 감정, 충분히 누릴 자격이 있어요."
    elif core in ["화남", "불만"]:
        # 정당한 감정 인식 및 진정 어조
        return "지금 그 감정, 충분히 그럴 수 있어요.\n\n" + response
    else:
        return response

def summarize_emotion_flow(emotion_log: List[List[str]]) -> str:
    from collections import Counter
    flat = [e for group in emotion_log for e in group]
    count = Counter(flat)
    if not count:
        return ""
    common = count.most_common(2)
    trend = ", ".join([f"{e}({n}회)" for e, n in common])
    return f"최근 대화에서 주요 감정은 {trend}입니다."

# 응답 생성

def generate_counseling_response(user_input: str, mbti: str, topic: str, emotions: List[str]) -> str:
    tone = get_mbti_tone(mbti)
    tf = get_tf_trait(mbti)
    compatible = get_compatible_mbti(mbti)

    system_prompt = (
        f"당신은 {mbti} 유형의 말투와 {tf} 성향을 지닌 심리상담 챗봇입니다. "
        "정서 공감을 중심으로 따뜻하게 반응해주세요. 텍스트에 이모티콘이나 해시태그는 포함하지 말고, "
        "너무 공식적이거나 어색한 문체는 피해주세요."
    )

    # 대화 이력 압축
    full_history = compress_history(chat_history)

    messages = [{"role": "system", "content": system_prompt}]
    messages += [{"role": m["role"], "content": m["content"]} for m in full_history]
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6,
            max_tokens=600
        )
        content = response.choices[0].message["content"].strip()

        # 감정 템플릿 + 감정 스타일 조정
        response_with_template = insert_emotion_templates(content, emotions)
        styled_response = adjust_style_by_emotion(response_with_template, emotions)

        # 감정 흐름 요약 (선택적으로 출력)
        if len(chat_history) >= 10 and 'emotion_log' in globals():
            summary = summarize_emotion_flow(emotion_log)
            if summary:
                styled_response += f"\n\n🧾 {summary}"

        return styled_response

    except Exception:
        return "죄송해요. 상담 응답을 생성하는 데 문제가 발생했어요. 잠시 후 다시 시도해 주세요."

def detect_question_type(user_input: str) -> str:
    input_lower = user_input.lower()

    if any(kw in input_lower for kw in ["차이", "비교", "vs", "vs."]):
        return "비교"
    elif any(kw in input_lower for kw in ["예시", "예를", "같은", "사례"]):
        return "예시"
    elif any(kw in input_lower for kw in ["란", "란?", "이란", "무엇", "정의"]):
        return "정의"
    else:
        return "일반"

def generate_information_response(user_input: str) -> str:
    question_type = detect_question_type(user_input)

    system_prompt = (
        "당신은 친절하고 정확한 정보를 제공하는 AI입니다. "
        "사용자의 질문에 대해 핵심 개념을 쉽게 설명하고, 필요한 경우 항목별 리스트나 예시를 포함해주세요. "
        "정보는 명확하고 중립적이어야 하며, 불필요한 감정 표현이나 개인 의견은 포함하지 마세요."
    )

    # 질문 유형에 따라 안내 프롬프트 보조 문구 구성
    type_guidance = {
        "정의": "개념을 간단히 정의하고, 핵심 내용을 이해하기 쉽게 설명해주세요.",
        "비교": "두 개념 간의 차이점을 항목별로 비교해서 설명해주세요.",
        "예시": "해당 개념의 예시를 2개 이상 들어서 설명해주세요.",
        "일반": "핵심 정보를 중심으로 명료하고 정확하게 설명해주세요."
    }

    user_prompt = f"질문: {user_input}\n\n요청 유형: {question_type}\n{type_guidance[question_type]}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.4,
            max_tokens=500
        )

        content = response.choices[0].message["content"].strip()
        return content if content else "요청하신 정보를 찾지 못했어요. 다시 질문해주실 수 있을까요?"

    except Exception:
        return "죄송해요. 정보를 불러오는 데 문제가 생겼어요. 잠시 후 다시 시도해주세요."

# 입력 처리
def summarize_chat(turns: List[Dict[str, str]]) -> str:
    summary_prompt = (
        "다음은 사용자와 심리상담 챗봇 사이의 최근 대화입니다.\n"
        "이 대화를 요약하여 사용자가 어떤 고민을 하고 있었고 어떤 반응을 받았는지 간결히 정리해주세요.\n\n"
        f"{[msg['role'] + ': ' + msg['content'] for msg in turns]}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 대화를 요약하는 요약 전문가야."},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message["content"].strip()
    except Exception:
        return ""

def save_session_log(mbti: str):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"session_{mbti}_{now}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"mbti": mbti, "chat_history": chat_history, "emotion_log": emotion_log}, f, ensure_ascii=False, indent=2)

# 메인 처리 함수
def process_user_input(user_input: str, mbti: str) -> str:
    intent = detect_intent(user_input)
    topic = detect_topic(user_input) if intent == "감정상담" else None
    emotions = extract_emotions(user_input) if intent == "감정상담" else []
    if emotions:
        emotion_log.append(emotions)

    if intent == "정보요청":
        response = generate_information_response(user_input)
    else:
        response = generate_counseling_response(user_input, mbti, topic, emotions)

    if len(response) < 15 or "죄송해요" in response:
        response = generate_counseling_response(user_input, mbti, topic, emotions)

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})

    if len(chat_history) >= 6:
        print("\n[요약]", summarize_chat(chat_history[-6:]))

    return response

# 세션 실행
def start_counseling_session():
    print("[MBTI 상담 챗봇 시작]")
    while True:
        mbti_input = input("MBTI를 입력하세요: ").strip().upper()
        if is_valid_mbti(mbti_input): break
        print("올바른 MBTI가 아닙니다.")

    print(f"{mbti_input} 유형 상담 시작. 종료하려면 '종료' 입력")
    while True:
        user_input = input("당신: ").strip()
        if user_input.lower() in ["종료", "exit", "quit"]:
            print("상담 종료. 감사합니다.")
            save_session_log(mbti_input)
            break
        print("챗봇:", process_user_input(user_input, mbti_input))

# 실행
if __name__ == "__main__":
    start_counseling_session()