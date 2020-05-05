from typing import Dict


class User:
    def __init__(self, id: str, notifications_count: int = 0):
        self.id = id
        self.notifications_count = notifications_count


class UserManager:
    _ALL_USERS: Dict[str, "User"] = dict()

    @classmethod
    def increment_notifications_count(cls, user_id: str):
        cls._ALL_USERS[user_id].notifications_count += 1

    @classmethod
    def from_filepath(cls, users_filepath: str):
        with open(users_filepath) as fd:
            for line in fd.readlines():
                uid = line.strip("\n")
                cls._ALL_USERS[uid] = User(uid, 0)

    @classmethod
    def reset_all_notifications_count(cls):
        for user in cls._ALL_USERS.values():
            user.notifications_count = 0
