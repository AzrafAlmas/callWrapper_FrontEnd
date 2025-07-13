
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeResponse, name="documents-about"),
    path('upload', views.uploadResponse, name="documents-upload"),
]
