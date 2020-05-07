from datetime import datetime


class Config:
    USERS_FILEPATH = "data/users.csv"

    NOTIFICATIONS_HEADERS = ["timestamp", "user_id", "friend_id", "friend_name"]

    INITIAL_TS = datetime(2017, 8, 1, 0, 6, 47)
    MAX_NOTIFICATIONS_PER_DAY = 4


class ConfigStats:
    BUNDLES_HEADERS = ["timestamp_last_tour", "timestamp_first_tour", "tours", "receiver_id", "message"]

    INITIAL_TS = datetime(2017, 8, 1, 0, 6, 47)
    MAX_NOTIFICATIONS_PER_DAY = 4
