from django.db import models

# For signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Remove this line: from django.contrib.auth.models import User

from import_library_clone import *
from pymongo import MongoClient
import os

########## NEW ADMIN IMPORTS ########
from django.contrib.auth.models import AbstractUser

#######33 new custom user class
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username

# When a user is created or updated, do this - UPDATED to use CustomUser
@receiver(post_save, sender=CustomUser)
def user_created_or_updated_handler(sender, instance, created, **kwargs):
    username = instance.username
    
    # Connect to the mongodb database
    MONGODB_URL = os.getenv("mongo_login_FRONTEND")
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client["main"]
    users_collection = db["users"]

    if created:  # User is being created
        # Insert new document
        document = {
            "Username": username,
            "Num_Docs": 15,
            "Phone_Number": instance.phone_number or "0000000000",
            "Calls_This_Month": 0,
            "Estimated_Price_Usage": 0
        }
        users_collection.insert_one(document)
        print(f"User {username} created in MongoDB with phone: {instance.phone_number}")
        
    else:  # User is being updated
        # Update the phone number in MongoDB
        users_collection.update_one(
            {"Username": username},
            {"$set": {"Phone_Number": instance.phone_number or "0000000000"}}
        )
        print(f"User {username} phone number updated in MongoDB to: {instance.phone_number}")

# Now for when a user is deleted, remove them from the database - UPDATED to use CustomUser
@receiver(post_delete, sender=CustomUser)
def user_deleted_handler(sender, instance, **kwargs):
    to_delete_username = instance.username

    # Connecting to mongodb
    MONGODB_URL = os.getenv("mongo_login_FRONTEND")
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client["main"] # Get the database
    users_collection = db["users"] # Get the collection
    
    print("Username to be Deleted: " + to_delete_username)
    
    users_collection.delete_one({"Username": to_delete_username})