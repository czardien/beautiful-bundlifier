import sys
from typing import Set
from datetime import datetime

from lib.models.bundle import Bundle


class StatsManager:
    _HEADERS = ["avg_delay", "avg_tours_count", "avg_daily_bundle_count"]

    _COUNT_BUNDLES: int = 0
    _COUNT_DAYS: int = 1

    _DAILY_COUNT: int = 0
    _DAILY_USERS: Set[str] = set()

    _AVG_DELAY: float = 0.0
    _AVG_TOUR_COUNT: float = 0.0
    _AVG_DAILY_BUNDLE_COUNT: float = 0.0

    _PREVIOUS_TS: datetime = datetime(2017, 8, 1, 0, 6, 47)

    @classmethod
    def update(cls, bundle: Bundle):
        # update daily if needed
        current_timestamp = bundle.timestamp_last_tour
        is_a_new_day = current_timestamp.year != cls._PREVIOUS_TS.year or \
                current_timestamp.month != cls._PREVIOUS_TS.month or \
                current_timestamp.day != cls._PREVIOUS_TS.day

        if is_a_new_day:
            cls.update_daily()

        # incremental average
        cls._COUNT_BUNDLES += 1
        cls._DAILY_COUNT += 1
        cls._DAILY_USERS.add(bundle.receiver_id)

        cls._AVG_DELAY = cls._AVG_DELAY + (bundle.delay.total_seconds() - cls._AVG_DELAY) / cls._COUNT_BUNDLES
        cls._AVG_TOUR_COUNT = cls._AVG_TOUR_COUNT + (bundle.tours - cls._AVG_TOUR_COUNT) / cls._COUNT_BUNDLES

        cls._PREVIOUS_TS = current_timestamp

    @classmethod
    def update_daily(cls):
        avg_daily_bundle_count = float(cls._DAILY_COUNT) / float(len(cls._DAILY_USERS))
        cls._AVG_DAILY_BUNDLE_COUNT = cls._AVG_DAILY_BUNDLE_COUNT + \
                (avg_daily_bundle_count - cls._AVG_TOUR_COUNT) / cls._COUNT_DAYS

        cls._COUNT_DAYS += 1
        cls._DAILY_COUNT = 0
        cls._DAILY_USERS = {}

    @classmethod
    def log(cls):
        avgs = [str(cls._AVG_DELAY), str(cls._AVG_TOUR_COUNT), str(cls._AVG_DAILY_BUNDLE_COUNT)]

        sys.stderr.write(','.join(cls._HEADERS) + "\n")
        sys.stderr.write(','.join(avgs) + "\n")
