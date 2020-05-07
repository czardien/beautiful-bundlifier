from datetime import datetime

from lib.models.notification import Notification


class Bundle:
    _TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, tours: int, timestamp_first_tour: datetime, timestamp_last_tour: datetime, receiver_id: str,
            first_friend_id: str, first_friend_name: str):
        self.tours = tours
        """The number of tours for the present bundle"""
        self.receiver_id = receiver_id
        """The user to send the bundle to"""
        self.friend_ids = {first_friend_id}
        """All distinct ids for friends who completed a tour as part of the present bundle"""
        self.first_friend_name = first_friend_name
        """The friend name who completed the first tour of the present bundle"""
        self.timestamp_first_tour = timestamp_first_tour
        """The friend name who completed the first tour of the present bundle"""
        self.timestamp_last_tour = timestamp_last_tour

    @property
    def message(self):
        if len(self.friend_ids) > 1:
            return f"{self.first_friend_name} and {self.tours - 1} other went on a tour"

        else:
            return f"{self.first_friend_name} went on a tour"

    @classmethod
    def from_notification(cls, notification: Notification):
        return Bundle(1, notification.timestamp, notification.timestamp, notification.user_id, notification.friend_id,
                notification.friend_name)

    def update(self, notification: Notification):
        self.friend_ids.add(notification.friend_id)
        self.timestamp_last_tour = notification.timestamp
        self.tours += 1

    def __str__(self):
        return ",".join([
            self.timestamp_last_tour.strftime(self._TIMESTAMP_FORMAT),
            self.timestamp_first_tour.strftime(self._TIMESTAMP_FORMAT),
            str(self.tours),
            self.receiver_id,
            self.message
        ])
