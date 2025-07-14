# Modul_Project
GPT 기반 MBTI 예측 및 감정 분석을 활용한 AI 상담 챗봇 웹 애플리케이션.  
Streamlit을 기반으로 한 프론트엔드와 백엔드 통합 구조로 구성되어 있으며, 사용자 입력을 통해 MBTI를 예측하고 감정 상태를 분석한 뒤, 적절한 상담 메시지를 제공

---

```
## 디렉터리 구조

Modul_Project_1/
├── .streamlit/                # Streamlit 앱 설정 디렉토리
├── .venv/                     # 가상 환경 디렉토리
├── images/                    # 이미지 파일 저장 디렉토리
├── project/                   # 프로젝트 메인 디렉토리
│   ├── database/              # 데이터베이스 관련 파일
│   ├── images/                # 이미지 파일 저장 디렉토리
│   ├── models/                # 학습된 모델 파일들
│   ├── static/                # 정적 파일들
│   ├── tokenizers/            # 토크나이저 파일들
│   ├── cards.py               # 카드 UI 컴포넌트
│   ├── chat.py                # 채팅 기능 구현
│   ├── counsel.py             # 상담 관련 기능
│   ├── emotion.py             # 감정 분석 기능
│   ├── home.py                # 홈 페이지 구현
│   ├── mbti_counsel_agent.py  # MBTI 상담 에이전트
│   ├── mbti_list.py           # MBTI 유형 관련 데이터
│   ├── mbti_predictor.py      # MBTI 예측 모델
│   ├── music.py               # 음악 추천 기능
│   ├── recommand.py           # 추천 시스템
│   ├── requirements.txt       # 필요한 파이썬 패키지 목록
│   ├── streamlit_app.py       # Streamlit 메인 애플리케이션
│   └── travel.py              # 여행지 추천 기능
├── static/                    # 정적 파일 (폰트 등)
│   ├── OFL-SpaceGrotesk.txt
│   ├── OFL-SpaceMono.txt
│   ├── SpaceGrotesk-SemiBold.ttf
│   ├── SpaceGrotesk-VariableFont_wght.ttf
│   ├── SpaceMono-Bold.ttf
│   ├── SpaceMono-BoldItalic.ttf
│   ├── SpaceMono-Italic.ttf
│   └── SpaceMono-Regular.ttf
├── mbti_places.txt            # MBTI별 추천 여행지 데이터
├── mbti_prompt.txt            # MBTI 프롬프트 데이터
└── README.md                  # 프로젝트 설명 문서 
```

---

## 주요 기능
- MBTI 4지표 기반 분류기로 사용자 텍스트 입력에 대한 성격유형 예측
- 감정 분석 모델을 통해 긍정/부정 상태 분석
- GPT 상담 시스템을 이용한 맞춤형 대화 응답 생성
- Streamlit 기반의 직관적인 웹 UI 제공
- 여러 Streamlit 페이지 간 네비게이션 지원

---

## 실행 방법

1. 프로젝트 루트에 `.env` 파일을 생성하고 OpenAI API, SERPAPI_API, YOUTUBE_API키를 등록:
OPENAI_API_KEY=sk-...

2. 가상환경 실행 후, 필요한 라이브러리를 설치:
```bash
pip install -r project/requirements.txt
```

3. Streamlit 앱을 실행:
streamlit run project/streamlit_app.py

### figma 참조
### https://www.figma.com/design/2aXOLMNtFIh5rVlBxD4PSV/%EB%A7%88%EC%83%81-%EC%88%98%EA%B1%B0%EB%B0%98?node-id=0-1&p=f&t=pCGQzfuZ9iokkRza-0

