from datetime import datetime


class Config:
    USERS_FILEPATH = "data/users.csv"

    CSV_HEADERS = ["timestamp", "user_id", "friend_id", "friend_name"]
    CSV_DELIMITER = ","

    INITIAL_TS = datetime(2017, 8, 1, 0, 6, 47)
    MAX_NOTIFICATIONS_PER_DAY = 4
    ANALYSIS = False
