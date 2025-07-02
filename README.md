# Modul_Project

MBTI 예측, 감정 분석, GPT 상담을 통합한 스트림릿 기반 웹 애플리케이션입니다.  
FastAPI 백엔드와 연동되어 사용자와의 대화를 통해 성격유형과 감정을 분석하고,  
이에 기반한 맞춤형 상담 응답을 제공합니다.

---

## 📁 디렉터리 구조

Modul_Project/
│
├── .env # 환경변수 파일 (API 키 등)
├── .gitignore # Git 추적 제외 파일 목록
├── .streamlit/ # Streamlit 설정 파일
├── .venv/ # 가상환경 폴더
├── README.md # 프로젝트 설명 파일
├── module.ipynb # 개발/분석용 노트북
├── project/ # 메인 프로젝트 폴더
│ ├── pycache/ # 파이썬 캐시 파일
│ ├── agent.py # GPT 기반 챗봇 에이전트 로직
│ ├── cards.py # 스트림릿 UI 카드 구성 (이전 버전)
│ ├── cards2.py # 스트림릿 UI 카드 구성 (최신 버전)
│ ├── counsel.py # 상담 응답 생성 로직
│ ├── emotion.py # 감정 분석 기능
│ ├── home.py # 홈 화면 구성
│ ├── images/ # 이미지 리소스 폴더
│ ├── models/ # 학습된 MBTI 분류 모델 저장 폴더
│ │ └── (6개 모델 파일)
│ ├── pages/ # 스트림릿 페이지 구성 폴더
│ │ ├── chat.py # 채팅 페이지
│ │ ├── mbti_list.py # MBTI 유형별 설명 페이지
│ │ └── recommand.py # 콘텐츠 추천 페이지
│ ├── requirements.txt # 필요한 라이브러리 목록
│ ├── static/ # 정적 파일 (이미지, 아이콘 등)
│ │ └── (8개 파일)
│ ├── streamlit_app.py # 스트림릿 앱의 메인 진입점
│ └── tokenizers/ # 텍스트 전처리용 토크나이저 파일
│ └── (6개 파일)
└── requirements.txt # 루트에서도 종속성 관리 가능

---

## 실행 방법

1. 가상환경 활성화 (이미 `.venv`가 있다면):
   ```bash
   source .venv/Scripts/activate     # Windows 기준

2. 필요한 패키지 설치:
pip install -r project/requirements.txt

3. 환경변수 설정 (.env 파일에 OpenAI 키 등 포함)

4. 애플리케이션 실행:
streamlit run project/streamlit_app.py
