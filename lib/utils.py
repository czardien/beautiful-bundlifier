import argparse
from typing import Union
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Generates bundles from a timestamped notifications stream')
    parser.add_argument('notifications_filepath', type=str, help='Absolute path for the event stream to process.')
    return parser.parse_args()


def is_a_new_day(cur: datetime, pre: Union[datetime, None]) -> bool:
    if not pre:
        return False

    return cur.day != pre.day or cur.month != pre.month or cur.year != pre.year


def split_csv_line(line: str, csv_delimiter: str):
    return [element.strip().replace("\n", "") for element in line.split(csv_delimiter)]
