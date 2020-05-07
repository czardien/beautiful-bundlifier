import argparse
from typing import List

from lib.config import Config
from lib.models.notification import Notification

from lib.models.user import UserManager
from lib.models.bundle_manager import BundleManager


def bundle(notifications_filepath: str, csv_headers: List[str], csv_delimiter: str = ','):
    # pass on the data builds user and event models
    with open(notifications_filepath, "r") as f:
        for line in f.readlines():
            notification = Notification.from_line(line, csv_headers, csv_delimiter)
            BundleManager.update(notification)
            BundleManager.send_ready()

    BundleManager.send_pending()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates bundles from a timestamped notifications stream')
    parser.add_argument('notifications_filepath', type=str, help='Absolute path for the event stream to process.')
    parser.add_argument('--metrics', dest='metrics', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    UserManager.from_filepath(Config.USERS_FILEPATH)
    print(Config.INITIAL_TS)
    print(type(Config.INITIAL_TS))
    BundleManager.from_config(Config.INITIAL_TS, args.metrics)

    bundle(args.notifications_filepath, Config.NOTIFICATIONS_HEADERS)
