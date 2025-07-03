# Modul_Project
GPT 기반 MBTI 예측 및 감정 분석을 활용한 AI 상담 챗봇 웹 애플리케이션.  
Streamlit을 기반으로 한 프론트엔드와 백엔드 통합 구조로 구성되어 있으며, 사용자 입력을 통해 MBTI를 예측하고 감정 상태를 분석한 뒤, 적절한 상담 메시지를 제공

---

```
## 디렉터리 구조

Modul_Project/
├── .gitignore # Git 추적 제외 항목
├── .streamlit/ # Streamlit 설정 파일
├── .venv/ # 가상환경 폴더
├── README.md # 프로젝트 설명 파일
├── module.ipynb # 분석 및 실험용 모듈
├── requirements.txt # 루트 의존성 파일
│
├── project/ # 메인 프로젝트 폴더
│ ├── pycache/ # 파이썬 캐시
│ ├── agent.py # GPT 기반 상담 에이전트 로직
│ ├── mbti_predictor.py # MBTI 예측 모델 로직
│ ├── counsel.py # 상담 응답 생성 기능
│ ├── emotion.py # 감정 분석 기능
│ ├── cards.py # UI 카드 컴포넌트 (구버전)
│ ├── cards2.py # UI 카드 컴포넌트 (최신)
│ ├── home.py # 홈 화면 구성
│ ├── streamlit_app.py # 메인 Streamlit 앱 진입점
│ ├── requirements.txt # 프로젝트 전용 의존성 목록
│ │
│ ├── models/ # 학습된 MBTI 분류 모델 폴더
│ │ ├── ei_bilstm_model2.h5
│ │ ├── ns_bilstm_model2.h5
│ │ ├── tf_bilstm_model.h5
│ │ └── jp_bilstm_model.h5
│ │
│ ├── tokenizers/ # 토크나이저 파일 폴더
│ │ ├── ei_tokenizer2.pkl
│ │ ├── ns_tokenizer2.pkl
│ │ ├── tf_tokenizer.pkl
│ │ └── jp_tokenizer.pkl
│ │
│ ├── static/ # 정적 파일 (아이콘, CSS 등)
│ ├── images/ # 이미지 리소스
│ └── pages/ # Streamlit 페이지
│ ├── chat.py # 채팅 페이지
│ ├── mbti_list.py # MBTI 유형 설명 페이지
│ └── recommand.py # 콘텐츠 추천 페이지
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

1. 프로젝트 루트에 `.env` 파일을 생성하고 OpenAI API 키를 등록:
OPENAI_API_KEY=sk-...

2. 가상환경 실행 후, 필요한 라이브러리를 설치:
```bash
pip install -r project/requirements.txt
```

3. Streamlit 앱을 실행:
streamlit run project/streamlit_app.py
