from django.urls import path
from . import views

urlpatterns = [
    path("upload/audio", views.upload_audio),
    path("upload/ebook", views.upload_ebook),
    path("list/audio", views.list_audio),
    path("list/ebooks", views.list_ebooks),
]
