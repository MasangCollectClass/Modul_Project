import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

<<<<<<< HEAD
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

request = youtube.search().list(
    part="snippet",
    q="biochar concrete",   # 검색어
    maxResults=5,
    type="video"
)

response = request.execute()

for item in response["items"]:
    title = item["snippet"]["title"]
    video_id = item["id"]["videoId"]
    print(f"{title} - https://www.youtube.com/watch?v={video_id}")
=======
# .env에서 API 키 로드
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def recommend_music_by_emotion(emotion: str, max_results: int = 3) -> list:

    if not emotion:
        search_query = "감정 안정 음악"
    else:
        search_query = f"{emotion.strip()}할 때 듣는 노래"

    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        request = youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            maxResults=max_results,
            order="relevance"
        )
        response = request.execute()

        results = []
        for item in response["items"]:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            results.append({"title": title, "url": video_url})

        return results

    except Exception as e:
        print(f"[오류] 유튜브 검색 실패: {e}")
        return [{"title": "검색 실패", "url": ""}]

if __name__ == '__main__':
    test_emotion = input("감정을 입력하세요 (예: 불안, 기쁨, 슬픔): ")
    recommendations = recommend_music_by_emotion(test_emotion)
    
    print("\n🎵 추천 음악:")
    for music in recommendations:
        print(f"- {music['title']}\n  {music['url']}\n")
>>>>>>> bin
