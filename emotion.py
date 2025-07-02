import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = None
try:
    client = OpenAI()
    print("OpenAI 클라이언트가 성공적으로 초기화되었습니다.")
    # (선택 사항) API 연결 확인을 위한 간단한 테스트:
    # models_response = client.models.list()
    # print(f"API 연결 확인. 사용 가능한 모델 예시: {[m.id for m in models_response.data[:3]]}")
except Exception as e:
    print(f"오류: OpenAI 클라이언트 초기화 실패.")
    print(f"'.env' 파일에 'OPENAI_API_KEY'가 설정되었는지, 또는 키가 유효한지 확인해주세요.")
    print(f"자세한 오류 메시지: {e}") # 여기서 실제 오류 메시지를 출력하도록 수정
    print("이 오류가 발생하면 이후 감정 분석 기능이 정상 작동하지 않습니다.")

def analyze_sentiment(user_text: str) -> str:
    """
    사용자의 텍스트를 입력받아 GPT API를 통해 감정을 분석하고 반환하는 함수.
    이 함수는 OpenAP AI의 최신 ChatCompletion API를 사용합니다.

    Args:
        user_text (str): 분석할 사용자의 대화 텍스트.

    Returns:
        str: 분석된 감정 (예: '기쁨', '슬픔', '중립' 등).
             GPT가 정해진 감정 외 다른 것을 반환하거나, API 호출에 실패할 경우 '중립' 또는 '오류' 반환.
    """
    # OpenAI 클라이언트가 정상적으로 초기화되지 않았다면 감정 분석을 수행할 수 없습니다.
    if client is None:
        print("경고: OpenAI 클라이언트가 초기화되지 않아 감정 분석을 수행할 수 없습니다. API 키 설정을 확인해주세요.")
        return "오류" # API 키 문제로 인한 오류 시 '오류' 반환

    # --- GPT에게 보낼 메시지 (프롬프트 구성) ---
    # 이 리스트는 GPT에게 어떤 역할을 수행하고, 어떤 종류의 응답을 기대하는지 지시합니다.
    # 'role'은 메시지의 주체를 나타내며, 'content'는 실제 메시지 내용입니다.
    # Few-shot 예시는 'user'와 'assistant' 메시지 쌍으로 이루어집니다.
    allowed_emotions = [
    # 🌞 긍정
    "기쁨","환희","유쾌","희열","만족","뿌듯함","감사","사랑","애정",
    "평온","안도","자신감","설렘","기대","존경","경외","흥분","열정","유머",
    # 🌧 부정
    "슬픔","우울","상실감","실망","좌절","후회","자책","외로움","분노","짜증",
    "혐오","경멸","두려움","공포","불안","초조","수치","부끄러움","피로","무기력","억울함",
    # 🌪 혼합·복합
    "혼란","갈등","당황","놀람","충격","호기심","의심","불신","그리움","향수",
    # 💤 기타
    "중립"
    ]

    # 기본 프롬프트 메시지 (few-shot 예시까지 포함)
    prompt_messages = [
        # 시스템 메시지: GPT의 역할 정의 (매우 중요!)
        # 답변 형식과 일치하도록 명확히 지시.
        {"role": "system", "content": f"너는 사용자의 감정을 분석하는 전문 심리 분석가야. 요청하는 문장에서 가장 지배적인 감정을 오직 다음 목록의 단어 중 하나로만 반환해야 해: {', '.join(allowed_emotions)}."},

        # 사용자 지시 메시지: GPT에게 명확한 요청 사항 전달 (단어 하나만!)
        {"role": "user", "content": "나는 너에게 사용자 문장을 제공할거야. 너는 그 문장에서 가장 강하게 드러나는 감정만을 위에 명시된 단어 중 하나로 오직 그 단어 자체만 출력해줘. 다른 불필요한 설명, 문장, 인사는 일절 포함하지 마."},

        # --- Few-shot 예시: GPT가 감정을 정확히 이해하도록 돕는 중요한 부분 ---
        # 실제 사용자 문장과 예상되는 감정 답변을 제공하여 GPT의 학습을 돕습니다.
        # 다양한 감정과 표현에 대한 예시를 추가/수정하면서 GPT의 답변을 테스트하고 개선하세요.
        {"role": "user", "content": "사용자 문장: '오늘 정말 기분이 최고야!'"},
        {"role": "assistant", "content": "기쁨"},
        {"role": "user", "content": "사용자 문장: '정말 눈물이 날 만큼 행복해!'"},
        {"role": "assistant", "content": "환희"},
        {"role": "user", "content": "사용자 문장: '캬~ 뿌듯하다!'"}, 
        {"role": "assistant", "content": "뿌듯함"},
        {"role": "user", "content": "사용자 문장: '덕분에 너무 고마워.'" },
        {"role": "assistant", "content": "감사"},
        {"role": "user", "content": "사용자 문장: '너 정말 사랑해.'" },
        {"role": "assistant", "content": "사랑"},
        {"role": "user", "content": "사용자 문장: '하루 종일 마음이 잔잔해.'" },
        {"role": "assistant", "content": "평온"},
        {"role": "user", "content": "사용자 문장: '휴… 드디어 끝났어!'"},
        {"role": "assistant", "content": "안도"},
        {"role": "user", "content": "사용자 문장: '할 수 있을 것 같아, 자신 있어!'"}, 
        {"role": "assistant", "content": "자신감"},
        {"role": "user", "content": "사용자 문장: '내일 여행이라 설렌다!'"}, 
        {"role": "assistant", "content": "설렘"},
        {"role": "user", "content": "사용자 문장: '열정이 불타오른다!'"}, 
        {"role": "assistant", "content": "열정"},
        {"role": "user", "content": "사용자 문장: '푸하하, 완전 웃겨!'"}, 
        {"role": "assistant", "content": "유머"},

        # 🌧 부정
        {"role": "user", "content": "사용자 문장: '왜 이렇게 눈물이 나지…'"}, 
        {"role": "assistant", "content": "슬픔"},
        {"role": "user", "content": "사용자 문장: '다 망했어, 실망이 크다.'" }, 
        {"role": "assistant", "content": "실망"},
        {"role": "user", "content": "사용자 문장: '아, 그때 그렇게 하지 말걸…'"}, 
        {"role": "assistant", "content": "후회"},
        {"role": "user", "content": "사용자 문장: '혼자 있는 게 너무 외로워.'" }, 
        {"role": "assistant", "content": "외로움"},
        {"role": "user", "content": "사용자 문장: '진짜 열 받네!'" }, 
        {"role": "assistant", "content": "분노"},
        {"role": "user", "content": "사용자 문장: '으… 정말 역겨워.'" }, 
        {"role": "assistant", "content": "혐오"},
        {"role": "user", "content": "사용자 문장: '심장이 벌렁, 무서워…'" }, 
        {"role": "assistant", "content": "두려움"},
        {"role": "user", "content": "사용자 문장: '계속 불안해서 잠이 안 와.'" }, 
        {"role": "assistant", "content": "불안"},
        {"role": "user", "content": "사용자 문장: '아… 창피해 죽겠다.'" }, 
        {"role": "assistant", "content": "수치"},
        {"role": "user", "content": "사용자 문장: '에휴, 완전히 녹초야.'" }, 
        {"role": "assistant", "content": "피로"},
        {"role": "user", "content": "사용자 문장: '억울해서 잠이 안 온다.'" }, 
        {"role": "assistant", "content": "억울함"},

        # 🌪 혼합·복합
        {"role": "user", "content": "사용자 문장: '머릿속이 복잡해, 뭐가 맞는 거지?'"}, 
        {"role": "assistant", "content": "혼란"},
        {"role": "user", "content": "사용자 문장: '갑자기 시켜서 완전 당황했어!'"}, 
        {"role": "assistant", "content": "당황"},
        {"role": "user", "content": "사용자 문장: '헉! 말도 안 돼!'"}, 
        {"role": "assistant", "content": "놀람"},
        {"role": "user", "content": "사용자 문장: '이건 왜 이럴까? 궁금하다.'" }, 
        {"role": "assistant", "content": "호기심"},
        {"role": "user", "content": "사용자 문장: '문득 고향 생각이 나네…'" }, 
        {"role": "assistant", "content": "그리움"},

        # 🌫 중립
        {"role": "user", "content": "사용자 문장: '오늘은 25°C였어.'" }, 
        {"role": "assistant", "content": "중립"},
    ]

    # 실제 분석 대상 문장을 prompt_messages 리스트에 추가 (매번 다르게)
    prompt_messages.append({"role": "user", "content": f"사용자 문장: '{user_text}'"})

    # 사용할 GPT 모델 선택:
    # "gpt-3.5-turbo": 빠르고 비용 효율적. 대부분의 경우 감정 분석에 충분합니다.
    # "gpt-4": 더 높은 정확도를 제공하지만, 느리고 API 호출 비용이 더 많이 발생합니다.
    model_to_use = "gpt-4" 

    # 응답의 창의성 조절:
    # 0.0에 가까울수록 일관적이고 반복적인 응답을 생성합니다.
    # 1.0에 가까울수록 더 다양하고 창의적인 응답을 생성합니다.
    # 감정 분석은 일관성이 중요하므로 낮은 값(0.0~0.2)을 설정하는 것이 좋습니다.
    temperature = 0.0 # <--- 0.0으로 하여 GPT가 지시를 가장 엄격하게 따르도록 함.

    # 응답으로 받을 최대 토큰 수:
    # GPT의 응답 길이를 제한합니다. 감정 단어 하나만 받을 것이므로 최소한으로 설정합니다.
    max_tokens = 5 # <--- 최소 토큰으로만 단어 하나만 생성하도록 제한.

    try:
        # GPT API를 호출하여 ChatCompletion 생성
        response = client.chat.completions.create(
            model=model_to_use,
            messages=prompt_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # GPT 응답에서 텍스트(감정 단어) 추출 및 앞뒤 공백 제거
        sentiment = response.choices[0].message.content.strip()

        # GPT가 우리가 정의한 감정 목록 외의 다른 단어를 반환할 경우 처리
        # 이는 GPT가 프롬프트 지시를 따르지 않는 예외적인 경우에 대비합니다.
        if sentiment in allowed_emotions:
            return sentiment
        else:
            print(f"경고: GPT가 예상치 못한 감정 '{sentiment}'을(를) 반환했습니다. '중립'으로 처리합니다.") # 어떤 감정인지 출력
            return "중립"

    except Exception as e:
        # API 통신 오류, 네트워크 문제 등 다양한 예외 상황 처리
        print(f"감정 분석 중 GPT API 호출 오류 발생: {e}") # 실제 오류 메시지를 출력하도록 수정
        # 오류 발생 시 기본 감성인 '중립'을 반환하여 프로그램이 멈추지 않게 합니다.
        return "중립"

if __name__ == '__main__':
    print("--- MBTI 상담 챗봇 단일 감정 분석 시작 ---")
    
    user_input = input("\n당신의 대화를 입력해주세요: ")
    
    print(f"\n[챗봇 분석 중...]")
    
    # 1. 사용자의 대화에서 감정 분석
    detected_emotion = analyze_sentiment(user_input)
    print(f"    > 분석된 감정: {detected_emotion}") # 여기서 실제 분석된 감정을 출력하도록 수정
    print("-" * 50) # 구분선 추가
    
    print("감정 분석이 완료되었습니다. 프로그램을 종료합니다.")