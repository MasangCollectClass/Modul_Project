import streamlit as st

# 사이드메뉴 하단과 홈화면에 표시되는 작은 미리보기 칸 입니다.


# 채팅
def chat_card():
    st.page_link("chat.py", label="Chat", icon=":material/chat:")
    st.chat_message("assistant").write("입력하신 문장을 기반으로 MBTI를 예측하고, 감정 분석 및 맞춤형 상담을 진행해 드립니다.")
    st.caption("10개의 문장을 입력하시면 상담이 시작됩니다.")
    st.chat_input("지금 바로 시작해보세요")

# mbti 리스트
def mbti_list():
    st.page_link("mbti_list.py", label="MBTI List", icon=":material/favorite:")
    mbti_descriptions = {
        "ESTP": "활발하고 현실적이며 문제 해결 능력이 뛰어난 유형입니다.",
        "ESFP": "사교적이고 즐거움을 추구하며 사람들과 잘 어울립니다.",
        "ENFP": "열정적이고 창의적이며 새로운 가능성을 탐구합니다.",
        "ENTP": "토론을 즐기며 혁신적이고 독창적인 아이디어를 추구합니다.",
        "ESTJ": "체계적이고 책임감이 강하며 리더십이 뛰어납니다.",
        "ESFJ": "친절하고 협조적이며 타인을 돕는 것을 좋아합니다.",
        "ENFJ": "타인의 성장을 돕고 영감을 주는 지도자형입니다.",
        "ENTJ": "전략적이며 목표 지향적이고 추진력이 강합니다.",
        "ISTJ": "성실하고 신뢰할 수 있으며 규칙과 절차를 중시합니다.",
        "ISFJ": "책임감 있고 헌신적이며 세심한 배려를 합니다.",
        "INFJ": "직관적이고 통찰력이 있으며 이상주의적인 성향입니다.",
        "INTJ": "분석적이고 계획적이며 독립적인 사고를 합니다.",
        "ISTP": "실용적이고 탐구심이 강하며 문제 해결에 능합니다.",
        "ISFP": "온화하고 예술적이며 조화를 중시합니다.",
        "INFP": "이상적이고 가치 중심적이며 깊이 있는 사고를 합니다.",
        "INTP": "논리적이며 이론적이고 독창적인 아이디어를 선호합니다.",
    }
    selected_mbti = st.selectbox(
        "MBTI", 
        options=list(mbti_descriptions.keys()),
        index=0
    )
    st.container(border=True)
    st.write(mbti_descriptions[selected_mbti])
    st.link_button("이 성격유형에 대해서 더 알아볼까요?", url=f"https://www.16personalities.com/ko/%EC%84%B1%EA%B2%A9%EC%9C%A0%ED%98%95-{selected_mbti}", icon=":material/open_in_new:")

# 추천 리스트
def recommand():
    st.page_link("recommand.py", label="Recommand", icon=":material/thumb_up:")
    with st.container(border=True):
        st.markdown("### 🎵 추천 음악")
        st.caption("감정을 어루만져 줄 음악을 추천합니다.")
        st.caption('감정분석을 먼저 완료해주세요!')

    with st.container(border=True):
        st.markdown("### ✈️ 감성 여행지")
        st.caption("지친 마음을 달래 줄 추천 여행지 추천입니다.")