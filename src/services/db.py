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
                        { "first_name": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
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
    



class Client:
    def __init__(self):
        self.clients = db['clients']

    def create_client(self, data):
        result = self.clients.insert_one(data)
        return result

    def find_client(self, cond={}):
        result = self.clients.find_one(cond)
        return result

    def delete_client(self, cond):
        result = self.clients.delete_one(cond)
        return result

    def get_clients(self, cond={}):
        
        if 'search' in cond:
            cond['$or'] = [
                        { "first_name": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
                        { "email": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
                    ]
            del cond['search']

        aggregation = [
            {
                "$match": cond
            },
            {
                "$lookup": {
                    "from": "users",
                    "let": {
                        "employee": "$employee" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": ["$_id", "$$employee"]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "employee"
                }
            },
            { "$unwind": { "path": "$employee", "preserveNullAndEmptyArrays": True } },
            {
                "$project": {
                    'first_name': 1,
                    'last_name': 1,
                    'email': 1,
                    'mobile': 1,
                    'dob': 1,
                    'employee': "$employee.first_name"
                }
            },
            {
                "$sort": {
                    'createdAt': -1
                }
            }
        ]
        result = self.clients.aggregate(aggregation)
        return result

    def update_client(self, cond, data):

        result = self.clients.update_one(cond, {"$set": data})
        return result




class Admin:
    def __init__(self):
        self.admins = db['admins']

    def create_admin(self, data):
        result = self.admins.insert_one(data)
        return result

    def find_admin(self, cond={}):
        result = self.admins.find_one(cond)
        return result
