from django.db import models

class MediaItem(models.Model):
    AUDIO = "audio"
    EBOOK = "ebook"
    TYPE_CHOICES = [(AUDIO, "Audio"), (EBOOK, "eBook")]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.FileField(upload_to="audio/", blank=True, null=True)
    ebook = models.FileField(upload_to="ebooks/", blank=True, null=True)
    name = models.CharField(max_length=255)  # original or display name
    size_bytes = models.PositiveBigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def url(self):
        f = self.file or self.ebook
        return f.url if f else ""

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # set size after file saved
        f = self.file or self.ebook
        if f and f.size != self.size_bytes:
            self.size_bytes = f.size
            super().save(update_fields=["size_bytes"])
