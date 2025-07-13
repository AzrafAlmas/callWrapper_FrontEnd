import pymongo
from pymongo import MongoClient
from django.conf import settings
import os
import import_library_clone



# Used for later imports to import the mongodb database for query and whatnot

# MongoDB Atlas connection
MONGODB_URL = os.getenv("mongo_login")

try:
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client["main"]
    # Test connection
    mongo_client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    mongo_client = None
    mongo_db = None