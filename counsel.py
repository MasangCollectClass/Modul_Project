import os
import openai
from dotenv import load_dotenv
import pickle
import tensorflow as tf
from openai import OpenAI

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 사용자 MBTI별로 궁합이 잘 맞는 MBTI 유형 매핑
MBTI_COMPATIBILITY_MAP = {
    "INTP": "INFJ", "INFJ": "ENFP", "ENFP": "INTJ", "INTJ": "ENFP",
    "ISFJ": "ESTP", "ESTP": "ISFJ", "ISTJ": "ESFP", "ESFP": "ISTJ",
    "INFP": "ENFJ", "ENFJ": "INFP", "ISFP": "ENTJ", "ENTJ": "ISFP",
    "ENTP": "ISFJ", "ESFJ": "INTP", "ESTJ": "INFP", "ISTP": "ENFJ"
}

# 16가지 MBTI 유형에 따른 말투 스타일 정의
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

# 사용자의 고민 문장에서 다양한 표현을 감지할 수 있도록 키워드 세트를 풍부하게 정의

COUNSELING_TOPICS = {
    "전문상담": [
        "우울증", "공황장애", "불면증", "자해", "자살", "약물", "진단서", "정신병원", 
        "과호흡", "죽고 싶", "숨이 안 쉬어짐", "멍함", "감정이 없음"
    ],
    "관계상담": [
        "연애", "이별", "소개팅", "짝사랑", "밀당", "친구", "왕따", "소외감", 
        "가족", "형제", "부모님", "대화가 안 됨", "신뢰", "갈등", "혼자 된 느낌"
    ],
    "진로상담": [
        "진로", "이직", "퇴사", "퇴사하고 싶", "진학", "입시", "미래 직업", "커리어", 
        "회사 생활", "업무 적성", "일이 안 맞음", "성취감 없음"
    ],
    "학업상담": [
        "공부", "성적", "학점", "졸업", "과제", "수업 집중", "시험", 
        "지각", "휴학", "학교 스트레스", "학업 의욕 없음"
    ],
    "자기이해": [
        "자존감", "열등감", "자기혐오", "나는 왜 이럴까", "나 자신을 모르겠어", 
        "정체성", "나는 누구", "감정 기복", "감정이 들쭉날쭉", "자주 흔들림"
    ],
    "라이프스타일": [
        "생활 루틴", "새로운 취미", "휴가", "여행", "일상 변화", "생활 변화", 
        "운동 시작", "일상이 지루함", "뭘 하며 살아야 할지", "재미 없음"
    ],
    "경제고민": [
        "돈", "월세", "경제적 부담", "생활비", "대출", "통장 잔고", 
        "가난함", "물가", "알바", "재정 문제", "지출", "돈 걱정"
    ],
    "미래불안": [
        "미래가 막막", "불안감", "앞날", "계획이 없음", "불확실", 
        "뭐가 될지 모르겠어", "비전 없음", "나중에 어떻게 살아야 할지"
    ],
    "감정불안정": [
        "무기력", "감정 소모", "감정 기복", "멘탈 흔들림", "혼란스러움", 
        "내 마음도 모르겠음", "마음이 복잡", "집중 안 됨", "의욕 없음"
    ]
}

def detect_topics(user_input: str) -> list:
    """
    사용자의 입력 문장에서 상담 주제를 감지하여
    관련된 모든 주제를 리스트 형태로 반환합니다.
    """
    detected = []

    for topic, keywords in COUNSELING_TOPICS.items():
        for word in keywords:
            if word in user_input:
                detected.append(topic)
                break  # 하나의 주제에서 중복 감지 방지

    return list(set(detected)) or ["일반"]

def build_system_prompt(mbti: str, companion: str, tone: str, topics: list, recommended_song: str) -> str:
    """
    사용자의 MBTI와 관련된 상담 스타일을 기반으로,
    다중 상담 주제, 감정 분석, 시각화, 음악 추천을 포함한 GPT 프롬프트를 생성합니다.
    """
    # 주제 나열 (예: 진로상담, 감정불안정)
    topic_str = ", ".join(topics)

    # 주제별 조언 지시 블록
    topic_guidance = "\n".join([
        f"- [{t}]에 대한 공감 또는 조언을 포함해주세요."
        for t in topics if t != "일반"
    ]) or "- 고민에 대해 일반적인 공감과 조언을 포함해주세요."

    # 시스템 프롬프트 구성
    system_prompt = (
        f"당신은 MBTI {companion} 유형의 말투를 사용하는 상담가입니다.\n"
        f"말투 특징: {tone}\n\n"
        f"사용자의 MBTI는 {mbti}이며, 고민은 다음 주제와 관련 있습니다: {topic_str}.\n"
        f"각 주제에 해당하는 고민을 모두 반영하여 응답을 구성해주세요.\n\n"
        "상담 응답에는 다음 요소를 반드시 포함해야 합니다:\n"
        f"{topic_guidance}\n"
        "- 고민에서 감지된 감정 키워드를 2~4개 추출해주세요.\n"
        "- 그 감정을 시각적으로 표현한 이미지 설명을 생성해주세요.\n"
        f"- 마지막에 반드시 다음 문장을 그대로 포함하세요:\n[추천 음악: {recommended_song}]\n\n"
        "출력 예시:\n"
        "[공감 메시지]\n[감정 키워드: 무기력, 혼란, 외로움]\n[감정 시각화: 바람 없는 잿빛 바다 위에 떠 있는 작은 배]\n[추천 음악: ...]"
    )

    return system_prompt

