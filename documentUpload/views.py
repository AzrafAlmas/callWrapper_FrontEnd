

# IMPORTS
import import_library_clone
import os # Must be manually imported
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

# Database imports
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps  # Handles ObjectId and other MongoDB types

# Create your views here.
def homeResponse(request):
    context_block = {
        "name": request.user.username
    }
    return render(request, "home.html", context_block)

def uploadResponse(request):
    # The context block will hold all the documents that belong to the user
    # Following are the database imports and whatnot
    client = MongoClient(os.getenv("mongo_login_FRONTEND"))
    db = client["main"]

    if request.user.is_authenticated:
        account_user = request.user.username
        content_collection = db["content"]

        # Get content based on the logged in username
        user_data = content_collection.find(
            {"Username":account_user}
        )

        # Keep in mind that when you do (find), it will always return a list of items, even when there is only 1 item
        # Formatted to be [ {item 1}, {item 2} ] etc

        dumped_user_data = dumps(user_data) # Must first dump to get it as a string
        loaded_user_data = json.loads(dumped_user_data) # And then load to make it work like a JSON formatted string

        context_block ={
            "content_gotten": loaded_user_data
        }

    return render(request, "upload.html", context_block)