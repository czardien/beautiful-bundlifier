import argparse
from typing import List

from lib.config import Config
from lib.models.event import Event
from lib.models.user import UserManager
from lib.models.notification_manager import NotificationManager


def bundle(events_stream_path: str, csv_headers: List[str], csv_delimiter: str):
    # pass on the data builds user and event models
    with open(events_stream_path, "r") as f:
        for line in f.readlines()[:3]:
            event = Event.from_line(line, csv_headers, csv_delimiter)
            NotificationManager.update(event)
            NotificationManager.send_ready()

        NotificationManager.send_pending()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates notifications from event stream.')
    parser.add_argument('events_stream_path', type=str, help='Absolute path for the event stream to process.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    UserManager.from_filepath(Config.USERS_FILEPATH)
    NotificationManager.from_config(Config.MAX_NOTIFICATIONS_PER_DAY, Config.ANALYSIS, Config.INITIAL_TS)

    bundle(args.events_stream_path, Config.CSV_HEADERS, Config.CSV_DELIMITER)
