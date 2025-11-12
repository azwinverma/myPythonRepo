from django.urls import path
from . import views

urlpatterns = [
    # path("captions/generate", views.generate_captions, name="generate_captions"),
    # path("captions/styles", views.styles, name="styles"),

    path("styles", views.styles, name="caption_styles"),
    path("styles/", views.styles, name="caption_styles_slash"),
    path("generate", views.generate_captions, name="caption_generate"),
    path("generate/", views.generate_captions, name="caption_generate_slash"),
]
