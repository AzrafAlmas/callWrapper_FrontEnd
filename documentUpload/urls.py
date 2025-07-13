
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeResponse, name="documents-about"),
    path('upload', views.uploadResponse, name="documents-upload"),
    path('upload-button', views.upload_button_Response, name="documents-upload-button"),
    path('delete-document', views.delete_Response, name='delete-documents-button')
]
