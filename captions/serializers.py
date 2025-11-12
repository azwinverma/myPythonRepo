from rest_framework import serializers

class CaptionRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    tone = serializers.CharField(required=False, default="friendly")
    max_chars = serializers.IntegerField(required=False, default=2200)
    add_emojis = serializers.BooleanField(required=False, default=True)
    add_hashtags = serializers.BooleanField(required=False, default=True)
    topic = serializers.CharField(required=False, default="lifestyle")
    n = serializers.IntegerField(required=False, default=3)

class CaptionVariantSerializer(serializers.Serializer):
    caption = serializers.CharField()
    hashtags = serializers.ListField(child=serializers.CharField(), required=False)

class CaptionResponseSerializer(serializers.Serializer):
    variants = CaptionVariantSerializer(many=True)
    used_model = serializers.CharField()
