import sys
import argparse
from datetime import datetime

from lib import utils
from lib.models.bundle import Bundle


def metrics(bundles_filepath: str, headers: bool = False):
    """
    Get all bundles and users with number of bundles sent per user; based on notebooks/bundles.ipynb measures.
    """
    users = dict()
    bundles = list()

    with open(bundles_filepath, "r") as fp:
        for line in fp.readlines():
            split = utils.split_csv_line(line, ',')

            bundle = Bundle(split[2], datetime.strptime(split[0], Bundle._TIMESTAMP_FORMAT),
                            datetime.strptime(split[1], Bundle._TIMESTAMP_FORMAT), split[3], "UNKNOWN", "UNKOWN")
            bundles.append(bundle)

            if bundle.receiver_id not in users:
                users[bundle.receiver_id] = 1
            else:
                users[bundle.receiver_id] += 1

    span_bundles = bundles[-1].timestamp_last_tour - bundles[0].timestamp_last_tour
    span_bundles_seconds = span_bundles.total_seconds()

    # converting values for users to daily averages
    for uid, val in users.items():
        users[uid] = val / (span_bundles_seconds / 3600 / 24)

    # separating users on load acceptable threshold
    top_users_daily = {uid: val for uid, val in users.items() if val > 4}
    rest_users_daily = {uid: val for uid, val in users.items() if val <= 4}

    # measuring average load and delay on two sets
    avg_load_rest = sum(rest_users_daily.values()) / len(rest_users_daily)
    avg_load_top = sum(top_users_daily.values()) / len(top_users_daily)

    rest_bundles = [b for b in bundles if b.receiver_id in rest_users_daily]
    top_bundles = [b for b in bundles if b.receiver_id in top_users_daily]

    avg_delay_rest = sum(
        [
            (b.timestamp_last_tour - b.timestamp_first_tour).total_seconds()
            for b in rest_bundles
        ]) / len(rest_bundles)

    avg_delay_top = sum(
        [
            (b.timestamp_last_tour - b.timestamp_first_tour).total_seconds()
            for b in top_bundles
        ]) / len(top_bundles)

    line = f"{datetime.now().isoformat()},{avg_load_rest:.4f},{avg_load_top:.4f},{avg_delay_rest:.2f}," \
            f"{avg_delay_top:.2f}\n"

    if headers:
        sys.stdout.write("timestamp,avg_load_rest,avg_load_top,avg_delay_rest,avg_delay_top\n")

    sys.stdout.write(line)


def parse_args():
    parser = argparse.ArgumentParser(description='Generates metrics from a bundles stream')
    parser.add_argument('--headers', '-H', action='store_true', dest='headers', help='Prints headers')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    metrics("data/bundles.csv", args.headers)
