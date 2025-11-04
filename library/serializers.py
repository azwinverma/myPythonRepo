from rest_framework import serializers
from .models import MediaItem

class MediaItemSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MediaItem
        fields = ["id", "type", "name", "url", "size_bytes", "created"]

    def get_url(self, obj):
        return obj.url()
