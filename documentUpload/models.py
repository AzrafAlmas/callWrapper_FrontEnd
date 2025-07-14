from django.db import models

# For signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from import_library_clone import *
from pymongo import MongoClient
import os


# When a user is created, do this
@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):

    if created:  # Only run when user is created, not updated
        new_username = instance.username

        UserProfile.objects.create(user=instance, phone_number="") # ADDS A NEW FIELD 

        # Connect to the mongodb database
        MONGODB_URL = os.getenv("mongo_login_FRONTEND")
        mongo_client = MongoClient(MONGODB_URL)
        db = mongo_client["main"]

        # users collection
        users_collection = db["users"]

        # now insert that
        document = {
            "Username": new_username,
            "Num_Docs": 15,
            "Phone_Number": 0000000000,
            "Calls_This_Month": 0,
            "Estimated_Price_Usage": 0
        }


        users_collection.insert_one(document)

# Now for when a user is deleted, remove them from the database
@receiver(post_delete, sender=User)
def user_deleted_handler(sender, instance, **kwargs):
    to_delete_username = instance.username

    # Connecting to mongodb
    MONGODB_URL = os.getenv("mongo_login_FRONTEND")
    mongo_client = MongoClient(MONGODB_URL)
    db = mongo_client["main"] # Get the database
    users_collection = db["users"] # Get the collection
    
    print("Username to be Deleted: " + to_delete_username)
    
    users_collection.delete_one({"Username": to_delete_username})

################## NEW ADMIN MODELS ##################
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, help_text="Enter phone number")
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
    
## TO SYNC MONGODB AND DJANGO DATABASE STUFF ##
@receiver(post_save, sender=UserProfile)
def sync_phone_to_mongodb(sender, instance, **kwargs):
    """Sync phone number changes to MongoDB"""
    try:
        MONGODB_URL = os.getenv("mongo_login_FRONTEND")
        mongo_client = MongoClient(MONGODB_URL)
        db = mongo_client["main"]
        users_collection = db["users"]
        
        # Update MongoDB with new phone number
        users_collection.update_one(
            {"Username": instance.user.username},
            {"$set": {"Phone_Number": instance.phone_number}}
        )
        mongo_client.close()
        print(f"Updated phone number for {instance.user.username} in MongoDB")
    except Exception as e:
        print(f"Error syncing phone to MongoDB: {e}")