import json
import os

from googleapiclient.discovery import build


channel_id = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=channel_id)

class Channel:
    """Класс для ютуб-канала"""

    def init(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
    def print_info(self, dict_to_print: dict) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))