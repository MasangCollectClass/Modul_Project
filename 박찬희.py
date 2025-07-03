import streamlit as st
import random

st.set_page_config(page_title="여행지 추천", layout="wide")
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] {
            max-width: 130px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
""", unsafe_allow_html=True)

st.header("여행지 추천")

# 여행 영상
videos = {
    "MBTI 필수 영상": [
        "https://www.youtube.com/embed/exJF_Y3QFbg",
    ],
    "아시아": [ 
        "https://www.youtube.com/embed/U4nGQDQ_VVk",
    ],
    "유럽": [
        "https://www.youtube.com/embed/gWAWZ5uTJak",
    ],
    "북미": [
        "https://www.youtube.com/embed/IYIJi-yoqU4",
    ],
    "남미": [
        "https://www.youtube.com/embed/6mgojdknC5A",
    ],
    "아프리카": [
        "https://www.youtube.com/embed/BA9oBJBjKsg",
    ],
    "오세아니아": [
        "https://www.youtube.com/embed/IDWqPQgXj6k?list=PLVM-Zbp1vQ7flXGIs5Awh357olB8FYzVw",
    ]
}

# 음악 추천 - 감정별
music_recommendations = {
    "MBTI 유형별 노래": [
        "https://www.youtube.com/embed/-xDt6P58tt0",
    ],

    "기분 좋아지는 노래": [
        "https://www.youtube.com/embed/9Ibf10h9U0c",
    ]
}

# 탭 자동 생성
tabs = st.tabs(list(videos.keys()) + ["🎵 음악 추천"])

# iframe 템플릿
iframe_template = '''
<iframe width="1000" height="563" src="{url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
'''

# 여행 탭
for i, region in enumerate(videos.keys()):
    with tabs[i]:
        st.subheader(f"🎥 {region} 추천 여행 영상")
        for url in videos[region]:
            cache_buster = random.randint(1, 999999)
            url_with_cb = url + f"&cb={cache_buster}" if "?" in url else url + f"?cb={cache_buster}"
            st.markdown(iframe_template.format(url=url_with_cb), unsafe_allow_html=True)

# 음악 탭
with tabs[-1]:
    st.subheader("🎶 감정에 어울리는 음악 추천")
    for mood, urls in music_recommendations.items():
        st.markdown(f"**{mood}**")
        for url in urls:
            st.markdown(iframe_template.format(url=url), unsafe_allow_html=True)
