from pymongo import MongoClient
import os


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
                    '_id': {
                        "$toString": "$_id"
                    },
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




class Bank:
    def __init__(self):
        self.banks = db['banks']

    def create_bank(self, data):
        result = self.banks.insert_one(data)
        return result

    def find_bank(self, cond={}):
        result = self.banks.find_one(cond)
        return result

    def delete_bank(self, cond):
        result = self.banks.delete_one(cond)
        return result
    


    def get_banks(self, cond={}):
        
        if 'search' in cond:
            cond['$or'] = [
                        { "name": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
                    ]
            del cond['search']

        aggregation = [
            {
                "$match": cond
            },
            {
                "$project": {
                    "name": 1,
                    "status": 1,
                    "createdAt": { "$dateToString": { "format": "%d-%m-%Y", "date": "$createdAt" } },
                }
            },
            {
                "$sort": {
                    'createdAt': -1
                }
            }
        ]
        result = self.banks.aggregate(aggregation)
        return result
    
    def get_bank_with_cards(self, cond={}):
        
        if 'search' in cond:
            cond['$or'] = [
                        { "name": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
                    ]
            del cond['search']

        aggregation = [
            {
                "$match": cond
            },
            {
                "$lookup": {
                    "from": "cards",
                    "let": {
                        "bank_id": "$_id" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": ["$bank", "$$bank_id"]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "cards"
                }
            },
            { "$unwind": { "path": "$cards",  } },
            {
                "$project": {
                    "_id": {
                        "$toString": "$_id"
                    },
                    "name": 1,
                    "status": 1,
                    "cards": {
                        "_id": {
                            "$toString": "$cards._id"
                        },
                    "name": 1
                    },
                    "createdAt": { "$dateToString": { "format": "%d-%m-%Y", "date": "$createdAt" } },
                }
            },
            {
                "$sort": {
                    'createdAt': -1
                }
            }
        ]
        result = self.banks.aggregate(aggregation)
        return result

    def update_bank(self, cond, data):
        result = self.banks.update_one(cond, {"$set": data})
        return result
    



class Card:
    def __init__(self):
        self.cards = db['cards']

    def create_card(self, data):
        result = self.cards.insert_one(data)
        return result

    def find_card(self, cond={}):
        result = self.cards.find_one(cond)
        return result

    def delete_card(self, cond):
        result = self.cards.delete_one(cond)
        return result

    def get_cards(self, cond={}):
        
        if 'search' in cond:
            cond['$or'] = [
                        { "name": {"$regex": '.*' + cond['search'] + '.*', "$options": 'si'} },
                    ]
            del cond['search']

        aggregation = [
            {
                "$match": cond
            },
            {
                "$lookup": {
                    "from": "banks",
                    "let": {
                        "bank": "$bank" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": ["$_id", "$$bank"]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "bank"
                }
            },
            { "$unwind": { "path": "$bank", "preserveNullAndEmptyArrays": True } },

            {
                "$project": {
                    "_id": {
                        "$toString": "$_id"
                    },
                    "name": 1,
                    "status": 1,
                    "bank": { "name": 1, },
                    "createdAt": { "$dateToString": { "format": "%d-%m-%Y", "date": "$createdAt" } },
                }
            },
            {
                "$sort": {
                    'createdAt': -1
                }
            }
        ]
        result = self.cards.aggregate(aggregation)
        return result

    def update_card(self, cond, data):
        result = self.cards.update_one(cond, {"$set": data})
        return result
    



class UserCard:
    def __init__(self):
        self.user_cards = db['usercards']

    def create_user_card(self, data):
        result = self.user_cards.insert_one(data)
        return result

    def find_card(self, cond={}):
        result = self.user_cards.find_one(cond)
        return result

    def delete_card(self, cond):
        result = self.user_cards.delete_one(cond)
        return result
    
    def get_client_cards(self, cond):
        
        aggregation = [
            {
                "$match": cond
            },
            {
                "$lookup": {
                    "from": "cards",
                    "let": {
                        "card": "$card" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": ["$_id", "$$card"]
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "$lookup": {
                                "from": "banks",
                                "let": {
                                    "bank": "$bank" 
                                },
                                "pipeline": [
                                    {
                                        "$match": {
                                            "$expr": {
                                                "$and": [
                                                    {
                                                        "$eq": ["$_id", "$$bank"]
                                                    }
                                                ]
                                            }
                                        }
                                    },
                                    
                                ],
                                "as": "bank"
                            }
                        },
                        { "$unwind": { "path": "$bank" } },
                    ],
                    "as": "card"
                }
            },
            { "$unwind": { "path": "$card" } },
            {
                "$lookup": {
                    "from": "users",
                    "let": {
                        "employees": "$employees" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$in": ["$_id", "$$employees.employee"]
                                }
                            }
                        }
                    ],
                    "as": "employees"
                }
            },

            {
                "$project": {
                    "_id": {
                        "$toString": "$_id"
                    },
                    "card": { "name": 1, "bank": { "name": 1, }},

                    "client": {
                        "_id": {
                            "$toString": "$client"
                        },
                    },
                    "employees": {
                        "$map": {
                            "input": "$employees",
                            "as": "emp",
                            "in": {
                                "_id": { "$toString": "$$emp._id" },
                                "first_name": "$$emp.first_name",
                                "last_name": "$$emp.last_name"
                            }
                        }
                    },
                    "status": 1,
                    "createdAt": { "$dateToString": { "format": "%d-%m-%Y", "date": "$createdAt" } },
                }
            },
            {
                "$sort": {
                    'createdAt': -1
                }
            }
        ]

        result = self.user_cards.aggregate(aggregation)
        return result
    
    def get_all_cards(self, cond):

        # cond={}
        # if employeeId:
        #     cond["$expr"] = {
        #             "$in": [employeeId, "$employees.employee"],
        #         },
        
        
        aggregation=[
            {
                "$match": cond
            },
            {
                "$lookup": {
                    "from": "cards",
                    "let": {
                        "card": "$card" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": ["$_id", "$$card"]
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "$lookup": {
                                "from": "banks",
                                "let": {
                                    "bank": "$bank" 
                                },
                                "pipeline": [
                                    {
                                        "$match": {
                                            "$expr": {
                                                "$and": [
                                                    {
                                                        "$eq": ["$_id", "$$bank"]
                                                    }
                                                ]
                                            }
                                        }
                                    },
                                    
                                ],
                                "as": "bank"
                            }
                        },
                        { "$unwind": { "path": "$bank" } },
                    ],
                    "as": "card"
                }
            },
            { "$unwind": { "path": "$card" } },
            {
                "$lookup": {
                    "from": "users",
                    "let": {
                        "employees": "$employees" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$in": ["$_id", "$$employees.employee"]
                                }
                            }
                        }
                    ],
                    "as": "employees"
                }
            },
            {
                "$lookup": {
                    "from": "clients",
                    "let": {
                        "client": "$client" 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {
                                            "$eq": ["$_id", "$$client"]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "client"
                }
            },
            { "$unwind": { "path": "$client", } },
            {
                "$project": {
                    "_id": {
                        "$toString": "$_id"
                    },
                    "card": { "name": 1, "bank": { "name": 1, }},
                    "client": { "first_name": 1, "last_name": 1 },
                    "employees": { 'first_name': 1, 'last_name': 1,},
                    "createdAt": { "$dateToString": { "format": "%d-%m-%Y", "date": "$createdAt" } },
                }
            },
            {
                "$sort": {
                    'createdAt': -1
                }
            }
        ]

        result = self.user_cards.aggregate(aggregation)
        return result

        