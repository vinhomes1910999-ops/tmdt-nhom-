from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import StaticPage, ContactMessage


def page_list(request):
    pages = StaticPage.objects.all().order_by("-updated_at")

    data = [
        {
            "id": page.id,
            "slug": page.slug,
            "title": page.title,
            "content": page.content,
            "updated_at": page.updated_at,
        }
        for page in pages
    ]

    return JsonResponse(data, safe=False)


def page_detail(request, slug):
    try:
        page = StaticPage.objects.get(slug=slug)
    except StaticPage.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy nội dung"},
            status=404
        )

    return JsonResponse({
        "id": page.id,
        "slug": page.slug,
        "title": page.title,
        "content": page.content,
        "updated_at": page.updated_at,
    })


@require_http_methods(["POST"])
def contact_message(request):
    import json

    try:
        data = json.loads(request.body)

        message = ContactMessage.objects.create(
            full_name=data.get("full_name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            subject=data.get("subject", ""),
            message=data.get("message", "")
        )

        return JsonResponse({
            "success": True,
            "message": "Gửi liên hệ thành công",
            "id": message.id
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)
def policy(request):
    return JsonResponse({
        "title": "Privacy Policy",
        "content": (
            "We respect customer privacy. "
            "Customer information is only used "
            "to provide and improve our services."
        )
    })


def store_location(request):
    return JsonResponse({
        "name": "Fashion Store",
        "address": "Ho Chi Minh City, Vietnam",
        "google_maps": (
            "https://www.google.com/maps/search/"
            "?api=1&query=Ho+Chi+Minh+City"
        )
    })
