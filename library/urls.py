from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path("upload/audio", views.upload_audio),
    path("upload/ebook", views.upload_ebook),
    path("list/audio", views.list_audio),
    path("list/ebooks", views.list_ebooks),
    # Mobile-friendly aliases (optional, keeps Flutter simple)
    path("meditation-tracks/", views.list_audio, name="meditation-tracks"),
    path("ebooks/", views.list_ebooks, name="ebooks"),
]