def generate_counseling_response(user_input: str, user_mbti: str, recommended_song: str) -> str:
    """
    사용자의 MBTI, 고민 내용, 음악 추천 결과를 기반으로
    감정 분석, 다중 주제 반영, 위기 레벨 감지를 포함하는 상담 응답을 생성합니다.
    """
    mbti = user_mbti.upper()
    companion = MBTI_COMPATIBILITY_MAP.get(mbti)
    tone = MBTI_TONE.get(companion, "따뜻하고 진심 어린 말투입니다.")
    topics = detect_topics(user_input)

    # 전문상담 주제 포함 여부
    has_critical_topic = "전문상담" in topics

    # GPT용 시스템 프롬프트 구성 (전문상담 여부에 따라 분기)
    if has_critical_topic:
        system_prompt = (
            f"당신은 MBTI {companion} 유형의 말투로 공감하는 상담가입니다.\n"
            f"말투 특징: {tone}\n\n"
            "사용자의 고민은 심리적으로 민감할 수 있으니, 아래 지시에 따라 응답을 생성해주세요:\n"
            "1. 먼저, 고민의 심각도를 3단계(정서 피로 / 증상화 경향 / 고위험 신호) 중 하나로 판단하세요.\n"
            "2. 단계에 따라 다음을 수행해주세요:\n"
            "   - 1단계: 부드러운 공감 + 감정 키워드 + 시각화 + 음악 추천 포함\n"
            "   - 2단계: 따뜻한 조언과 감정 정리 + 공식 기관의 조언 요약 + 음악 포함\n"
            "   - 3단계: 즉각적인 공감 + 신뢰할 기관 안내 요청 멘트 포함 + 감정 요약 + 음악 포함\n"
            "3. 감정 시각화 표현은 반드시 포함해주세요\n"
            f"4. 마지막 줄에 다음 문장을 그대로 사용하세요:\n[추천 음악: {recommended_song}]"
        )
    else:
        topic_str = ", ".join(topics)
        topic_guidance = "\n".join([
            f"- [{t}] 주제를 반영한 공감 또는 조언을 포함해주세요."
            for t in topics if t != "일반"
        ]) or "- 일반적인 정서적 공감을 전해주세요."

        system_prompt = (
            f"당신은 MBTI {companion} 유형의 말투로 공감하는 상담가입니다.\n"
            f"말투 특징: {tone}\n\n"
            f"사용자의 고민 주제: {topic_str}\n"
            "다음 항목을 포함해 응답을 구성해주세요:\n"
            f"{topic_guidance}\n"
            "- 고민에 담긴 감정을 2~4개의 키워드로 정리해주세요.\n"
            "- 감정을 은유적으로 표현한 시각 이미지 설명을 추가해주세요.\n"
            f"- 마지막 줄에 다음 문장을 그대로 사용하세요:\n[추천 음악: {recommended_song}]\n\n"
            "출력 예시:\n"
            "[공감 메시지]\n[감정 키워드: 불안, 무기력, 우울]\n[감정 시각화: 새벽 안개 속에 홀로 선 가로등 아래 실루엣]\n[추천 음악: ...]"
        )

    # 사용자 프롬프트
    user_prompt = f'고민 내용: "{user_input}"\n사용자 MBTI: {mbti}'

    # GPT 호출
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
    """
    목적:
    사용자가 받은 상담 응답 텍스트를 기반으로,
    오늘의 감정 상태를 요약 정리하는 리포트를 생성합니다.

    출력에는 다음 요소가 포함됩니다:
    1. 감정 키워드 (예: 불안, 피로, 외로움)
    2. 감정을 비유적으로 표현한 이미지 설명 요약
    3. 응답에서 가장 마음에 닿았을 공감 문장 또는 조언
    4. 전체적인 감정 분위기를 표현한 '감정 날씨 요약'

    스타일:
    - 말투는 친근하고 조용하며 위로를 전하는 느낌
    - 상담 마무리에 스스로를 되돌아볼 수 있도록 따뜻하게 표현

    프롬프트 구조:
    - 시스템 메시지: 출력 항목 설명 및 문체 안내
    - 사용자 메시지: 실제 상담 응답 텍스트 입력

    매개변수:
    - response_text (str): 이전에 생성된 GPT 상담 응답 전체 텍스트

    반환값:
    - str: GPT가 생성한 감정 리포트 텍스트 (이모지 없음)
    """

    # GPT에게 전달할 시스템 프롬프트: 출력 항목과 말투 지시
    system_prompt = (
        "당신은 섬세하고 따뜻한 심리 상담가입니다.\n"
        "아래 상담 응답 텍스트를 읽고, 사용자의 감정 상태를 부드럽게 요약해주세요.\n\n"
        "출력에는 다음 내용을 포함해주세요:\n"
        "1. 사용자의 주된 감정 키워드 (2~4개)\n"
        "2. 감정 시각화 이미지 설명 요약\n"
        "3. 응답에서 가장 따뜻한 공감 문장 또는 조언 하나 선택\n"
        "4. 전체 감정 분위기를 정리한 오늘의 감정 날씨 (텍스트만, 이모지 없이)\n\n"
        "말투는 진심이 느껴지는 다정하고 위로하는 말투로 작성해주세요. 존댓말로 표현해주세요."
    )

    # 사용자 프롬프트: 상담 응답 본문을 GPT에게 입력으로 전달
    user_prompt = f"상담 응답 내용:\n{response_text}"

    # GPT 호출: 감정 리포트 요청
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6,
        max_tokens=500
    )

    # 결과 응답 텍스트 반환
    return response.choices[0].message["content"].strip()

