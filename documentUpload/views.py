

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

# PDF import
from PyPDF2 import PdfReader

#### HOME PAGE ####
def homeResponse(request):
    context_block = {
        "name": request.user.username
    }
    return render(request, "home.html", context_block)

#### SUBMIT BUTTON FOR DOCUMENTS ####
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
        # MongoDB Collection
        client = MongoClient(os.getenv("mongo_login_FRONTEND"))
        db = client["main"]
        content_collection = db["content"]
        users_collection = db["users"]
        
        # Check if there are any documents left to upload
        user_information = users_collection.find_one(
            {"Username": user}
        )
        # Now dump and load
        user_info_dump = dumps(user_information)
        user_info_loads = json.loads(user_info_dump)

        # Now check if they user has any documents left to upload
        if int(user_info_loads["Num_Docs"]) == 0:
            return render(request, "upload_error.html")

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

            # Update user data
            users_collection.find_one_and_update(
                {"Username": user},
                {"$inc": {"Num_Docs": -1}}
            )

        # Now PDF Compatibility for type
        if upload_type == "PDF" and "pdf_file" in request.FILES:
            pdf_file = request.FILES['pdf_file'] # Gets the file
            reader = PdfReader(pdf_file) # Read the pdf file
            parsed_pdf = ''

            # Extracts the text
            for page in reader.pages:
                parsed_pdf += page.extract_text() or ''
            # Now 'text' contains the extracted PDF text
            
            ## Get ready and upload
            pdf_document = {
                "Username": user,
                "Title": request.POST.get("title"),
                "Type": upload_type,
                "Content": parsed_pdf,
            }
            content_collection.insert_one(pdf_document) # Insert the document to database
            users_collection.find_one_and_update(
                {"Username": user},
                {"$inc": {"Num_Docs": -1}}
            )
            
            # Update user database

    # Handle GET request (initial page load)
    return redirect('/upload')
    
#### FOR THE UPLOAD PAGE ####
def uploadResponse(request):

    # The context block will hold all the documents that belong to the user
    # Following are the database imports and whatnot
    client = MongoClient(os.getenv("mongo_login_FRONTEND"))
    db = client["main"]

    if request.user.is_authenticated:
        account_user = request.user.username
        content_collection = db["content"]
        users_collection = db["users"]

        # Get content based on the logged in username
        user_data = content_collection.find(
            {"Username":account_user}
        )

        user_information = users_collection.find_one({"Username": account_user})
        

        # Keep in mind that when you do (find), it will always return a list of items, even when there is only 1 item
        # Formatted to be [ {item 1}, {item 2} ] etc

        dumped_user_data = dumps(user_data) # Must first dump to get it as a string
        loaded_user_data = json.loads(dumped_user_data) # And then load to make it work like a JSON formatted string

        context_block ={
            "content_gotten": loaded_user_data,
            "Phone_Number": user_information["Phone_Number"],
            "Number_Docs": user_information["Num_Docs"]
        }

    return render(request, "upload.html", context_block)

#### DELETE DOCUMENT BUTTON ####
def delete_Response(request):
    user = request.user.username

    # MongoDB Collection
    client = MongoClient(os.getenv("mongo_login_FRONTEND"))
    db = client["main"]
    content_collection = db["content"]
    users_collection = db["users"]
    
    # Check if there are any documents left to upload
    user_information = users_collection.find_one(
        {"Username": user}
    )

    # Now dump and load
    user_info_dump = dumps(user_information)
    user_info_loads = json.loads(user_info_dump)

    # Delete the said document 
    document_to_delete = request.POST.get('title')
    print("Document to DELETE: " + document_to_delete)

    # Delete the document from the database
    content_collection.find_one_and_delete({"Title": document_to_delete})

    # update the user collection
    users_collection.find_one_and_update(
        {"Username": user},
        {"$inc": {"Num_Docs": 1}}
    )

    return render(request, "document_deleted.html")