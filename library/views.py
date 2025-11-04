import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import MediaItem
from .serializers import MediaItemSerializer

AUDIO_EXT = {".mp3", ".m4a", ".wav", ".aac", ".ogg"}
EBOOK_EXT = {".pdf", ".epub", ".mobi", ".azw3"}

def _ext_ok(name: str, allow: set[str]) -> bool:
    _, ext = os.path.splitext(name or "")
    return ext.lower() in allow

@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_audio(request):
    f = request.FILES.get("file")
    if not f or not _ext_ok(f.name, AUDIO_EXT):
        return Response({"detail": "Invalid or missing audio file"}, status=400)
    item = MediaItem.objects.create(type=MediaItem.AUDIO, file=f, name=f.name)
    return Response(MediaItemSerializer(item).data, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_ebook(request):
    f = request.FILES.get("file")
    if not f or not _ext_ok(f.name, EBOOK_EXT):
        return Response({"detail": "Invalid or missing ebook file"}, status=400)
    item = MediaItem.objects.create(type=MediaItem.EBOOK, ebook=f, name=f.name)
    return Response(MediaItemSerializer(item).data, status=201)

@api_view(["GET"])
@permission_classes([AllowAny])
def list_audio(request):
    qs = MediaItem.objects.filter(type=MediaItem.AUDIO).order_by("name")
    return Response(MediaItemSerializer(qs, many=True).data)

@api_view(["GET"])
@permission_classes([AllowAny])
def list_ebooks(request):
    qs = MediaItem.objects.filter(type=MediaItem.EBOOK).order_by("name")
    return Response(MediaItemSerializer(qs, many=True).data)
