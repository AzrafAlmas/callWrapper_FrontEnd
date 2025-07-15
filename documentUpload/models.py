from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from import_library_clone import *
from pymongo import MongoClient
import os

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username

@receiver(post_save, sender=CustomUser)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        new_username = instance.username
        MONGODB_URL = os.getenv("mongo_login_FRONTEND")
        mongo_client = MongoClient(MONGODB_URL)
        db = mongo_client["main"]
        users_collection = db["users"]
        
        document = {
            "Username": new_username,
            "Num_Docs": 15,
            "Phone_Number": instance.phone_number or "0000000000",
            "Calls_This_Month": 0,
            "Estimated_Price_Usage": 0
        }
        users_collection.insert_one(document)

@receiver(post_delete, sender=CustomUser)
def user_deleted_handler(sender, instance, **kwargs):
    to_delete_username = instance.username
    MONGODB_URL = os.getenv("mongo_login_FRONTEND")
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client["main"]
    users_collection = db["users"]
    print("Username to be Deleted: " + to_delete_username)
    users_collection.delete_one({"Username": to_delete_username})