from googleapiclient.discovery import build
import os


class Video:

    def __init__(self, video_id):
        youtube = self.get_service()
        self.__video_id = video_id
        try:
            self._video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.__video_id
                                                         ).execute()

            assert self._video_response['items'] != []
        except AssertionError:
            self.__title = None
            self.__url = None
            self.__view_count = None
            self.__like_count = None
            self.__comment_count = None
        else:
            self.__title = self._video_response['items'][0]['snippet']['title']
            self.__url = f'https://youtu.be/{self.__video_id}'
            self.__view_count = self._video_response['items'][0]['statistics']['viewCount']
            self.__like_count = self._video_response['items'][0]['statistics']['likeCount']
            self.__comment_count = self._video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.__title

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

