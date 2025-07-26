import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["chat_db"]

users_collection = db["users"]
conversations_collection = db["conversations"]
