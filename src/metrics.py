import statistics as stats

from lib import utils
from lib.models.bundle import Bundle


def metrics(bundles_filepath: str):
    """
    Get all bundles and users with number of bundles sent per user; based on notebooks/bundles.ipynb measures.
    """
    bundles = list()

    daily_avgs = list()
    daily_loads = dict()
    daily_delays = list()

    with open(bundles_filepath, "r") as fp:
        previous_ts = None
        for line in fp.readlines():
            bundle = Bundle.from_line(line)
            bundles.append(bundle)

            current_ts = bundle.timestamp_last_tour

            if utils.is_a_new_day(current_ts, previous_ts):
                daily_avgs.append({
                    "load": stats.mean(list(daily_loads.values())),
                    "delay": stats.mean(daily_delays)
                })

                daily_loads = dict()
                daily_delays = list()

            if bundle.receiver_id in daily_loads:
                daily_loads[bundle.receiver_id] += 1

            else:
                daily_loads[bundle.receiver_id] = 1

            daily_delays.append((bundle.timestamp_last_tour - bundle.timestamp_first_tour).total_seconds())

            previous_ts = current_ts

    avg_load = stats.mean([daily_avg["load"] for daily_avg in daily_avgs])
    std_load = stats.stdev([daily_avg["load"] for daily_avg in daily_avgs])

    avg_delay = stats.mean([daily_avg["delay"] for daily_avg in daily_avgs])
    std_delay = stats.stdev([daily_avg["delay"] for daily_avg in daily_avgs])

    print(f"Average daily load per user: {avg_load:.2f} bundle/user/day")
    print(f"Std dev daily load per user: {std_load:.2f} bundle/user/day")

    print(f"Average bundle delay: {avg_delay:.2f} seconds ({avg_delay / 60:.1f}min)")
    print(f"Std dev bundle delay: {std_delay:.2f} seconds ({std_delay / 60:.1f}min)")


if __name__ == "__main__":
    metrics("data/bundles.csv")
