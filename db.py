import json
from collections import defaultdict

DB_PATH = "db.json"

class Database:
    def __init__(self):
        data : dict = json.load(open(DB_PATH))["users"]
        self.users = {int(key) : value for key, value in data.items()}

    def save(self):
        json.dump(self.__dict__, open(DB_PATH, mode="w"))
    
    def get(self, user_id: int) -> dict:
        if self.users.get(user_id) == None:
            self.users[user_id] = dict()

        return self.users[user_id]