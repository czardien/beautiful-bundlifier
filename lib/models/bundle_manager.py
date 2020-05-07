import sys
from typing import Dict, List, Tuple, Set
from datetime import datetime

from lib.models.user import UserManager
from lib.models.notification import Notification
from lib.models.bundle import Bundle


class BundleManager:
    _READY: Dict[str, Bundle] = dict()
    _PENDING: Dict[str, Bundle] = dict()

    _METRICS: bool = False
    _METRICS_COUNT_DAY: int = 1
    _METRICS_COUNT_BUNDLE: int = 0
    _METRICS_USER_IDS: Set[str] = set({})

    _PREVIOUS_TS: datetime

    @classmethod
    def from_config(cls, initial_ts: datetime, metrics: bool = False):
        cls._PREVIOUS_TS = initial_ts
        cls._METRICS = metrics

    @classmethod
    def send_ready(cls):
        for user_id, bundle in sorted(cls._READY.items(), key=lambda tup: tup[1].timestamp_last_tour):
            cls._METRICS_USER_IDS.add(user_id)
            sys.stdout.write(str(bundle) + "\n")

        cls._READY = dict()

    @classmethod
    def send_pending(cls):
        for user_id, bundle in sorted(cls._PENDING.items(), key=lambda tup: tup[1].timestamp_last_tour):
            if cls._METRICS:
                cls._METRICS_COUNT_BUNDLE += 1
                cls._METRICS_USER_IDS.add(user_id)

            sys.stdout.write(str(bundle) + "\n")

        cls._PENDING = dict()

    @classmethod
    def update(cls, notification: Notification):
        current_timestamp = notification.timestamp
        elapsed = current_timestamp - cls._PREVIOUS_TS
        """Time delta between current notification timestamp and previous notification timestamp"""

        is_a_new_day = current_timestamp.year != cls._PREVIOUS_TS.year or \
                current_timestamp.month != cls._PREVIOUS_TS.month or \
                current_timestamp.day != cls._PREVIOUS_TS.day

        # reset all users count of bundles received to zero when going into new day
        if is_a_new_day:
            if cls._METRICS:
                cls._METRICS_COUNT_DAY += 1
            UserManager.reset_all_bundles_count()

        # if new observation takes places at same time than previous we just update pending bundles
        if elapsed.total_seconds() > 0:
            # when new observation happens in the future we move pending notifications into a ready state
            _tmp_ready: List[Tuple[str, Bundle]] = []

            for user_id, pending in cls._PENDING.items():
                # TODO: use variables
                # var_elapsed_since_first_tour = (current_timestamp - pending.timestamp_first_tour).total_seconds()
                # var_elapsed_since_last_tour = (current_timestamp - pending.timestamp_last_tour).total_seconds()
                # var_current_tours_count = pending.tours
                # var_user_bundles_count = UserManager.get(notification.user_id).bundles_count

                # naive; all pending go to ready
                _tmp_ready.append((user_id, pending))

            # building dict of ready
            cls._READY = dict(_tmp_ready)

            # cleaning up pending
            for user_id, ready in _tmp_ready:
                cls._PENDING.pop(user_id)

        # updating pending with current notification
        if notification.user_id in cls._PENDING:
            cls._PENDING[notification.user_id].update(notification)

        else:
            cls._PENDING[notification.user_id] = Bundle.from_notification(notification)

        # setting previous timestamp to current timestamp
        cls._PREVIOUS_TS = current_timestamp
