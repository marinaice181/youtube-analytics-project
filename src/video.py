import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id # id видео
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.video_id).execute()
        self.title: str = self.video_response['items'][0]['snippet']['title'] # название видео
        self.video_url = f"https://www.youtube.com/{self.video_id}" # ссылка на видео
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount'] # количество просмотров
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount'] # количество лайков

    def __str__(self):
        return self.title


class PLVideo(Video):
    """
    Класс который инициализируется 'id видео' и 'id плейлиста'
    """
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id