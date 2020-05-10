from typing import List

from lib import utils
from lib.errors import BundlifyError
from lib.config import Config
from lib.hypervisor import Hypervisor, HypervisorFactory
from lib.models.notification import Notification


def bundlify(notifications_filepath: str, hypervisor: Hypervisor, csv_headers: List[str], csv_delimiter: str = ','):
    # pass on the data builds user and event models
    with open(notifications_filepath, "r") as f:
        previous_timestamp = None
        for line in f.readlines():
            try:
                notification = Notification.from_line(line, csv_headers, csv_delimiter)

            except TypeError:
                raise BundlifyError(f"Please provide a valid file with headers: {csv_headers}")

            current_timestamp = notification.timestamp

            if utils.is_a_new_day(current_timestamp, previous_timestamp):
                hypervisor.send_bundles()

            hypervisor.update_notifications(notification)
            previous_timestamp = current_timestamp

        if not line:
            raise BundlifyError(f"Please do not provide an empty file.")

        # process remaining notifications
        hypervisor.send_bundles(last_timestamp=notification.timestamp)


if __name__ == "__main__":
    args = utils.parse_args(list(HypervisorFactory._ENABLED.keys()))

    hypervisor = HypervisorFactory.build(args.hypervisor)
    bundlify(args.notifications_filepath, hypervisor, Config.CSV_HEADERS)
