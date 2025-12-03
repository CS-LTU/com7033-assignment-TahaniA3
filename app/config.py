import pymongo
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId  



client = MongoClient('mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/')
server_info = client.server_info()

mongo_version = server_info["version"]

print(f"mongoDB version: {mongo_version}")

db = client["stroke_database"]
collection = db["stroke_collection"]
# Users collection for authentication
users_collection = db["users"] 

