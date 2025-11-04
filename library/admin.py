from django.contrib import admin
from .models import MediaItem

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "name", "size_bytes", "created")
    search_fields = ("name",)
    list_filter = ("type",)
