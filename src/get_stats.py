import argparse
from typing import List

from lib.config import ConfigStats
from lib.models.bundle import Bundle
from lib.models.stats_manager import StatsManager


def stats(bundles_filepath: str, csv_headers: List[str], csv_delimiter: str = ','):
    # pass on the data builds user and event models
    with open(bundles_filepath, "r") as f:
        for line in f.readlines():
            bundle = Bundle.from_line(line, csv_headers, csv_delimiter)
            StatsManager.update(bundle)

    StatsManager.log()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates stats from bundles and notifications filepaths.')
    parser.add_argument('bundles_path', type=str, help='Absolute path for the bundles file to process.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    stats(args.bundles_path, ConfigStats.BUNDLES_HEADERS)
