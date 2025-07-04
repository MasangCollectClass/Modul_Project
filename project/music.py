import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

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