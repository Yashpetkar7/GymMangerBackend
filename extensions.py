# extensions.py
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://yashpetkar07:<db_password>@cluster0.zuowc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.gym_management
users_collection = db.users
