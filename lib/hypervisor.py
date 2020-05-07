import sys
from typing import Dict, List, Union
from datetime import datetime

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

        if self.bundles:
            for bundle in sorted(self.bundles, key=lambda b: b.timestamp_last_tour):
                sys.stdout.write(str(bundle) + "\n")

    def update_notifications(self, notification: Notification):
        if notification.user_id in self.user_notifications:
            self.user_notifications[notification.user_id].append(notification)

        else:
            self.user_notifications[notification.user_id] = [notification]


class HypervisorNaive(Hypervisor):

    def _compute_bundles_from_notifications(self) -> List[Bundle]:
        bundles = list()
        for user_id, notifications in self.user_notifications.items():
            for notification in notifications:
                bundles.append(Bundle.from_notification(notification))

        return bundles
