import sys
from typing import Dict, List, Union
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


class HypervisorV1(Hypervisor):
    """V1 bundles all notifications when a daily number for a given user exceeds 4"""

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


class HypervisorFactory:
    _ENABLED = {"naive": HypervisorNaive, "v1": HypervisorV1}

    @classmethod
    def build(cls, hid: str) -> Hypervisor:

        if hid not in cls._ENABLED:
            raise BundlifyError(f"Hypervisor: '{hid}' not enabled - currently enabled: {cls._ENABLED}")

        return cls._ENABLED[hid]()
