from django.urls import path
from .views import upload_patent,transfer_ownership

urlpatterns = [
    path("upload/", upload_patent, name="upload_patent"),
    path("transfer_ownership/", transfer_ownership, name="transfer_ownership")
]
