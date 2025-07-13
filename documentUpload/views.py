from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def aboutResponse(request):
    context_block = {}
    return render(request, "about.html", context_block)

def uploadResponse(request):
    context_block = {}
    return render(request, "upload.html", context_block)