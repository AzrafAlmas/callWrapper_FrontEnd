

# IMPORTS
import import_library
import os # Must be manually imported
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def aboutResponse(request):
    context_block = {}
    print(os.getenv("mongo_login"))
    return render(request, "about.html", context_block)

def uploadResponse(request):
    context_block = {}
    return render(request, "upload.html", context_block)