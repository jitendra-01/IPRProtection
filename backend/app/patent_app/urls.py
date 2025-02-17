from django.urls import path
from .views import upload_patent

urlpatterns = [
    path("upload/", upload_patent, name="upload_patent"),
]
