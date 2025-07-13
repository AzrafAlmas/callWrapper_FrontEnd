

# IMPORTS
from import_library_clone import *
import os # Must be manually imported
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
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

def upload_button_Response(request):
    if request.method == 'POST':
        user = request.user.username
        upload_type = request.POST.get("type")


        '''
            To upload a mongodb index, the following format must be followed:
            Capitals count. ID will be made automatically, but these must exist



            Content: content
            Title: title
            Username: username
            Type: type
            Website_Link: link

            the "Content" will have the parsed text in it
            Only some stuff will have the link in it
        '''

        # website parsing
        if upload_type == "Website":
            web_link = request.POST.get("website_link")

            # Now actually parse the website
            response = requests.get(web_link)
            response.raise_for_status() # If the website is down or something
            # Parse
            soup = BeautifulSoup(response.content, "html.parser")

            # Get the text
            parsed_text = soup.get_text(separator="", strip=True)

            # Now upload it to the mongodb database
            # Make sure to add to the "content" collection 
            client = MongoClient(os.getenv("mongo_login_FRONTEND"))
            db = client["main"]
            content_collection = db["content"]

            # Creating the JSON
            document = {
                "Username": user,
                "Title": request.POST.get("title"),
                "Type": upload_type,
                "Content": parsed_text,
                "Website_Link":web_link
            }

            # Now insert
            content_collection.insert_one(document)
    
    # Handle GET request (initial page load)
    return redirect('/upload')
    
    
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


def delete_Response(request):
    print(request.POST.get('title'))
    return HttpResponse("Hello my pookie")