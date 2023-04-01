from pymongo import MongoClient, GEOSPHERE
import os
import bson

#cC7WjuD5Dj3mz9l2
client = MongoClient("mongodb+srv://vaseem:wK7COg790fEBik4n@cluster0.h7oo8j8.mongodb.net")
db = client["manaya-finserve-dev"]


class User:
    def __init__(self):
        self.user = db['users']

    def create_user(self, data):
        result = self.user.insert_one(data)
        return result

    def find_user(self, cond={}):
        result = self.user.find_one(cond)
        return result

    def delete_user(self, cond):
        result = self.user.delete_one(cond)
        return result

    def get_users(self, cond={}):
        
        if 'search' in cond:
            cond['$or'] = [
                        { "name": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
                        { "email": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
                    ]
            del cond['search']

        aggregation = [
            {
                "$match": cond
            },
            {
                "$sort": {
                    'createdAt': -1
                }
            }
        ]
        result = self.user.aggregate(aggregation)
        return result

    def update_user(self, cond, data):
        result = self.user.update_one(cond, {"$set": data})
        return result

