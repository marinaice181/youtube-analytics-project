import os
from datetime import timedelta
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """
        название плейлиста
        ссылку на плейлист
        """
        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails,snippet',
                                                                 maxResults=50, ).execute()
        self.channel_id = self.playlist_videos['items'][0]['snippet']['channel_id']
        self.playlists = self.youtube.playlists().list(channelId=self.channel_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50, ).execute()
        for playlist in self.playlists['items']:
            if playlist['id'] == self.playlist_id:
                self.title = playlist['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)).execute()

    def __str__(self):
        return f'{self.title}'

    @property
    def total_duration(self) -> timedelta:
        """
        возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        total:timedelta = timedelta(hours=0, minutes=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        """
        Возвращает ссылку на популярное видео из плэйлиста (по количеству лайков)
        """
        max_like_count = 0
        url = ""
        for video in self.video_response['items']:
            if max_like_count < int(video['statistics']['likeCount']):
                max_like_count = int(video['statistics']['likeCount'])
                url = f"https://www.youtu.be/{video['id']}"
            return url