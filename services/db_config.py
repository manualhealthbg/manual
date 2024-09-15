DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'manual',
}

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["manual"]
quiz_collection = mongo_db["quizes"]