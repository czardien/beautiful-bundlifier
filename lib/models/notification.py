from typing import List
from datetime import datetime


class Notification:
    _TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, timestamp: str, user_id: str, friend_id: str, friend_name: str):
        self.timestamp = datetime.strptime(timestamp, self._TIMESTAMP_FORMAT)
        self.user_id = user_id
        self.friend_id = friend_id
        self.friend_name = friend_name

    @staticmethod
    def _split_line(line: str, csv_delimiter: str):
        return [element.strip().replace("\n", "") for element in line.split(csv_delimiter)]

    @classmethod
    def from_line(cls, line: str, csv_headers: List[str], csv_delimiter: str):
        csv_line = cls._split_line(line, csv_delimiter)
        return Notification(**dict(zip(csv_headers, csv_line)))

    def __str__(self):
        return f"Event(timestamp='{self.timestamp}',user_id='{self.user_id}',friend_id='{self.friend_id}'," \
               f"friend_name='{self.friend_name}')"
