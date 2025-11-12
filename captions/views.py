# captions/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

CAPTION_STYLES = [
    {"id": "minimal", "name": "Minimal & Clean"},
    {"id": "trending", "name": "Trending/Relay"},
    {"id": "storyteller", "name": "Storyteller"},
    {"id": "funny", "name": "Funny/Playful"},
    {"id": "motivational", "name": "Motivational"},
]

def styles(request):
    return JsonResponse({"styles": CAPTION_STYLES}, status=200)

@csrf_exempt
def generate_captions(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Use POST"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = {}

    topic = (data.get("topic") or "").strip()
    style = (data.get("style") or "minimal").strip()
    hashtags = bool(data.get("hashtags", True))
    count = int(data.get("count") or 5)
    count = max(1, min(count, 10))

    if not topic:
        return JsonResponse({"detail": "Missing 'topic'."}, status=400)

    # Dummy captions for now; plug in your LLM later
    base = [
        f"{topic} — keeping it real ✨",
        f"Little moments, big vibes: {topic}",
        f"{topic} and a whole lot of sunshine ☀️",
        f"Made for this: {topic}",
        f"Today’s energy: {topic} 💫",
        f"POV: you love {topic}",
        f"{topic}, but make it aesthetic",
        f"Just {topic} things 🧿",
        f"{topic} — less talk, more feel",
        f"Still thinking about {topic}…",
    ]

    captions = base[:count]
    if hashtags:
        tag = "#" + topic.replace(" ", "")
        captions = [f"{c}\n\n{tag} #DailyMantra #Inspo" for c in captions]

    return JsonResponse({
        "style": style,
        "topic": topic,
        "captions": captions,
    }, status=200)





# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from .serializers import CaptionRequestSerializer
# from .helpers import (
#     DEFAULT_STYLES, pick_hashtags, trim_text, local_template, hf_generate, HF_TOKEN
# )

# @api_view(["GET"])
# @permission_classes([permissions.AllowAny])
# def styles(request):
#     return Response({"styles": list(DEFAULT_STYLES.keys()), "can_use_hf": bool(HF_TOKEN)})

# @api_view(["POST"])
# @permission_classes([permissions.AllowAny])
# def generate_captions(request):
#     s = CaptionRequestSerializer(data=request.data)
#     s.is_valid(raise_exception=True)
#     req = s.validated_data

#     prompt = req["prompt"].strip()
#     tone = req.get("tone", "friendly")
#     max_chars = req.get("max_chars", 2200)
#     add_emojis = req.get("add_emojis", True)
#     add_hashtags = req.get("add_hashtags", True)
#     topic = req.get("topic", "lifestyle")
#     n = max(1, req.get("n", 3))

#     variants = []
#     used_model = "templated-local"

#     if HF_TOKEN:
#         # Try HF for each variant; if HF fails once, fallback to local for that one.
#         for _ in range(n):
#             style_hint = DEFAULT_STYLES.get(tone, tone)
#             full_prompt = (
#                 "Write an Instagram caption.\n"
#                 f"Style: {style_hint}\n"
#                 f"Topic/context: {prompt}\n"
#                 "Keep it short and catchy. Do not include hashtags in the body.\n"
#             )
#             try:
#                 txt, used_model = hf_generate(full_prompt)
#             except Exception:
#                 txt = local_template(prompt, tone, add_emojis)
#                 used_model = "templated-local (fallback)"
#             cap = trim_text(txt, max_chars)
#             tags = pick_hashtags(topic) if add_hashtags else []
#             variants.append({"caption": cap, "hashtags": tags})
#     else:
#         # Local-only
#         for _ in range(n):
#             cap = local_template(prompt, tone, add_emojis)
#             cap = trim_text(cap, max_chars)
#             tags = pick_hashtags(topic) if add_hashtags else []
#             variants.append({"caption": cap, "hashtags": tags})

#     return Response({"variants": variants, "used_model": used_model}, status=status.HTTP_200_OK)
