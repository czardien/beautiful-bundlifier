import sys
from typing import Dict, List, Tuple
from datetime import datetime

from lib.models.user import UserManager
from lib.models.event import Event
from lib.models.notification import Notification


class NotificationManager:
    """
    For all users all notifications are created and live by default in _PENDING; as time goes with further observations

    """
    _READY: Dict[str, Notification] = dict()
    _PENDING: Dict[str, Notification] = dict()

    _PREVIOUS_TS: datetime

    _MAX_NOTIFICATIONS_PER_DAY: int = 4
    _ANALYSIS: bool = False
    """If set to true will print additional information on stdout for analysis (e.g. delay, #notif/day/user...)"""

    @classmethod
    def from_config(cls, max_notifications_per_day: int, analysis: bool, initial_ts: datetime):
        cls._MAX_NOTIFICATIONS_PER_DAY = max_notifications_per_day
        cls._ANALYSIS = analysis
        cls._PREVIOUS_TS = initial_ts

    @classmethod
    def send_ready(cls):
        for notification in sorted(cls._READY.values(), key=lambda n: n.timestamp_last_tour):
            sys.stdout.write(str(notification) + "\n")

        cls._READY = dict()

    @classmethod
    def send_pending(cls):
        for notification in sorted(cls._PENDING.values(), key=lambda n: n.timestamp_last_tour):
            sys.stdout.write(str(notification) + "\n")

        cls._PENDING = dict()

    @classmethod
    def update(cls, event: Event):
        """Where the magic happens"""
        current_timestamp = event.timestamp
        elapsed = current_timestamp - cls._PREVIOUS_TS
        """Time delta between current event timestamp and previous event timestamp"""

        is_a_new_day = current_timestamp.year != cls._PREVIOUS_TS.year or \
                current_timestamp.month != cls._PREVIOUS_TS.month or \
                current_timestamp.day != cls._PREVIOUS_TS.day

        if is_a_new_day:
            # reset all users count of notifications received to zero when going into new day
            UserManager.reset_all_notifications_count()

        _tmp_ready: List[Tuple[str, Notification]] = []
        for user_id, pending in cls._PENDING.items():
            if elapsed.total_seconds() > 0:
                _tmp_ready.append((user_id, pending))

        for user_id, _ in _tmp_ready:
            # unsetting pending when ready
            cls._PENDING.pop(user_id)

        # building list of ready
        cls._READY = dict(_tmp_ready)

        # updating pending with current event
        if event.user_id in cls._PENDING:
            cls._PENDING[event.user_id].update(event)

        else:
            cls._PENDING[event.user_id] = Notification.from_event(event)

        # setting previous timestamp to current timestamp
        cls._PREVIOUS_TS = current_timestamp
