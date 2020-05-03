import sys
from typing import Dict
from datetime import datetime, timedelta

from lib.models.event import Event


class Notification:
    _TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, tours: int, timestamp_first_tour: datetime, receiver_id: str, first_friend_name: str):
        self.tours = tours
        self.timestamp_first_tour = timestamp_first_tour
        self.receiver_id = receiver_id
        self.first_friend_name = first_friend_name
        self.notification_sent = None

    @property
    def message(self):
        if self.tours > 1:
            return f"{self.first_friend_name} and {self.tours - 1} other went on a tour"

        else:
            return f"{self.first_friend_name} went on a tour"

    @classmethod
    def from_event(cls, event: Event):
        return Notification(1, event.timestamp, event.user_id, event.friend_name)

    def update(self, event: Event):
        self.tours += 1

    def update_sent_timestamp(self):
        self.notification_sent = datetime.now()

    def __str__(self):
        return ",".join([
            self.notification_sent.strftime(self._TIMESTAMP_FORMAT),
            self.timestamp_first_tour.strftime(self._TIMESTAMP_FORMAT),
            str(self.tours),
            self.receiver_id,
            self.message
        ])


class NotificationManager:
    _BATCH: Dict[str, Notification] = dict()
    _MAX_NOTIFICATIONS_PER_DAY: int = 4

    _ELAPSED: timedelta

    @classmethod
    def from_config(cls, max_notifications_per_day: int):
        cls._MAX_NOTIFICATIONS_PER_DAY = max_notifications_per_day

    @staticmethod
    def send(notification: Notification):
        sys.stdout.write(str(notification) + "\n")

    @classmethod
    def update_batch(cls, event: Event):
        if event.user_id not in cls._BATCH:
            cls._BATCH[event.user_id] = Notification.from_event(event)

        else:
            cls._BATCH[event.user_id].update(event)

    @classmethod
    def send_batch(cls):
        for user_id, notification in cls._BATCH.items():
            notification.update_sent_timestamp()
            cls.send(notification)

        cls._BATCH = dict()
