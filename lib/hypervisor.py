import sys
from typing import Dict, List, Union, Tuple
from datetime import datetime

from lib.errors import BundlifyError
from lib.models.bundle import Bundle
from lib.models.notification import Notification


class Hypervisor:
    def __init__(self):
        self.bundles: List[Bundle] = list()
        self.user_notifications: Dict[str, List[Notification]] = dict()

    def _compute_bundles_from_notifications(self) -> List[Bundle]:
        raise NotImplementedError("Consider me an abstract class :heart:")

    def send_bundles(self, last_timestamp: Union[datetime, None] = None):
        """This method goes over pending notifications and computes bundles"""
        self.bundles = self._compute_bundles_from_notifications()

        # reset user notifications
        self.user_notifications = {uid: list() for uid in self.user_notifications}

        if self.bundles:
            for bundle in sorted(self.bundles, key=lambda b: b.timestamp_last_tour):
                sys.stdout.write(str(bundle) + "\n")

    def update_notifications(self, notification: Notification):
        if notification.user_id in self.user_notifications:
            self.user_notifications[notification.user_id].append(notification)

        else:
            self.user_notifications[notification.user_id] = [notification]


class HypervisorNaive(Hypervisor):
    """Naive maps each Notification to a Bundle; delay assured to be 0"""

    def _compute_bundles_from_notifications(self) -> List[Bundle]:
        bundles = list()
        for user_id, notifications in self.user_notifications.items():
            for notification in notifications:
                bundles.append(Bundle.from_notification(notification))

        return bundles


class HypervisorAllInOne(Hypervisor):
    """AllInOne bundles all notifications when a daily number for a given user exceeds 4"""

    def _compute_bundles_from_notifications(self) -> List[Bundle]:
        bundles = list()
        for user_id, notifications in self.user_notifications.items():
            if len(notifications) > 4:
                bundle = Bundle.from_notification(notifications[0])
                for notification in notifications[1:]:
                    bundle.update(notification)

                bundles.append(bundle)

            else:
                bundles.extend([Bundle.from_notification(notification) for notification in notifications])

        return bundles


class HypervisorGreedy(Hypervisor):
    """Greedy bundles notifications with minimum delay when a daily number for a given user exceeds 4"""

    def _compute_bundles_from_notifications(self) -> List[Bundle]:
        bundles: List[Bundle] = list()
        for user_id, notifications in self.user_notifications.items():
            if len(notifications) > 4:
                # dynamically evaluate equally split buckets while keeping delay small
                # bundles_with_delay: List[Tuple[List[Bundle], float]] = list()
                bundles_with_min_delay: Union[Bundle, None] = None
                min_delay: float = None

                for idx1 in range(1, len(notifications) - 2):
                    for idx2 in range(idx1 + 1, len(notifications) - 1):
                        for idx3 in range(idx2 + 1, len(notifications)):
                            tmp_bundles = [
                                Bundle.from_notifications(notifications[:idx1]),
                                Bundle.from_notifications(notifications[idx1:idx2]),
                                Bundle.from_notifications(notifications[idx2:idx3]),
                                Bundle.from_notifications(notifications[idx3:])
                            ]
                            tmp_delay = sum([bundle.delay.total_seconds() for bundle in tmp_bundles])
                            if not min_delay or tmp_delay < min_delay:
                                bundles_with_min_delay = tmp_bundles
                                min_delay = tmp_delay

                            # bundles_with_delay.append((tmp_bundles, tmp_delay))

                # bundles_with_min_delay = min(bundles_with_delay, key=lambda bundle_with_delay: bundle_with_delay[1])[0]
                bundles.extend(bundles_with_min_delay)

            else:
                bundles.extend([Bundle.from_notification(notification) for notification in notifications])

        return bundles


class HypervisorFactory:
    _ENABLED = {
        "naive": HypervisorNaive,
        "all-in-one": HypervisorAllInOne,
        "greedy": HypervisorGreedy
    }

    @classmethod
    def build(cls, hid: str) -> Hypervisor:

        if hid not in cls._ENABLED:
            raise BundlifyError(f"Hypervisor: '{hid}' not enabled - currently enabled: {cls._ENABLED}")

        return cls._ENABLED[hid]()
