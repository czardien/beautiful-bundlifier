import sys
from typing import List
from datetime import datetime
from lib.models.event import Event


class Notification:
    _TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, tours: int, timestamp_first_tour: datetime, receiver_id: str, message: str):
        self.tours = tours
        self.timestamp_first_tour = timestamp_first_tour
        self.receiver_id = receiver_id
        self.message = message
        self.notification_sent = None

    @classmethod
    def from_event(cls, event: Event):
        return Notification(1, event.timestamp, event.user_id,
                f"{event.friend_name} went on a tour")

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
    _BATCH: List[Notification] = list()
    _MAX_NOTIFICATIONS_PER_DAY = None

    @classmethod
    def from_config(cls, max_notifications_per_day: int):
        cls._MAX_NOTIFICATIONS_PER_DAY = max_notifications_per_day

    @staticmethod
    def send(notification):
        sys.stdout.write(str(notification) + "\n")

    @classmethod
    def update_batch(cls, event: Event):
        cls._BATCH.append(Notification.from_event(event))

    @classmethod
    def send_batch(cls):
        for notification in cls._BATCH:
            notification.update_sent_timestamp()
            cls.send(notification)
