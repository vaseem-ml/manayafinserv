import shutil
import json
import os
from src.services.db import User
import bcrypt
import jwt
import bson
import datetime

user = User()


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")



def verify_token(token):
    try:
        payload = jwt.decode(token, 'aranyani', algorithms=['HS256'])
        current_user = user.find_user({'_id': bson.ObjectId(payload['_id'])})
        if not current_user:
            return None
        return current_user
    except jwt.exceptions.InvalidSignatureError as e:
        return None