import sys
import argparse
from typing import List, Set

from lib.config import Config
from lib.models.event import Event


USER_IDS: Set[str] = set()


def read_users(events_stream_path: str, csv_headers: List[str], csv_delimiter: str):
    # pass on the data builds user and event models
    with open(events_stream_path, "r") as f:
        for line in f.readlines():
            event = Event.from_line(line, csv_headers, csv_delimiter)

            if event.user_id not in USER_IDS:
                USER_IDS.add(event.user_id)
                sys.stdout.write(f"{event.user_id}\n")


def parse_args():
    parser = argparse.ArgumentParser(description='Generates user base from event stream.')
    parser.add_argument('events_stream_path', type=str, help='Absolute path for the event stream to process.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    read_users(args.events_stream_path, Config.CSV_HEADERS, Config.CSV_DELIMITER)
